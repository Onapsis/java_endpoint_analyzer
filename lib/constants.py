# Types
ALL = "ALL"
SOAP = "SOAP"
SERVLETS = "SERVLETS"
WEBDYNPROS ="WEBDYNPRO"
PORTALAPPS ="PORTALAPPS"





#General stuff
DASH_NUMBER_LINE = 35
DIR_RESULTS = "extracted_files"
CREATE_TEMP_DIR_CMD =  "mkdir -p {}"
SAP_APPS_DIR = "/usr/sap/{sid}/J{instance}/j2ee/cluster/apps/sap.com/"
SCRIPT_PATH = '/tmp/get_all_config_files.sh'
OUTPUT_ENDPOINTS_FILE = "endpoints.json"

# Portal Apps 
PORTALAPP_FILETYPE = "PortalApp"
PORTALAPP_DIR_RESULTS = "portalapp"

PORTALAPP_CONFIG_COMMAND_EXTRACT = """#!/bin/bash
cd {sap_apps_dir}
for portalapp_path in $(find * -type f -name portalapp.xml);do
   yes|cp $portalapp_path {random_dir_path}/$(echo $portalapp_path | awk -F/ '{{print $1}}')_$(echo $portalapp_path | awk -F/ '{{print $NF}}')
done
"""


# Servlets
SERVLETS_FILETYPE = "Servlet"
SERVLETS_DIR_RESULTS = "servlet"
SERVLETS_WEBXML_COMMAND_EXTRACT = """#!/bin/bash

cd {sap_apps_dir}
for full_path_to_file in $(find ~+ -name web.xml  | awk -Fweb.xml '{{print $1}}' | xargs -I% ls %webdynpro.xml 2>&1  >/dev/null | awk -F"access " '{{print $2}}' | awk -F"webdynpro.xml" '{{print $1}}' | xargs -I % ls %portalapp.xml 2>&1  >/dev/null | awk -F"access " '{{print $2}}' | awk -F"portalapp.xml" '{{print $1}}')
do
    cp $full_path_to_file/web.xml {random_dir_path}/$(echo $full_path_to_file | awk -F"/sap.com/" '{{print $2}}'| awk -F"/root/" '{{print $1}}' | sed  "s/\//_/g")_web.xml 
done    
"""

# Webdynpro
WEBDYNPRO_FILETYPE = "Webdynpro"
WEBDYNPRO_DIR_RESULTS = "webdynpro"
WEBDYNPRO_CONFIG_COMMAND_EXTRACT = """#!/bin/bash
cd {sap_apps_dir}
for webdynpro_path in $(find * -type f -name webdynpro.xml);do
   yes|cp $webdynpro_path {random_dir_path}/$(echo $webdynpro_path | awk -F/ '{{print $1}}')_$(echo $webdynpro_path | awk -F/ '{{print $NF}}')
done
"""

# SOAP
SOAP_FILETYPE = "SOAP"
SOAP_ERROR1 = "servlet_jsp"
SOAP_ERROR2 = "No such file or directory"
SOAP_DIR_RESULTS = "soap"
SOAP_CONFIG_COMMAND_EXTRACT = """#!/bin/bash

cd {sap_apps_dir}
for full_path_to_file in $(find * -type f -name web.xml|xargs -I % bash -c "grep webservices.servlet.SoapServlet % &> /dev/null && echo %   | cut -d '/' -f 2"| sort| uniq | xargs -I % find % -type f -iname "configuration*.xml")
do
   yes|cp $full_path_to_file {random_dir_path}/$(echo $full_path_to_file | awk -F/ '{{print $1}}')_$(echo $full_path_to_file | awk -F/ '{{print $NF}}')
done
"""


