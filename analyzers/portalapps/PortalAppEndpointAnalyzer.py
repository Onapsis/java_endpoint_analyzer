#!/usr/bin/env python3
import os

from xml.etree import ElementTree as ET
from analyzers.portalapps.PortalData import PortalData

WEBDYNPRO = "webdynpro"
COMPONENTS = "components"
COMPONENT = "component"
COMPONENT_CONFIG = "component-config"
PROPERTY = "property"

NAME = "name"
VALUE = "value"
COMPONENT_DATA = "Component names"

class PortalAppEndpointAnalyzer:
    def __init__(self):
        pass

    def _parse_tags(self, portalapp_data):
        tags_info = {COMPONENT_DATA:[]}
        for children in list(portalapp_data):
            data = {}
            if children.tag == COMPONENT:
                data = children.attrib
                for subchildren in list(children):
                    if subchildren.tag == COMPONENT_CONFIG:
                        for subsubchildren in list(subchildren):
                            if subsubchildren.tag == PROPERTY:
                                attribs = subsubchildren.attrib
                                try:
                                    data.update({attribs[NAME]:attribs[VALUE]})
                                except KeyError:
                                    continue
                tags_info[COMPONENT_DATA].append(data)
        return tags_info

    def _parse(self, xml_file_path):
        xml_content = ET.parse(xml_file_path)
        xml_root = xml_content.getroot()
        res = {COMPONENT_DATA:[]}
        for children in list(xml_root):
          if children.tag == COMPONENTS:
            res = self._parse_tags(children)
        return res
    
    def _get_services(self, config_file):
        filename =  config_file.split('/')[-1]
        app_name = filename.split("_portalapp.xml")[0]
        portal_data = self._parse(config_file)
        entrypoints = set()
        base_template = f"/irj/servlet/prt/portal/prtroot/{app_name}"
        for component_data in portal_data[COMPONENT_DATA]:
            component_name = component_data[NAME]
            entrypoints.add(f"{base_template}.{component_name}")
        return PortalData(filename, app_name, entrypoints)


    def analyze(self, directory):
        all_services = []
        for filename in os.listdir(directory):
            full_filepath = os.path.join(directory, filename)
            services = self._get_services(full_filepath)
            all_services.append(services)

        return {service.app_name:service.__dict__ for service in all_services}
