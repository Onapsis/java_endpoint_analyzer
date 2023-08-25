#!/usr/bin/env python3
import os

from xml.etree import ElementTree as ET
from analyzers.webdynpros.wdData import WDData

WEBDYNPRO = "webdynpro"
APPLICATIONS = "applications"
SHORT_NAMES = "Short names"
CLASS = "class"
NAME = "name"
SHORT_NAME = "shortName"


class WDEndpointAnalyzer:
    def __init__(self):
        pass

    def _parse_tags(self, webdynpro_data):
        tags_info = {SHORT_NAMES:[]}
        for children in list(webdynpro_data):
            if children.tag == APPLICATIONS:
                for part in list(children):
                    part_data = part.attrib
                    part_data[CLASS] = part_data.pop(NAME) #Change the "name" of the key from NAME to CLASS
                    tags_info[SHORT_NAMES].append(part_data)
        return tags_info

    def _parse(self, xml_file_path):
        xml_content = ET.parse(xml_file_path)
        xml_root = xml_content.getroot()
        res = {}
        for children in list(xml_root):
          if children.tag == WEBDYNPRO:
            res = self._parse_tags(children)
        return res
    

    def _get_services(self, config_file):
        filename = config_file.split('/')[-1]
        app_name = filename.split("_webdynpro.xml")[0]
        wd_data = self._parse(config_file)
        entrypoints = set()
        base_template = f"/webdynpro/resources/sap.com/{app_name}"
        for short_name_data in wd_data[SHORT_NAMES]:
            short_name = short_name_data[SHORT_NAME]
            entrypoints.add(f"{base_template}/{short_name}")
        return WDData(filename, app_name, entrypoints)
    

    def analyze(self, directory):
        all_services = []
        for filename in os.listdir(directory):
            full_filepath = os.path.join(directory, filename)
            services = self._get_services(full_filepath)
            all_services.append(services)

        return {service.app_name:service.__dict__ for service in all_services}