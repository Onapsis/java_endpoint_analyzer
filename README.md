# Java Endpoint Analyzer

# Introduction and goal 
Java Endpoint Analyzer (JEA) helps you assess the scope of an SAP system based on Java in order to understand which HTTP endpoints are exposed. To do so, it automatically analyzes deployment files (like web.xml, webdympro.xml , portalapp.xml) in order to extract out the URLs (endpoints) that the system has. It is meant to be used internally as OS credentials are needed. 

It currently works with the following type of applications:
- Servlets
- SOAP Applications
- Portal Apps
- Webdynpros

# How does it works

JEA requires credentials of the target SAP system in order to log in through SSH and download specific files. These files are deployment configuration files that each type of webapp uses. Once they are downloaded locally, the analysis phase of the process begins. Every file is parsed and based on what those files state, the entry points are built. 

The output of this tool will be an endpoints.json file holding all found HTTP endpoints of the java system. 

# Installation
This tool uses Python >= 3.8 

Install the necessary dependencies with: 

```bash
pip install -r requirements.txt
```

# Usage

JEA can be used in two different modes: 
- Extraction + Analysis 
- Analysis Only  

The final list of endpoints will be stored in the CWD inside a file named "endpoints.json"

## Extraction + Analysis

Under this mode, JEA will connect to the SAP system, download deployment files of the types specified and later extract the endpoints from them.

There are three main arguments to be used in this situation: 
* **--extract**: Specifies that extraction of files should occur.
* **-t**: Specifies which type of webapps are going to be downloaded/analyzed 
* **-d**: Specifies the path to the directory where all extracted files will be stored.

Due to extraction being activated, information and credentials of the targeted SAP system must be provided. This information is gathered from *system_config.py* file. You must create this file filling the necessary data. A template file called *system_config.py.template* can be found in the main directory of the repository. Feel free to make a copy of that file and start completing the necessary data. 

SAP's required information for extraction (*system_config.py*):
* **SAP_HOST**: Destination. SAP server's host. 
* **SAP_INSTANCE**: Instance number of the targeted instance.
* **SAP_SID**: SID. SAP's SID.
* **SAP_SSH_PORT**: SSH port. Default: 22.
* **SAP_SSH_USER**: SSH user. 
* **SAP_SSH_PASSWORD**: SSH password (if needed). You can avoid using it if your OS user have already configured the SSH connection to that server through certs.

## Analysis only

If you already executed the extraction phase and you want to re-analyze the deployment files without extracting again, this mode should be used. 
Similar to the previous case, the following parameters should be used: 
* **-t**: Specifies which type of webapps are going to be downloaded/analyzed 
* **-d**: Specifies the path to the directory where the extracted files were stored. IMPORTANT: Consider that while doing an extraction, JEA automatically creates a directory inside the provided output directory with the name of the host (for organization purposes). In this case, you should provide the full path to that directory (including the host name).

# Examples


## Extract and analyze SOAP files using SSH Certs for connection.
Retrieve endpoints from SOAP webapps from system saplab.test.com (DEV) instance 00. Having already a trust SSH connection

*system_config.py*
```python   
SAP_HOST = "saplab.test.com"
SAP_INSTANCE = "00"
SAP_SID = "DEV"
SAP_SSH_PORT =  22
SAP_SSH_USER =  "devadm"
SAP_SSH_PASSWORD = ""
```

```bash
python jea.py --extract -t SOAP -d results
```

## Extract and analyze ALL files using SSH password for connection.
Retrieve endpoints from ALL possible webapps from system saplab.test.com (DEV) instance 95 using "devadm:ILoveSAP1234." as credentials. 
*system_config.py*
```python   
SAP_HOST = "saplab.test.com"
SAP_INSTANCE = "95"
SAP_SID = "DEV"
SAP_SSH_PORT =  22
SAP_SSH_USER =  "devadm"
SAP_SSH_PASSWORD = "ILoveSAP1234."
```

```bash
python jea.py --extract -t ALL -d results
```

## Only analyze WEBDYNPROS files
Retrieve endpoints from WEBDYNPROS webapps. Results of extraction from saplab.test.com were placed under directory "/tmp/jea_extraction". 
```bash
python jea.py -t WEBDYNPROS -d /tmp/jea_extraction/saplab.test.com
```




