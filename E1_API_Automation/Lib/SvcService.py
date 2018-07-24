import ssl

from suds.client import Client
from suds.wsse import *


class SvcService:
    def __init__(self, service_wsdl, security_user=None):
        self.wsdl = service_wsdl
        self.security_user = security_user
        self.client = None

    def create_service(self):
        self.client = Client(self.wsdl)
        if self.security_user:
            security = Security()
            token = UsernameToken(self.security_user.get('username'), self.security_user.get('password'))
            security.tokens.append(token)
            self.client.set_options(wsse=security)
