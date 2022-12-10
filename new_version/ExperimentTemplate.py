from connect_setup import *
import vars
from multiprocessing import Process
from itertools import count


class ExperimentTemplate:
    """How to:
    In configuration.json need to be defined devices as in example and task.
    It's important to correctly prepare start and end variable that changes in config
    ex. parallel, parallel_end from 1 to 10. and that name need to be send int  ExpermitentTempalte("task_name_in_config", "var_where_we_start", "var_where_we_end")
    """
    def __init__(self, task_name, name_of_testing_parameter, name_of_testing_parameter_end) -> None:
        self._connect   = Connection()
        self._dev_op    = DevOperations()
        self._config    = self._dev_op.get_config()
        self._task_name = task_name
        self._task_conf = self._dev_op.get_task_config(self._task_name)

        self._name_of_testing_parameter = name_of_testing_parameter
        self._name_of_testing_parameter_end = name_of_testing_parameter_end
        self._tool_data_dir = f"{vars.PATH_DATA_FOLDER}{self._task_name}_{self._dev_op.get_current_date()}"
        self.__time_out = 3
        self.__retry = 5
        
    def _run_command_on_servers(self, command: str):
        """Run command on servers from config

        Args:
            command (str): command with will be executed

        Returns:
            list: That list contain connection and output from terminal
        """
        list_of_servers = []

        for device in self._config["dev"]:
            if device["type"] == "server":

                list_of_servers.append(
                    self._connect.connect_vm_via_sshkey(
                        cmd=command,
                        host=device["ip"],
                        user=device["name"],
                    )
                )

        return list_of_servers

    def _run_command_on_clients(self, command: str):
        """Run command on client from config

        Args:
            command (str): command with will be executed

        Returns:
            list: That list contain connection and output from terminal
        """
        list_with_clients = []

        for device in self._config["dev"]:
            if device["type"] == "client":
                list_with_clients.append(
                    self._connect.connect_vm_via_sshkey(
                        cmd=command,
                        host=device["ip"],
                        user=device["name"],
                    )
                )

        return list_with_clients

    def _set_clients_command(self,command):
        self.__client_command = command

    def _set_servers_command(self,command):
        self.__servers_command = command
    
    def _get_logfile_path_and_name(self):
        """Prepare dir and name of file.
        Returns:
            str: dir with name of logfile
        """
        
        # self._tool_data_dir - give path to folder where should be changes
        # self._name_of_testing_parameter - what part of config we are changing (ex. parallel)
        # self._task_conf['parallel'] - current value of variable that changes in config
        
        return f"{self._tool_data_dir}/{self._name_of_testing_parameter}_{self._task_conf[self._name_of_testing_parameter]}_{self._dev_op.get_current_date()}"
    
    def _run_servers(self):
        """That method will run prepared command on only server

        Returns:
            list: That list contain connection and output from terminal
        """
 
        return self._run_command_on_servers(self.__servers_command)

    def _run_clients(self):
        """That method will run prepared command on only clients

        Returns:
            list: That list contain connection and output from terminal
        """

        return self._run_command_on_clients(self.__client_command)

    def _update_config(self, name_of_var: str):
        """Update variable in config. That method is for updating settings on devices with will give diffrent output.
        Ex. Parralel
        """

        self._task_conf[name_of_var] += self._task_conf["counter"]

    def _run_command_on_all_dev(self, command):
        """Run given command on all devices from configuration

        Args:
            command (str): command that will be executed on all devices

        Returns:
            list: That list contain connection and output from terminal
        """
        devices = []
        
        for device in self._config["dev"]:
            devices.append(
                self._connect.connect_vm_via_sshkey(
                    cmd=command,
                    host=device["ip"],
                    user=device["name"],
                )
            )

        return devices

    def _create_dir_for_tool(self):
        """Prepare specific directory for tool

        Returns:
            list: That list contain connection and output from terminal
        """
        
        create_dir_command = f"mkdir {self._tool_data_dir}"

        return self._run_command_on_all_dev(create_dir_command)

    def _set_timeout_time(self, timeout:int = 3):
        self.__time_out = timeout

    def _set_retry_in_timeout_func(self, retry:int = 5):
        self.__retry = retry

    def _timeout_of_funcion(self, reference_to_func):
        """Set timeout and number of retry for funcion

        Args:
            reference_to_func (func): name_of_funcion without "()"
            retry (int, optional): Number of attempts. Defaults to 5.
            func_timeout (int, optional): max time for funcion to finish. Defaults to 3.
        """
        for _ in range(self.__retry):
            proc = Process(target=reference_to_func)
            proc.start()
            proc.join(timeout=self.__time_out)
            proc.terminate()

            # if finished in expect time
            if proc.exitcode == 0:
                return

    def _execute_on_devices(self):
        pass
    
    def _run(self):
        default_start = self._task_conf[self._name_of_testing_parameter]
        
        for repeat in range(self._task_conf["repeats"]):
            self._task_conf[self._name_of_testing_parameter] = default_start
            
            if repeat > 0:
                print(f"Repeat nr. {repeat+1}")

            self._create_dir_for_tool()

            while self._task_conf[self._name_of_testing_parameter] <= self._task_conf[self._name_of_testing_parameter_end]:
                print(f'{self._name_of_testing_parameter}: {self._task_conf[self._name_of_testing_parameter]}')

                self._execute_on_devices()
                self._update_config(self._name_of_testing_parameter)
    
    def start(self):
        raise ("Not implemented")
        

class Iperf3Parallel(ExperimentTemplate):
    def __init__(self) -> None:
        super().__init__(
            task_name="iperf3", 
            name_of_testing_parameter="parallel", 
            name_of_testing_parameter_end="parallel_end"
            )

    def _execute_on_devices(self):
        s_cmd = f"iperf3 -s -1 -J --logfile {self._get_logfile_path_and_name()}"
        c_cmd = f"iperf3 --parallel {self._task_conf['parallel']} -c {self.__get_server_ip()} -t {self._task_conf['transsmision_time']} -J --logfile {self._get_logfile_path_and_name()}"
        self._set_servers_command(s_cmd)
        self._set_clients_command(c_cmd)
        
        self._timeout_of_funcion(self._run_servers)
        self._run_clients()

    def __get_server_ip(self):
        for device in self._config["dev"]:
            if device["type"] == "server":
                return device["ip"]

    def start(self):
        self._run()

class PingTask(ExperimentTemplate):
    def __init__(self) -> None:
        task_name = "ping"
        name_of_testing_parameter = "transsmision_count"
        name_of_testing_parameter_end = "transsmision_count_end"
        super().__init__(task_name, name_of_testing_parameter, name_of_testing_parameter_end)
        
    def _execute_on_devices(self):
        c_cmd = f"'ping -c{self._task_conf['transsmision_count']} {self.__get_server_ip()} > {self._get_logfile_path_and_name()}'"

        self._set_clients_command(c_cmd)
        self._run_clients()
        
    def __get_server_ip(self):
        for device in self._config["dev"]:
            if device["type"] == "server":
                return device["ip"]
        
    def start(self):
        self._run()

        
        
        
        
        
        
        
        
   