#!/usr/bin/env python3
import os

from xml.etree import ElementTree as ET
from analyzers.servlets.ServletData import ServletData

SECURITY_CONSTRAINT_TAG = "security-constraint"
SECURITY_CONSTRAINT = "Has Security Constraint"
SERVLET_MAPPING_TAG = "servlet-mapping"
SERVLET_NAME_TAG = "servlet-name"
SERVLET_TAG = "servlet"
SERVLET_CLASS_TAG = "servlet-class"
SERVLET_URL_PATTERN_TAG = "url-pattern"
SERVLETS = "servlets"
IS_SOAP = "Is SOAP"
CLASS = "class"
PATTERN = "pattern"
SOAP_SERVLET_CLASS = "com.sap.engine.services.webservices.servlet.SoapServlet"



class SOAPServerClassFound(Exception): pass

class ServletEndpointAnalyzer:
    def __init__(self):
        pass

    def _get_tag(self, complete_tag_name):
        """
            {http://java.sun.com/xml/ns/javaee}context-param
        """
        return complete_tag_name.split("}")[1]

    def _get_info_from_servlet_tag(self, children_tag):
        servlet_name, servlet_class = "", ""
        for subchild in list(children_tag):
            tag = self._get_tag(subchild.tag)
            if tag == SERVLET_NAME_TAG:
                servlet_name = subchild.text
            if tag == SERVLET_CLASS_TAG:
                servlet_class = subchild.text
            else: 
                continue # Not important yet.
    
        return (servlet_name, servlet_class)
    
    def _get_info_from_servlet_mapping_tag(self, children_tag):
        servlet_name, servlet_pattern = "", ""
        for subchild in list(children_tag):
            tag = self._get_tag(subchild.tag)
            if tag == SERVLET_NAME_TAG:
                servlet_name = subchild.text
            if tag == SERVLET_URL_PATTERN_TAG:
                servlet_pattern = subchild.text
            else: 
                continue # Not important yet.
    
        return (servlet_name, servlet_pattern)

    def _parse_tags(self, xml_root):
        
        tags_info = {SERVLETS:{}, SECURITY_CONSTRAINT:False}
        for children_tag in list(xml_root):
            tag = self._get_tag(children_tag.tag) 
            if tag == SERVLET_TAG:
                is_soap = False
                name, _class = self._get_info_from_servlet_tag(children_tag)
                if _class == SOAP_SERVLET_CLASS:
                    # is_soap = True
                    raise SOAPServerClassFound()

                if name in tags_info[SERVLETS].keys():
                    tags_info[SERVLETS][name].update({CLASS:_class, IS_SOAP:is_soap})
                else:
                    tags_info[SERVLETS].update({name:{CLASS:_class, IS_SOAP:is_soap}})

            elif  tag == SERVLET_MAPPING_TAG:
                name, pattern = self._get_info_from_servlet_mapping_tag(children_tag)
                if name in tags_info[SERVLETS].keys():
                    tags_info[SERVLETS][name].update({PATTERN:pattern})
                else:
                    tags_info[SERVLETS].update({name:{PATTERN:pattern}})
            
            elif tag == SECURITY_CONSTRAINT_TAG:
                tags_info[SECURITY_CONSTRAINT] = True
            else:
                continue
        return tags_info

    def _parse(self, xml_file_path):
        xml_content = ET.parse(xml_file_path)
        xml_root = xml_content.getroot()
        return self._parse_tags(xml_root)
    

    def _get_services(self, config_file):
        filename =  config_file.split('/')[-1]
        app_name = filename.split("_servlet_jsp_")[0]
        sub_app = filename.split("_servlet_jsp_")[1].split("_web.xml")[0]
        servlets_data = self._parse(config_file)
    
        entrypoints = set()
        for servlet_info in servlets_data[SERVLETS].items():
            if PATTERN in servlet_info[1]:
                pattern = servlet_info[1][PATTERN].replace("*", "").strip("/")
                entrypoints.add(f"/{sub_app}/{pattern}")

        return ServletData(filename, app_name, sub_app, entrypoints, servlets_data[SECURITY_CONSTRAINT])
 
    def analyze(self, directory):
        all_services = []
        for filename in os.listdir(directory):
            full_filepath = os.path.join(directory, filename)
            try:
                services = self._get_services(full_filepath)
                all_services.append(services)

            except IndexError as e: 
                print(str(e))
                print(filename)
                continue

            except SOAPServerClassFound: 
                continue

        return {service.app_name:service.__dict__ for service in all_services}