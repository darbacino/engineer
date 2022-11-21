""" There will be methods connected with connecting to VM and Make there changes or only execute on there changes 
"""
import re
import subprocess
import json
import os
import sys


class ConnectionSetup:
    def connect_vm_via_ssh(self, user:str, host:str, password:str, cmd:str):
        """_summary_

        Args:
            user (str): vm name
            host (str): address ip
            cmd (str): command

        Returns:
            PIPE: opened pipe to communicate via ssh 
        """
        
        return subprocess.Popen(f'sshpass -p "{password}" ssh {user}@{host} {cmd}', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

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
    
    def get_generated_data(self):
        pass
        # print(data)
        # # out = os.system(f"ping -c 2 {ip}")
        
        # # print('here')
        # # print(os.system(f"ping -c 2 {ip}"))
        # # print('endHere')
        # # print(os.system(f"ping -c 1 {ip}" + ("-n 1 " if  sys.platform().lower()=="win32" else "-c 1 ") + ip))
        
        