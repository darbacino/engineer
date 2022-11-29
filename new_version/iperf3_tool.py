from connect_setup import ConnectionSetup
import vars, time, os
from multiprocessing import Process
from itertools import count
class Iperf3Tool:
    
    # __file_name =  vars.PATH_DATA_FOLDER + (__task_conf['output_file_name'] if __task_conf['output_file_name'] != "" else __task_conf["name"])
    # __tool_data_dir = f"{vars.PATH_DATA_FOLDER}_{__task_name}_{__connection_setup.get_current_data()}"
    def __init__(self) -> None:
        self.__connection_setup = ConnectionSetup()
        self.__configuration = self.__connection_setup.get_config(vars.PATH_CONFIG)
        self.__task_name = "iperf3"
        self.__server_ip = ""
        self. __task_conf = self.__connection_setup.get_task(self.__configuration, self.__task_name)

  
    def __run_command_on_server(self, command: str):
        for device in self.__configuration["dev"]:
            if device["type"] == "server":
                self.__server_ip = device["ip"]

                return self.__connection_setup.connect_vm_via_sshkey(
                    cmd=command,
                    host=device["ip"],
                    user=device["name"],
                )

    def __run_command_on_client(self, command:str):
        list_with_clients = []

        for device in self.__configuration["dev"]:
            if device["type"] == "client":
                list_with_clients.append(
                    self.__connection_setup.connect_vm_via_sshkey(
                        cmd=command,
                        host=device["ip"],
                        user=device["name"],
                    )
                )

        return list_with_clients
                
    def __run_server(self):
        command = f"iperf3 -s -1 -J --logfile {self.__tool_data_dir}/parallel_{self.__task_conf['parallel']}_{self.__connection_setup.get_current_data()}"
        # print(command)
        # command = "iperf3 -s "
        
        return self.__run_command_on_server(command)
    
    def __run_client(self):
        
        # print(self.__file_name)
        command = f"iperf3 --parallel {self.__task_conf['parallel']} -c {self.__server_ip} -t {self.__task_conf['transsmision_time']} -J --logfile {self.__tool_data_dir}/parallel_{self.__task_conf['parallel']}_{self.__connection_setup.get_current_data()}"
        # print(command)
        return self.__run_command_on_client(command)
        
    def __update_parallel(self):
        if self.__task_conf["parallel"] <= self.__task_conf["parallel_end"]:
            self.__task_conf["parallel"] += 1

    def create_dir_for_tool(self):
        self.__tool_data_dir = f"{vars.PATH_DATA_FOLDER}{self.__task_name}_{self.__connection_setup.get_current_data()}"
        create_dir_command = f"mkdir {self.__tool_data_dir}"
        # print(create_dir_command)
        self.__run_command_on_server(create_dir_command)
        self.__run_command_on_client(create_dir_command)
        
    def __timeout_of_funcion(self, t_func, retry = 5, func_timeout = 3):
        
        for _ in range(retry):
            p1 = Process(target=t_func)
            p1.start()
            p1.join(timeout=5)
            p1.terminate()
 
            if p1.exitcode == 0:
                return
        

    def start(self):
        # while self.__task_conf['repeats']: #num of repeats
        # folder dla wszystkich runow z tego taska 
        # potem w tym zbieramy kazdy plik z data jako jego nazwa 

        self.create_dir_for_tool()
        while self.__task_conf["parallel"] <= self.__task_conf["parallel_end"]:
            print(f'running parallel nr -- {self.__task_conf["parallel"]}')
            
            running_server  = self.__timeout_of_funcion(self.__run_server)
            
            # print(f"server -- {running_server}")
            running_clients = self.__run_client()
            # print(f"client -- {running_clients}")
            
            self.__update_parallel()
        
        # print("Generate graph")
        # for el in self.__run_plotter():
        #     print(el.decode())


        # self._run_operations("dict_with_clients")

    # mamy przygotowane miejsce teraz postawic server aby funcja odpalala server i do zmiennej

    # connect and set server and client
    # run operation
    # get data
    # close server and client 
    
    #TODO PREPARE THAT ON THIRD VM



#TODO Prepare that like it is separated class that  have methods that we will use to iperf3