""" There will be methods connected with connecting to VM and Make there changes or only execute on there changes 
"""
import re, vars, subprocess, json, os
from datetime import datetime


class Connection:
    def connect_vm_via_sshkey(self, user: str, host: str, cmd: str):
        """Execute command by SSH Key

        Args:
            user (str):         Device username
            host (str):         Device IP
            cmd (str):          Command with will be executed

        Returns:
            str: Opened pipe to communicate, resoult or error information
        """
        return subprocess.Popen(
            f"ssh {user}@{host} {cmd}",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ).communicate()

    def connect_vm_via_ssh(self, user: str, host: str, password: str, cmd: str):
        """Execute command by SSH

        Args:
            user (str):         Device username
            host (str):         Device IP
            password (str):     Device password
            cmd (str):          Command with will be executed

        Returns:
            str: Opened pipe to communicate, resoult or error information
        """

        return subprocess.Popen(
            f'sshpass -p "{password}" ssh {user}@{host} {cmd}',
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ).communicate()

    def terminal(self, command: str):
        """Execute command

        Args:
            command (str): Command to execute

        Returns:
            PIPE: opened pipe to communicate
        """

        return subprocess.Popen(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        ).communicate()

    def scp_via_sshkey(
        self, user: str, host: str, ssh_key_path: str, server_path: str, local_path: str
    ):
        """Method to copy by SCP by SSH Key

        Args:
            user (str):         Device username
            host (str):         Device IP
            cmd (str):          Command with will be executed
            ssh_key_path (str): Path to SSH Key
            server_path (str):  Path to file
            local_path (str):   Path on local device to save

        Returns:
            str: Opened pipe to communicate, resoult or error information
        """
        return subprocess.Popen(
            f"scp -i {ssh_key_path} {user}@{host}:{server_path} {local_path}",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ).communicate()


class DevOperations:
    """Operations on devices"""

    def __init__(self) -> None:
        """Operations on devices

        Args:
            retries (int, optional): _description_. Defaults to 2.
        """
        self.__connect = Connection()
        self.__config = self.__get_config_from_yaml()

    def __test_connection(self, ip: str):
        """Check connection with device

        Args:
            ip (str): Device IP address

        Returns:
            bool: True - device avaliable, False - notavaliable
        """
        ping_command = f"ping -c 2 {ip}"
        regex_expression = r", \d+ received"

        data = self.__connect.terminal(ping_command)[0].decode()
        data = re.search(regex_expression, data).group(0)

        if "0" in re.findall(r"[0-9]", data):
            return False
        return True

    def get_current_date(self):
        """Current date in format ex. 2000_12_31_24_60_60
                                         %Y_%m_%d_%H_%M_%S

        Returns:
            str: Current date
        """
        return datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

    def __get_config_from_yaml(self):
        """Get configuration from json file

        Returns:
            dict: Default configuration
        """
        if not os.path.exists(vars.PATH_CONFIG):
            print("\nProblem with configuration file. Exit")
            exit(2)

        with open(vars.PATH_CONFIG) as json_data:

            return json.load(json_data)

    def get_config(self):
        """Get configuration from json file

        Returns:
            dict: Default configuration
        """

        return self.__config

    def get_task_config(self, task_name: str):
        """Search in config for task

        Args:
            task_name (str): Name of task

        Returns:
            dict: Configuration for specific task
        """
        for settings in self.__config["task"]:
            if settings["name"] == task_name:

                return settings

    def __check_devices_avalibility(self):
        """Ping all devices that are in configuration"""
        print("Checking availability devices")

        for dev in self.__config["dev"]:
            avaliable = self.__test_connection(dev["ip"])

            if not avaliable:
                print(f"  Not avaiable {dev} ")
                exit(3)
            else:
                print(f'  {dev["ip"]} - {avaliable}')

    def __prepare_dir(self):
        """Prepare dir, remove if exist"""
        print("Removing old data on devices")
        command = f"'rm -drf {vars.PATH_DATA_FOLDER} *.zip 2> /dev/null ; mkdir {vars.PATH_DATA_FOLDER}'"

        for dev in self.__config["dev"]:
            self.__connect.connect_vm_via_sshkey(
                cmd=command, host=dev["ip"], user=dev["name"]
            )

    def __get_data_from_devices(self):
        """Zip and get data from devices"""
        print("Getting data from devices")

        for dev in self.__config["dev"]:
            zip_name = (
                f"{vars.ZIP_FILE_NAME}{dev['name']}_{self.get_current_date()}.zip"
            )
            command_create_zip = f"zip -r {zip_name} {vars.PATH_DATA_FOLDER}"

            # Zip data on device
            self.__connect.connect_vm_via_sshkey(
                cmd=command_create_zip, host=dev["ip"], user=dev["name"]
            )

            # Copy from device zip
            self.__connect.scp_via_sshkey(
                user=dev["name"],
                host=dev["ip"],
                ssh_key_path=dev["sshkeypath"],
                server_path=f"{zip_name}",
                local_path=vars.PATH_LOCAL_DIR_WITH_EXPERIMENTS,
            )
        print("Taking data from devices")

    def check_and_prepare_devices(self):
        self.__check_devices_avalibility()
        self.__prepare_dir()

    def get_data_from_devices(self):
        self.__get_data_from_devices()
