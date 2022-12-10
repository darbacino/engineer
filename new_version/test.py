# # # class mother:

# # #     def __init__(self) -> None:
# # #         print("M")

# # #     def __bum(self):
# # #         print("BOOM")


# # # class child(mother):
# # #     def __init__(self) -> None:
# # #         mother.__init__(self=self)


# # #     def cos(self):

# # #         mother._mother__bum(self)


# # # c = child()
# # # c.cos()


# # import random

# # skreslone_liczby = [10, 15, 2, 13, 4, 9] 
# # wylosowane_liczby = []  

# # for _ in skreslone_liczby:
# #     while True:
# #         wylosowana = random.randint(1, 19)
        
# #         if wylosowana not in wylosowane_liczby:
# #             wylosowane_liczby.append(wylosowana)
# #             break
        
# # trafione = len([trafione for trafione in skreslone_liczby if trafione in wylosowane_liczby])

# # if trafione == 6:
# #     print("GLOWNA NAGRODA !!!!!!")
# # elif trafione >= 3:
# #     print(f"Nagroda pieniężna za trafienie {trafione} liczb!")
# # else:
# #     print("Sproboj ponownie ;)")


# # # wylosowane_liczby = [random.randint(1,19) for _ in skreslone_liczby] # wykona sie tyle razy ile skreslonych liczb


# # # print(wylosowane_liczby)
     
        
        
# """
# #         from connect_setup import *
# # import vars
# # from multiprocessing import Process
# # from itertools import count


# # class ExperimentTemplate:
# #     def __init__(self) -> None:
# #         self.__connect   = Connection()
# #         self.__dev_op    = DevOperations()
# #         self.__config    = self.__dev_op.get_config()
# #         self.__task_name = "iperf3"
# #         self.__task_conf = self.__dev_op.get_task_config(self.__task_name)
# #         self.__server_ip = ""
# #         self.__name_of_testing_parameter = "parallel"
        
# #     def __run_command_on_servers(self, command: str):
# #         #Run command on servers from config

# #         #Args:
# #         #    command (str): command with will be executed

# #         #Returns:
# #          #   list: That list contain connection and output from terminal
# #          
# #         list_of_servers = []

# #         for device in self.__config["dev"]:
# #             if device["type"] == "server":
# #                 self.__server_ip = device["ip"]

# #                 list_of_servers.append(
# #                     self.__connect.connect_vm_via_sshkey(
# #                         cmd=command,
# #                         host=device["ip"],
# #                         user=device["name"],
# #                     )
# #                 )

# #         return list_of_servers

# #     def __run_command_on_clients(self, command: str):
# #         #Run command on client from config

# #         Args:
# #             command (str): command with will be executed

# #         Returns:
# #             list: That list contain connection and output from terminal
# #         #
# #         list_with_clients = []

# #         for device in self.__config["dev"]:
# #             if device["type"] == "client":
# #                 list_with_clients.append(
# #                     self.__connect.connect_vm_via_sshkey(
# #                         cmd=command,
# #                         host=device["ip"],
# #                         user=device["name"],
# #                     )
# #                 )

# #         return list_with_clients

# #     def __get_logfile_path_and_name(self):
# #         #Prepare dir and name of file.
# #         self.__tool_data_dir - give path to folder where should be changes
# #         self.__name_of_testing_parameter - what part of config we are changing (ex. parallel)
# #         self.__task_conf['parallel'] - current value of variable that changes in config
# #         Returns:
# #             str: dir with name of logfile
# #         #
# #         return f"{self.__tool_data_dir}/{self.__name_of_testing_parameter}_{self.__task_conf['parallel']}_{self.__dev_op.get_current_date()}"
    
# #     def __run_servers(self):
# #         #That method will run prepared command on only server

# #         Returns:
# #             list: That list contain connection and output from terminal
# #         #
# #         command = f"iperf3 -s -1 -J --logfile {self.__get_logfile_path_and_name()}"
 
# #         return self.__run_command_on_servers(command)

# #     def __run_clients(self):
# #         #That method will run prepared command on only clients

# #         Returns:
# #             list: That list contain connection and output from terminal
# #         #
# #         command = f"iperf3 --parallel {self.__task_conf['parallel']} -c {self.__server_ip} -t {self.__task_conf['transsmision_time']} -J --logfile {self.__get_logfile_path_and_name()}"

# #         return self.__run_command_on_clients(command)

# #     def __update_config(self, name_of_var: str):
# #         #Update variable in config. That method is for updating settings on devices with will give diffrent output.
# #         Ex. Parralel
# #         #

# #         self.__task_conf[name_of_var] += self.__task_conf["counter"]

# #     def __run_command_on_all_dev(self, command):
# #         #Run given command on all devices from configuration

# #         Args:
# #             command (str): command that will be executed on all devices

# #         Returns:
# #             list: That list contain connection and output from terminal
# #         #
# #         devices = []

# #         for device in self.__config["dev"]:
# #             self.__server_ip = device["ip"]

# #             devices.append(
# #                 self.__connect.connect_vm_via_sshkey(
# #                     cmd=command,
# #                     host=device["ip"],
# #                     user=device["name"],
# #                 )
# #             )

# #         return devices

# #     def create_dir_for_tool(self):
# #         #Prepare specific directory for tool

# #         Returns:
# #             list: That list contain connection and output from terminal
# #         #
# #         self.__tool_data_dir = f"{vars.PATH_DATA_FOLDER}{self.__task_name}_{self.__dev_op.get_current_date()}"
# #         create_dir_command = f"mkdir {self.__tool_data_dir}"

# #         return self.__run_command_on_all_dev(create_dir_command)

# #     def __timeout_of_funcion(self, reference_to_func, retry=5, func_timeout=3):
# #         #Set timeout and number of retry for funcion

# #         Args:
# #             reference_to_func (func): name_of_funcion without "()"
# #             retry (int, optional): Number of attempts. Defaults to 5.
# #             func_timeout (int, optional): max time for funcion to finish. Defaults to 3.
# #         #
# #         for _ in range(retry):
# #             proc = Process(target=reference_to_func)
# #             proc.start()
# #             proc.join(timeout=func_timeout)
# #             proc.terminate()

# #             # if finished in expect time
# #             if proc.exitcode == 0:
# #                 return

# #     def start(self):

# #         for repeat in range(self.__task_conf["repeats"]):
# #             if repeat > 0:
# #                 print(f"Repeat nr. {repeat+1}")

# #             self.create_dir_for_tool()

# #             while self.__task_conf["parallel"] <= self.__task_conf["parallel_end"]:
# #                 print(f'Parallel nr. {self.__task_conf["parallel"]}')

# #                 self.__timeout_of_funcion(self.__run_servers)
# #                 self.__timeout_of_funcion(self.__run_clients)

# #                 self.__update_config("parallel")



# # class Iperf3Parallel(ExperimentTemplate):
# #     def __init__(self) -> None:
# #         super().__init__()
        
        
# #     def start(self):
# #         s = self.__task_name
# #         print(s)
# #         # return super().start()
# """

# print("File I/O\n")
# try:
    
#     text_file = open("read_it.txt", "r")
# except SyntaxError:
#     print('ile does not exis')
    
# #Read stuff   
# for s in range(0, 4):
#     try:
#          print(text_file.readline()) 
#     except IOError: 
#         print("File does not exist") 
# text_file.close()





# class DataAnalysisPrepare:
    
#     def __init__(self) -> None:
#         self.__experiment_plotts = []
#         self.__connectnect_setup = connect_setup.Connection()
#         self.__dev_op = connect_setup.DevOperations()
#         self.__dict_with_path : dict = {}
#         self.__resoult_data = []
        
#         self.prepare_zips()

#     # def addPlotter(self, __object) :
#     #     self.__experiment_plotts.append(__object)
    
#     def __get_data_from_zip(self):
#         extension_of_zip:str = ".zip"
#         default_data_folder_name = f"{vars.PATH_LOCAL_DIR_WITH_EXPERIMENTS}/{vars.PATH_DATA_FOLDER}"
        
#         for zip_file in os.listdir(vars.PATH_LOCAL_DIR_WITH_EXPERIMENTS):
#             if zip_file.endswith(extension_of_zip):
                
#                 zip_file_path = f"{vars.PATH_LOCAL_DIR_WITH_EXPERIMENTS}/{zip_file}"
#                 new_data_folder_name = f"{vars.PATH_LOCAL_DIR_WITH_EXPERIMENTS}/{zip_file.rstrip('.zip')}"
                
#                 zip_ref = zipfile.ZipFile(zip_file_path)
#                 zip_ref.extractall(vars.PATH_LOCAL_DIR_WITH_EXPERIMENTS)
#                 zip_ref.close()
                
#                 os.rename(default_data_folder_name, new_data_folder_name)
#                 os.remove(zip_file_path) 

#     def __prepare_dict_with_path(self):
#         for devices_data in os.listdir(vars.PATH_LOCAL_DIR_WITH_EXPERIMENTS):
#             self.__dict_with_path[devices_data] = {}
            
#             for dir_in_dict in os.listdir(f"{vars.PATH_LOCAL_DIR_WITH_EXPERIMENTS}/{devices_data}"):
#                 self.__dict_with_path[devices_data][dir_in_dict] = []
                
#                 for tool_dir in os.listdir(f"{vars.PATH_LOCAL_DIR_WITH_EXPERIMENTS}/{devices_data}/{dir_in_dict}"):
#                     self.__dict_with_path[devices_data][dir_in_dict].append(tool_dir)
   
#     def __replace_tabs_with_space(self):
#          for dev in self.__dict_with_path:
#             for task in self.__dict_with_path[dev]:    
#                 for yaml_name in self.__dict_with_path[dev][task]:
                    
#                     yaml_path = f"{vars.PATH_LOCAL_DIR_WITH_EXPERIMENTS}/{dev}/{task}/{yaml_name}"  
#                     lines = ""
                    
#                     with open(yaml_path, 'r', encoding='utf-8') as input_file:
#                         lines = input_file.readlines()
                        
#                     with open(yaml_path, 'w', encoding='utf-8') as output_file:
#                         for line in lines:
#                             output_file.write(line.replace('\t', '    '))
                               
#     def get_yamls_paths(self):
#         return self.__dict_with_path
         
#     def load_all_yamls(self, task_name:str =""):
#         """If we ignore task name we wil lget ALL yamls

#         Args:
#             task_name (str, optional): _description_. Defaults to "".

#         Returns:
#             _type_: _description_
#         """
#         list_with_yamls = []
#         for dev in self.__dict_with_path:
#             for task in self.__dict_with_path[dev]:
                
#                 if task.startswith(task_name) or task_name == "":    
#                     for yaml_name in self.__dict_with_path[dev][task]:
#                         yaml_name = f"{vars.PATH_LOCAL_DIR_WITH_EXPERIMENTS}/{dev}/{task}/{yaml_name}"       
                        
#                         with open(yaml_name,"r") as yaml_file:
#                             try:
#                                 list_with_yamls.append(yaml.safe_load(yaml_file))
#                             except yaml.YAMLError as exc:
#                                 print(f"Ingoring empty Yamls --- {yaml_name}")
#         return list_with_yamls
                          
    
    
#     def __save_resoults_to_file(self):
#         output_path = f"{vars.PATH_LOCAL_DIR_WITH_PLOTER_OUTPUT}/{vars.PLOTTER_RESOULTS_PREFIX}_{self.__dev_op.get_current_date()}"
#         print(output_path)
#         with open(output_path,"w") as output:
#             for touple in self.__resoult_data:
#                 output.write(f"{touple[0]}{touple[1]}")
        
#     def prepare_zips(self):
#         self.__get_data_from_zip()
#         self.__prepare_dict_with_path()
#         self.__replace_tabs_with_space()
        
#         # for plotter in self.__experiment_plotts:
#         #     self.__resoult_data.append(plotter.start(self.__load_all_yamls(plotter.get_task_type())))
            
#         # self.__save_resoults_to_file()
#         # print("Plotter --- Done")
        
        
        















# # class Iperf3Plotter:
# #     def __init__(self) -> None:
# #         self.__task_type = "iperf3"
        
# #     def get_task_type(self):
# #         return self.__task_type
    
# #     def __iperf3_av_speed(self, list_with_yamls):
# #         bits_per_second = []
# #         for interval in list_with_yamls[0]["intervals"]:
# #             for stream in interval["streams"]:
# #                 bits_per_second.append(stream["bits_per_second"])
                
# #         av_bits_per_second = sum(bits_per_second) / len(bits_per_second)
        
# #         return ("Average bits per second: ",av_bits_per_second)
        
        
# #     def start(self,list_with_yamls):
# #         return self.__iperf3_av_speed(list_with_yamls)
        
# # # class pip:


print("ssz" in "dsadsadsaszszszzsdadas")