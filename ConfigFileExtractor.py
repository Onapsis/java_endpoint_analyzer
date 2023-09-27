import os
import os.path
import random
import string

from paramiko import SSHClient, AutoAddPolicy, ssh_exception
from lib.constants import (SAP_APPS_DIR, CREATE_TEMP_DIR_CMD, SCRIPT_PATH, DIR_RESULTS,
                       SOAP_CONFIG_COMMAND_EXTRACT, SOAP_DIR_RESULTS, SOAP_ERROR1, SOAP_ERROR2,
                       WEBDYNPRO_CONFIG_COMMAND_EXTRACT, WEBDYNPRO_DIR_RESULTS, SERVLETS_WEBXML_COMMAND_EXTRACT,
                       SERVLETS_DIR_RESULTS, PORTALAPP_CONFIG_COMMAND_EXTRACT, PORTALAPP_DIR_RESULTS, 
                       SOAP_FILETYPE, WEBDYNPRO_FILETYPE, SERVLETS_FILETYPE, PORTALAPP_FILETYPE, DASH_NUMBER_LINE)


class ErrorInOSCmdException(Exception):pass

class ConfigFileExtractor:
    def __init__(self, host, port, instance, sid, user, password=None, out_dir=DIR_RESULTS):
        self.host = host
        self.port = port
        self.sid = sid
        self.instance = instance
        self.user = user
        self.password = password
        self.out_dir = out_dir
        self._connect()

    def _execute_cmd(self, cmd):
        stdin, stdout, stderr = self.client.exec_command(cmd)
        error = stderr.read()
        if error != b"":
            raise ErrorInOSCmdException(f"Error trying to execute command \"{cmd}\": {error}")
        return stdout.read()

    def _connect(self):
        print(f"[+] Trying to connect to {self.host} with user {self.user}...",end="")
        self.client = SSHClient()
        self.client.set_missing_host_key_policy(AutoAddPolicy())
        self.client.load_system_host_keys()
        
        try:
            if self.password:
                self.client.connect(self.host, 
                            port=self.port,
                            username=self.user,
                            password=self.password,
                            allow_agent=False,
                            look_for_keys=False)
            else:
                self.client.connect(self.host,
                                port=self.port,
                                username=self.user,
                                password=self.password)
                
        except ssh_exception.AuthenticationException:  
            print(f"\n[-] SSH authentication failed. Review the SSH user/password combination is correct and retry.")
            exit(1)

    def _copy_command_to_script(self, cmd):
        ftp = self.client.open_sftp()
        file = ftp.file(SCRIPT_PATH, "w")
        file.chmod(0o755)
        file.write(cmd)
        file.flush()
        ftp.close()

    def _copy_dir(self, remote_source_dir, local_dest_dir):
        full_path_local_dest_dir = f"{self.out_dir}/{self.host}/{local_dest_dir}"
        if not os.path.exists(full_path_local_dest_dir):
            os.makedirs(full_path_local_dest_dir)

        ftp = self.client.open_sftp()
        out = self._execute_cmd(f"ls {remote_source_dir}")
        filenames = out.decode('ascii').split('\n')
        for filename in filenames:
            if filename != "":
                ftp.get(f"{remote_source_dir}/{filename}", f"{full_path_local_dest_dir}/{filename}")
        ftp.close()

    def _extract_config_files(self, filetype, command, dest_dir_results):
        print(f"\t[+] Extracting {filetype} files")
        try:
            random_dir_path = "/tmp/" + "".join([random.choice(string.ascii_lowercase) for i in range(10)])
            app_dir = SAP_APPS_DIR.format(sid=self.sid, instance=self.instance)
            print(f"\t\t[+] Checking if apps dir is reachable..")
            out = self._execute_cmd(f"ls {app_dir}")

            print(f"\t\t[+] Creating directory {random_dir_path}")
            self._execute_cmd(CREATE_TEMP_DIR_CMD.format(random_dir_path))

            print(f"\t\t[+] Copying script file")
            self._copy_command_to_script(command.format(sap_apps_dir=app_dir, random_dir_path=random_dir_path))
            
            print(f"\t\t[+] Executing script/command (this could take a few mins)")
            self._execute_cmd(SCRIPT_PATH)

            print(f"\t\t[+] Copying all config files to this machine.")
            self._copy_dir(random_dir_path, dest_dir_results)

        except Exception as e: 
            raise e

        finally:
            print(f"\t\t[+] Deleting script and random dir in server..")
            self._execute_cmd(f'rm -r {SCRIPT_PATH} {random_dir_path}')
            print(f"\t\t[+] Done!")


    def extract_soap_files(self):
        try: 
            self._extract_config_files(SOAP_FILETYPE,SOAP_CONFIG_COMMAND_EXTRACT, SOAP_DIR_RESULTS)
        except ErrorInOSCmdException as e:
            if SOAP_ERROR1 in str(e) and SOAP_ERROR2 in str(e):
                print("\t\t[W] Servlet error found. Trying with command modification. ")
                new_cmd = SOAP_CONFIG_COMMAND_EXTRACT.replace("-f 2","-f 1")
                self._extract_config_files(SOAP_FILETYPE,new_cmd, SOAP_DIR_RESULTS)
            else: 
                raise e

    def extract_webdynpros_files(self):
        self._extract_config_files(WEBDYNPRO_FILETYPE,WEBDYNPRO_CONFIG_COMMAND_EXTRACT, WEBDYNPRO_DIR_RESULTS)
    
    def extract_portalapps_files(self):
        self._extract_config_files(PORTALAPP_FILETYPE,PORTALAPP_CONFIG_COMMAND_EXTRACT, PORTALAPP_DIR_RESULTS)

    def extract_servlets_files(self):
        self._extract_config_files(SERVLETS_FILETYPE,SERVLETS_WEBXML_COMMAND_EXTRACT, SERVLETS_DIR_RESULTS)

        
