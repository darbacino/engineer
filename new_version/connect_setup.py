""" There will be methods connected with connecting to VM and Make there changes or only execute on there changes 
"""
import re,vars
import subprocess
import json
import os
import sys
from datetime import datetime


class ConnectionSetup:
    def connect_vm_via_sshkey(self, user:str, host:str, cmd:str):

        return subprocess.Popen(f'ssh {user}@{host} {cmd}', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    
    # def prepare_dir_by_ssh(self, user:str, host:str):
    #     cmd = "mkdir 'experiments_data'"
    #     self.connect_vm_via_sshkey(user, host, cmd)
        
    def connect_vm_via_ssh(self, user:str, host:str, password:str, cmd:str):
        """_summary_

        Args:
            user (str): vm name
            host (str): address ip
            cmd (str): command

        Returns:
            PIPE: opened pipe to communicate via ssh 
        """
        # print(f'sshpass -p "{password}" ssh {user}@{host} {cmd}')
        return subprocess.Popen(f'sshpass -p "{password}" ssh {user}@{host} {cmd}', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    def mkdir_in_device(self):
        self.connect_vm_via_sshkey(
            
        )
    def ssh_terminal(self,command:str):
        """_summary_

        Args:
            command (str): command

        Returns:
            PIPE: opened pipe to communicate 
        """
        
        # return subprocess.Popen(f'ssh {user}@{host} {cmd}', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        return subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    
    def get_config(self, json_file:str):
        if not os.path.exists(json_file):
            print("\nProblem with configuration file. Exit")
            exit(2)

        with open(json_file) as json_data:
            
            return json.load(json_data)
    def get_task(self, config, task_name):
        for settings in config['task']:
            if settings["name"] == task_name:
                return settings
                
    def test_connection(self, ip:str):
        data = self.ssh_terminal(f"ping -c 2 {ip}")[0].decode()
        data = re.search(r", \d+ received", data).group(0)
        if "0" in re.findall(r"[0-9]",data):
            return False
        return True
    
    def get_current_data(self):
        return datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    def scp_via_sshkey(self, user:str, host:str, ssh_key_path:str, server_path:str, local_path:str):
        """_summary_

        Args:
            user (str): _description_
            host (str): _description_
            cmd (str): _description_
            ssh_key_path (str): _description_
            server_path (str): path to file with will be copied
            local_path (str): path on local device where to save

        Returns:
            _type_: _description_
        """
        return subprocess.Popen(f'scp -i {ssh_key_path} {user}@{host}:{server_path} {local_path}', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

class PrepareDevices:   
    __connection_setup = ConnectionSetup()
    __configuration = __connection_setup.get_config(vars.PATH_CONFIG)
    
    def __init__(self, retries=2, cleanup = False) -> None:
        self.__retries = retries
        self.__cleanup = cleanup

    def __check_devices_avalibility(self):
        print("Checking availability devices")
        for dev in self.__configuration["dev"]:
            avaliable = self.__connection_setup.test_connection(dev["ip"])
            print(f'{dev["ip"]} - {avaliable}')
            
            if not avaliable:
                print(f"Not avaiable {dev} ")
                exit(3)

    def __prepare_dir(self):
        """Prepare dir, remove if exist
        """
        print("Removing old data on devices")
        command = f"'rm -drf {vars.PATH_DATA_FOLDER} 2> /dev/null ; mkdir {vars.PATH_DATA_FOLDER}'"
        # command = f"'rm -drf {vars.PATH_DATA_FOLDER}  ; mkdir {vars.PATH_DATA_FOLDER}'"
        # print(f"prepare dir {command}")
        for dev in self.__configuration["dev"]:
            # print(f'prepare_dir : {self.__connection_setup.connect_vm_via_sshkey(cmd = command,host=dev["ip"],user=dev["name"])}')
            self.__connection_setup.connect_vm_via_sshkey(cmd = command,host=dev["ip"],user=dev["name"])
            #remove and create
            
        # print("Preparing directory connection")
        
    def __get_data_from_dir(self):
        """It will take data and remove old
        """
        
        print("Getting data from ALL devices")
    
        for dev in self.__configuration["dev"]:
            zip_name = f"{vars.ZIP_FILE_NAME}{dev['name']}_{self.__connection_setup.get_current_data()}.zip"
            command_create_zip  = f"zip -r {zip_name} {vars.PATH_DATA_FOLDER}"
            self.__connection_setup.connect_vm_via_sshkey(
                cmd = command_create_zip,
                host=dev["ip"],
                user=dev["name"]
            )

            self.__connection_setup.scp_via_sshkey(
                user=dev["name"], 
                host=dev["ip"], 
                ssh_key_path=dev["sshkeypath"], 
                server_path=f"{vars.PATH_TO_ZIP}{zip_name}", 
                local_path=vars.PATH_LOCAL_DIR_WITH_EXPERIMENTS
            )
        print("Taking data from devices")
        
    def start(self):
        if self.__cleanup:
            self.__check_devices_avalibility()
            self.__prepare_dir()
        else:
            self.__get_data_from_dir()
        