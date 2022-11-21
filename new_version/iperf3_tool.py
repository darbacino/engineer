from connect_setup import ConnectionSetup
import vars, time, os


class Iperf3Tool:
    __connection_setup = ConnectionSetup()
    __configuration = __connection_setup.get_config(vars.PATH_CONFIG)
    __task_name = "iperf3"
    __server_ip = ""
    __task_conf = __connection_setup.get_task(__configuration, __task_name)

    def __init__(self) -> None:
        self.__check_devices_avalibility()
        print("Running Iperf3")

    def __check_devices_avalibility(self):
        for dev in self.__configuration["dev"]:
            avaliable = self.__connection_setup.test_connection(dev["ip"])
            print(f'{dev["ip"]} - {avaliable}')
            if not avaliable:
                print(f"Not avaiable {dev} ")
                exit(3)

    def __clear_screen(self):

        os.system('cls' if os.name == 'nt' else 'clear')
        
    def __run_command_on_server(self, command: str):
        for device in self.__configuration["dev"]:
            if device["type"] == "server":
                self.__server_ip = device["ip"]

                return self.__connection_setup.connect_vm_via_ssh(
                    cmd=command,
                    host=device["ip"],
                    user=device["name"],
                    password=device["password"],
                )

    def __run_command_on_clients(self, command:str):
        list_with_clients = []

        for device in self.__configuration["dev"]:
            if device["type"] == "client":
                list_with_clients.append(
                    self.__connection_setup.connect_vm_via_ssh(
                        cmd=command,
                        host=device["ip"],
                        user=device["name"],
                        password=device["password"],
                    )
                )

        return list_with_clients
                
    def __run_server(self):
        command = "iperf3 -s --logfile DATA_TEST"
        
        return self.__run_command_on_server(command)
    
    def __run_client(self):
        command = f"iperf3 --parallel {self.__task_conf['parallel']} -c {self.__server_ip} -t {self.__task_conf['client_timeout']} --logfile {self.__task_conf['output_file_name']}"
        
        return self.__run_command_on_clients(command)
        

    def __update_parallel(self):
        if self.__task_conf["parallel"] <= self.__task_conf["parallel_end"]:
            self.__task_conf["parallel"] += 1
            # self.__task_conf["parallel"] = f'{self.__task_conf["parallel"]}_self.__task_conf["parallel"]'
            

    def __get_output_file(self):
        get_files_command = ""
        get_file_command2 = f"cat {self.__task_conf['output_file_name']} > {self.__task_conf['output_file_name']}"
        get_file_command = f"ls > {self.__task_conf['output_file_name']}"
        self.__run_command_on_clients(get_file_command2)
        

    def start(self):
        # while self.__task_conf['repeats']: #num of repeats
        while self.__task_conf["parallel"] <= self.__task_conf["parallel_end"]:
            
            print("Starting server")
            running_server = self.__run_server()
            print("Server prepared")
            
            print("Starting client")
            running_clients = self.__run_client()
            print("Client Prepared")
            
            self.__update_parallel()
            # self.__clear_screen()
            
            print(f'parallel nr -- {self.__task_conf["parallel"]}')
        
        self.__get_output_file()
        print("Dosia")

        # self._run_operations("dict_with_clients")

    # mamy przygotowane miejsce teraz postawic server aby funcja odpalala server i do zmiennej

    # connect and set server and client
    # run operation
    # get data
    # close server and client 
    
    #TODO PREPARE THAT ON THIRD VM
