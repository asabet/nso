#!/usr/bin/python

"""
This package contains all the logic to add a device to an NSO PNP server. 
Python package dependencies:
    requests==2.11.1

NSO Package dependencies: 
    cisco-pnp (1.5.0) - Official release
    pnp-devices (1.0) - see pnp-devices.tgz in this directory
    
How to use:
1) import the package
2) point the baseurl variable to the NSO REST api.
3) point the services variable to services.
4) instantiate a pnpadd object.
5) generate the XML (requires device serial and name)
6) post the XML to the rest API.

from pnpadd.pnpadd import pnpadd
baseurl = 'http://127.0.0.1:8080/api/'
service = '/running/services/'
device = pnpadd(baseurl, service)
serial = "9KXXI19RRUZ"
name = "CSR1kv-001"
device.gen_xml(serial, name)
device.create()
if device.status_code == 201:
  print("A OK!")
else:
  print(device.content)
"""

class pnpadd:
    def __init__(self, baseurl, service, login = ('admin', 'admin'), headers= {'Content-Type': 'application/vnd.yang.data+xml'} ):
        """
        Initialisation of the class sets the variables needed to POST the XML towards the NSO REST API.
        We assume admin/admin for credentials and set the HTTP header to XML.
        """
        self.baseurl = baseurl
        self.service = service
        self.login = login
        self.headers = headers
        self.xml = None
        self.status_code = None
        self.content = None

    def gen_xml(self):
        """
        To generate the XML that we will send to the REST API, we need the serialnumber and device name. If a devicename it not
        given we will generate it from the serial.
        """
        self.xml = """
           vnfd
              <user xmlns="http://tail-f.com/ns/aaa/1.1">
                <name>test</name>
              </user>
           /vnfd
file not create a xml 
        """
        
    def create(self):
        """
        To post the XML to the REST API we will use the python requests package (http://docs.python-requests.org/en/master/).
        We store the status and content that we get back in variables, so that we can use them from outside the class.
        """
        import requests
        reqPOST = requests.post(self.baseurl + self.service, auth=self.login, headers=self.headers, data=self.xml)
        self.status_code = reqPOST.status_code
        self.content = reqPOST.content


if __name__ == "__main__":
    """
    If we use use pnpadd.py from the CLI, we need to give the serial and the name as parameters.
    e.g.: $ python pnpadd.py 9KXXI19RRUZ CSR1kv-001
    """
    baseurl = 'http://127.0.0.1:8081/api/'
    service = '/running/nfvo/'
    device = pnpadd(baseurl, service)
    device.gen_xml()
    device.create()
