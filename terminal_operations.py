import subprocess

class Terminal:
    def __init__(self) -> None:
        # print('OLA')
        pass
        # pass
        
    def connect_vm_via_ssh(self, user:str, host:str, cmd:str):
        """_summary_

        Args:
            user (str): vm name
            host (str): address ip
            cmd (str): command

        Returns:
            PIPE: opened pipe to communicate via ssh 
        """
        
        # return subprocess.Popen(f'ssh {user}@{host} {cmd}', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        return subprocess.Popen(f'{cmd}', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

    def terminal(self,command):
        """_summary_

        Args:
            command (str): command

        Returns:
            PIPE: opened pipe to communicate 
        """
        
        # return subprocess.Popen(f'ssh {user}@{host} {cmd}', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        return subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

