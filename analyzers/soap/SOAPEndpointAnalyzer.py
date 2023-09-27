#!/usr/bin/env python3
import os
import warnings
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning
from analyzers.soap.SOAPData import SOAPData

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning, module='bs4')


NON_AUTH = "None"
SERVICE= "service"
BINDING_DATA= "bindingdata" 
SERVICE_DATA = "servicedata"
URL = "url"
AUTHENTICATION_METHOD = "AuthenticationMethod"
CONTEXT_ROOT = "contextroot"
NAME = "name"
PROPERTY_LIST = "propertylist"
PROPERTY = "property"
AUTHENTICATION_TEMPLATE = "AuthenticationTemplate"

class SOAPEndpointAnalyzer:

    def _get_auth_methods(self, binding_data):
        auth_methods = set()
        property_lists = binding_data.find_all(PROPERTY_LIST)
        for property_list in property_lists:
            properties = property_list.find_all(PROPERTY)
            for prop in properties:
                if prop.get(NAME) == AUTHENTICATION_METHOD or prop.get(NAME) == AUTHENTICATION_TEMPLATE:
                    auth_methods.add(prop.text)
        
        return auth_methods if auth_methods else {NON_AUTH}

    def _parse(self, config_file):
        with open(config_file, 'r') as f:
            xml_content = f.read()
        content = BeautifulSoup(xml_content, features="html.parser")
        return content
        
    def _get_services(self, config_file):
        filename = config_file.split("/")[-1]

        soap_content = self._parse(config_file)
        services_data = [] 
        services = soap_content.find_all(SERVICE)
        for service in services:
            name = service.get(NAME)
            service_data =  service.find(SERVICE_DATA)
            context_root = service_data.get(CONTEXT_ROOT)
            binding_data = service.find(BINDING_DATA)
            entrypoint = binding_data.get(URL)
            auth_methods = self._get_auth_methods(binding_data)
            service_data = SOAPData(filename, name, context_root, entrypoint, auth_methods)
            services_data.append(service_data)
        return services_data
  
    def analyze(self, directory):
        all_services = []
        for filename in os.listdir(directory):
            full_filepath = os.path.join(directory, filename)
            services = self._get_services(full_filepath)
            all_services.extend(services)
        return {service.app_name:service.__dict__ for service in all_services}



