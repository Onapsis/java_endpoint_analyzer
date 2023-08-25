#!/usr/bin/env python3
import json
from argparse import ArgumentParser
from ConfigFileExtractor import ConfigFileExtractor
from EndpointAnalyzer import EndpointAnalyzer
from lib.constants import DIR_RESULTS,SOAP,WEBDYNPROS,PORTALAPPS,SERVLETS,ALL, OUTPUT_ENDPOINTS_FILE
from lib.system_config import SAP_HOST, SAP_INSTANCE, SAP_SID, SAP_SSH_PORT, SAP_SSH_USER, SAP_SSH_PASSWORD


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-t', dest="types", required=True, nargs="+", choices=[SOAP,WEBDYNPROS,PORTALAPPS,SERVLETS,ALL], help="Indicates what type of webapps should be analyzed/extracted")
    parser.add_argument('-d', dest="files_directory", default= DIR_RESULTS, help="Directory where all config files will be/were extracted")
    parser.add_argument('--extract', dest="extract", action="store_true", help="Indicates that config files should be extracted")
    args = parser.parse_args()

    if args.extract:

        if not (SAP_HOST or SAP_SSH_PORT or SAP_INSTANCE or SAP_SID or SAP_SSH_USER):
            print("[-] Error: host, port, instance, sid and user are required to extract data. Complete the sap_config.py file.")
            exit(1)

        cfe = ConfigFileExtractor(SAP_HOST,
                                  SAP_SSH_PORT,
                                  SAP_INSTANCE,
                                  SAP_SID,
                                  SAP_SSH_USER,
                                  SAP_SSH_PASSWORD,
                                  args.files_directory)

        print(f"[+] Extracting {', '.join(args.types)} config files...")
        if SOAP in args.types or ALL in args.types:
            cfe.extract_soap_files()
        if SERVLETS in args.types or ALL in args.types:
            cfe.extract_servlets_files()
        if WEBDYNPROS in args.types or ALL in args.types:
            cfe.extract_webdynpros_files()
        if PORTALAPPS in args.types or ALL in args.types:
            cfe.extract_portalapps_files()
    else:
        print("[*] Skipping config files extraction...")


    print("\n[+] Analyzing endpoints...")
    files_dir = f"{args.files_directory}/{SAP_HOST}" if args.extract else args.files_directory
    ea = EndpointAnalyzer(files_dir)   
    endpoints = dict()

    if SOAP in args.types or ALL in args.types:
        endpoints.update({SOAP: ea.analyze_soap()})
    if SERVLETS in args.types or ALL in args.types:
        endpoints.update({SERVLETS: ea.analyze_servlets()})
    if WEBDYNPROS in args.types or ALL in args.types:
        endpoints.update({WEBDYNPROS: ea.analyze_webdynpros()})
    if PORTALAPPS in args.types or ALL in args.types:
        endpoints.update({PORTALAPPS: ea.analyze_portalapps()})

    
    print(f"\n[+] Saving endpoints to \"{OUTPUT_ENDPOINTS_FILE}\" file...", end="")
    with open(OUTPUT_ENDPOINTS_FILE, 'w') as f:
        json.dump(endpoints, f, indent=4)
    print(f" Done!")




    
        












    

