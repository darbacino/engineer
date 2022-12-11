import os
import vars , yaml, json
import zipfile
import connect_setup
import matplotlib.pyplot as plt
import shutil

class DataAnalysisPrepare:
    def __init__(self) -> None:
        self.__dict_with_path : dict = {}
        self.__prepare_zips()

    def __get_dirs_in_path(self, path):
        return [item for item in os.listdir(path) if os.path.isdir(f"{path}/{item}")]

    def uniquify(self, path):
        filename, extension = os.path.splitext(path)
        counter = 1

        while os.path.exists(path):
            path = f"{filename}({counter})"
            counter += 1

        return path
    
    def __get_data_from_zip(self):
        extension_of_zip:str = ".zip"
        default_data_folder_name = f"{vars.PATH_LOCAL_DIR_WITH_EXPERIMENTS}/{vars.PATH_DATA_FOLDER}"
        
        for zip_file in os.listdir(vars.PATH_LOCAL_DIR_WITH_EXPERIMENTS):
            if zip_file.endswith(extension_of_zip):
                
                zip_file_path = f"{vars.PATH_LOCAL_DIR_WITH_EXPERIMENTS}/{zip_file}"
                new_data_folder_name = f"{vars.PATH_LOCAL_DIR_WITH_EXPERIMENTS}/{zip_file.rstrip('.zip')}"
                
                zip_ref = zipfile.ZipFile(zip_file_path)
                zip_ref.extractall(vars.PATH_LOCAL_DIR_WITH_EXPERIMENTS)
                zip_ref.close()
                
                os.rename(default_data_folder_name, new_data_folder_name)
                os.remove(zip_file_path) 
        
        cwd = vars.PATH_LOCAL_DIR_WITH_EXPERIMENTS


        experiment_dir_name = self.uniquify(f"{cwd}/experiment")
        

                
        for index, device in enumerate(self.__get_dirs_in_path(cwd)):
            if "experiment" in device:
                continue
            dev_name = device.split('_',1)[0]
            
            for dir_task in self.__get_dirs_in_path(f"{cwd}/{device}"):
                task_name = dir_task.split('_',1)[0]

                if not os.path.exists(f"{experiment_dir_name}"):
                    os.mkdir(f"{experiment_dir_name}")

                if not os.path.exists(f"{experiment_dir_name}/{task_name}"):
                    os.mkdir(f"{experiment_dir_name}/{task_name}")

                
                for task_data in os.listdir(f"{cwd}/{device}/{dir_task}"):
                    os.rename(f"{cwd}/{device}/{dir_task}/{task_data}",f"{experiment_dir_name}/{task_name}/{index}_{dev_name}_{task_data}" )

            shutil.rmtree(f"{cwd}/{device}")
        


    
    def __prepare_dict_with_path(self):
        for devices_data in os.listdir(vars.PATH_LOCAL_DIR_WITH_EXPERIMENTS):
            self.__dict_with_path[devices_data] = {}
            
            for dir_in_dict in os.listdir(f"{vars.PATH_LOCAL_DIR_WITH_EXPERIMENTS}/{devices_data}"):
                self.__dict_with_path[devices_data][dir_in_dict] = []
                
                for tool_dir in os.listdir(f"{vars.PATH_LOCAL_DIR_WITH_EXPERIMENTS}/{devices_data}/{dir_in_dict}"):
                    self.__dict_with_path[devices_data][dir_in_dict].append(tool_dir)

    def __replace_tabs_with_space(self):
         for dev in self.__dict_with_path:
            for task in self.__dict_with_path[dev]:    
                for yaml_name in self.__dict_with_path[dev][task]:
                    
                    yaml_path = f"{vars.PATH_LOCAL_DIR_WITH_EXPERIMENTS}/{dev}/{task}/{yaml_name}"  
                    lines = ""
                    
                    with open(yaml_path, 'r', encoding='utf-8') as input_file:
                        lines = input_file.readlines()
                        
                    with open(yaml_path, 'w', encoding='utf-8') as output_file:
                        for line in lines:
                            output_file.write(line.replace('\t', '    '))
                 
    def get_yamls_paths_task(self, path):
        list_with_yamls = []
        
        # for task in os.listdir(f"{vars.PATH_LOCAL_DIR_WITH_EXPERIMENTS}/data"):
        #     # if 
        #     pass
        
        # for dev in self.__dict_with_path:
        #     for task in self.__dict_with_path[dev]:

        #         if task.startswith(task_name) or task_name == "":    
        #             for yaml_name in self.__dict_with_path[dev][task]:
        #                 yaml_name = f"{vars.PATH_LOCAL_DIR_WITH_EXPERIMENTS}/{dev}/{task}/{yaml_name}"       
        #                 list_with_yamls.append(yaml_name)


        for yaml_name in os.listdir(path):
            list_with_yamls.append(f"{path}/{yaml_name}")

        return list_with_yamls
    
    def get_yamls_paths(self):
        return self.__dict_with_path
    
    def __prepare_zips(self):
        self.__get_data_from_zip()
        # self.__prepare_dict_with_path()
        # self.__replace_tabs_with_space()

class IPerfSpeedParser:
    def __init__(self):
        self.__speeds = []
        self.__speeds_dict = {}

    def __parseSpeed(self, path):
        yaml_data = None
        data = None
        
        with open(path,"r") as yaml_file:
            try:
                json_data = json.load(yaml_file)
                data = json_data["intervals"][0]["streams"][0]["bits_per_second"]
            except:
                print('none')
                return None

            parallel_nr = path.rsplit('/',1)[1].split('_',4)[3]
            print(parallel_nr)
            if parallel_nr not in self.__speeds_dict:
                self.__speeds_dict[parallel_nr] = [data]
            else:
                self.__speeds_dict[parallel_nr].append(data)
        
    def parse_data(self,paths):
        for path in paths:
            print(f'path -- {path}')
            self.__parseSpeed(path)
    
    def getParsedData(self):
        return self.__speeds_dict

class AveragingAnalyzer:
    def __init__(self):
        self.__result = []
        
            
    def setValues(self, values):
        self.values = values

    def calculateAverage(self):
        print('\n\n\n\n')
        print(self.values)
        for data in self.values:
            self.__result.append((int(data),sum(self.values[data])/len(self.values[data])))
        

    def result(self):
        return self.__result

class AveragePlotter:
    def __init__(self) -> None:
        pass 
    def set_data(self,data):
        self.__data = data
        self.__data.sort() 
        
    def make_graph(self):
        parallel,res = zip(*self.__data)
        plt.plot(parallel,res)
        plt.ylabel('some numbers')
        dir_for_graph = f"{vars.CURRENT_WORKING_DIR}/Graphs/graph.png"
        # dir_for_graph = DataAnalysisPrepare.uniquify(self,path=dir_for_graph)
        plt.savefig(dir_for_graph)
        # plt.show()
        
class DataAnalysis:
    
    def __init__(self, path_to_data) -> None:
        self.__path_to_data = path_to_data
        # set path to all "iperf3 or pings" czyli daj mu swciezke i tam ma wszystkie yamle 
        self.preparation = DataAnalysisPrepare()
    
    def withParser(self, _parser):
        self.parser = _parser
        # give him pathes resout list of this values one per file
    
    def withAnalyzer(self, _analyzer):
        self.analyzer = _analyzer
        # we have pathes to yamls and do sth with that like UPP
    
    def withPlotter(self, _plotter):
        self.plotter = _plotter
        # make graph 
        
    def start_iperf3(self):
        yaml_paths = self.preparation.get_yamls_paths_task(self.__path_to_data)

        self.parser.parse_data(yaml_paths) 
        self.analyzer.setValues(self.parser.getParsedData())
        self.analyzer.calculateAverage()
        self.plotter.set_data(self.analyzer.result())
        
        self.plotter.make_graph()

    
