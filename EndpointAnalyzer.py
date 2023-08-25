from analyzers.soap.SOAPEndpointAnalyzer import SOAPEndpointAnalyzer
from analyzers.webdynpros.WDEndpointAnalyzer import WDEndpointAnalyzer
from analyzers.portalapps.PortalAppEndpointAnalyzer import PortalAppEndpointAnalyzer
from analyzers.servlets.ServletEndpointAnalyzer import ServletEndpointAnalyzer
from lib.constants import (SOAP_DIR_RESULTS, WEBDYNPRO_DIR_RESULTS, SERVLETS_DIR_RESULTS,
                       PORTALAPP_DIR_RESULTS, SOAP, SERVLETS, WEBDYNPROS, PORTALAPPS)

class EndpointAnalyzer:
    def __init__(self, results_directory):
        self.results_directory = results_directory

    def analyze_soap(self):
        see = SOAPEndpointAnalyzer()
        print(f"\t[+] Analyzing {SOAP} endpoints... ",end="")
        endpoints = see.analyze(f"{self.results_directory}/{SOAP_DIR_RESULTS}")
        print("Done!")
        return endpoints
    
    
    def analyze_servlets(self):
        svee = ServletEndpointAnalyzer()
        print(f"\t[+] Analyzing {SERVLETS} endpoints... ",end="")
        endpoints = svee.analyze(f"{self.results_directory}/{SERVLETS_DIR_RESULTS}")
        print("Done!")
        return endpoints
    
    def analyze_webdynpros(self):
        wdee = WDEndpointAnalyzer()
        print(f"\t[+] Analyzing {WEBDYNPROS} endpoints... ",end="")
        endpoints = wdee.analyze(f"{self.results_directory}/{WEBDYNPRO_DIR_RESULTS}")
        print("Done!")
        return endpoints
    
    def analyze_portalapps(self):
        pee = PortalAppEndpointAnalyzer()
        print(f"\t[+] Analyzing {PORTALAPPS} endpoints... ",end="")
        endpoints = pee.analyze(f"{self.results_directory}/{PORTALAPP_DIR_RESULTS}")
        print("Done!")
        return endpoints
    

