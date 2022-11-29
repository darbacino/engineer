import os
import vars , yaml
import zipfile
import connect_setup
# read file by file

def getPaths():
    return []

class IPerfSpeedParser:
    
    def __init__(self, paths):
        for path in paths:
            self._speeds.append(self.parseSpeed(path))
        
    def _parseSpeed(self, path):
        # read the actual speed from file
        speed = 10
        return speed
    
    def getParsedData(self):
        return self.__speeds

    
parser = IPerfSpeedParser(['/home/file1', '/home/file2'])

class AveragingAnalyzer:
    def __init__(self):
        self.result = -1
            
    def setValues(self, values):
        self.values = values

    def _calculateAverage(self):
        self.result = sum(self.values)/len(self.values)
        
    def result(self):
        return self.result

class DataAnalysis:
    
    def __init__(self):
        #get pathes
        self.parser = None # give him pathes resout list of thinvalues one per file
        self.analyzer = None #we have pathes to yamls and do sth with that like UPP
        self.plotter = None # make graph 
        
    def analyze(self):
        self.analyzer.setValues(self.parser.getParsedData())
        

class DABuilder:
    
    def __init__(self, buildMe):
        self._buildMe=buildMe
        
    def withParser(self, parser):
        pass
    
    def withAnalyzer(self, analyzer):
        pass
    
    def withPlotter(self, plotter):
        pass

class Plotter:
    
    def __init__(self) -> None:
        self.__experiment_plotts = []
        self.__connect_setup = connect_setup.ConnectionSetup()
        self.__dict_with_path : dict = {}
        self.__resoult_data = []
        

    def addPlotter(self, __object) :
        self.__experiment_plotts.append(__object)
    
    
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
                                    
    def __load_all_yamls(self, task_name:str =""):
        """If we ignore task name we wil lget ALL yamls

        Args:
            task_name (str, optional): _description_. Defaults to "".

        Returns:
            _type_: _description_
        """
        list_with_yamls = []
        for dev in self.__dict_with_path:
            for task in self.__dict_with_path[dev]:
                
                if task.startswith(task_name) or task_name == "":    
                    for yaml_name in self.__dict_with_path[dev][task]:
                        yaml_name = f"{vars.PATH_LOCAL_DIR_WITH_EXPERIMENTS}/{dev}/{task}/{yaml_name}"       
                        
                        with open(yaml_name,"r") as yaml_file:
                            try:
                                list_with_yamls.append(yaml.safe_load(yaml_file))
                            except yaml.YAMLError as exc:
                                print(f"Ingoring empty Yamls --- {yaml_name}")
        return list_with_yamls
                          
    
    
    def __save_resoults_to_file(self):
        output_path = f"{vars.PATH_LOCAL_DIR_WITH_PLOTER_OUTPUT}/{vars.PLOTTER_RESOULTS_PREFIX}_{self.__connect_setup.get_current_data()}"
        print(output_path)
        with open(output_path,"w") as output:
            for touple in self.__resoult_data:
                output.write(f"{touple[0]}{touple[1]}")
        
    def start(self):
        self.__get_data_from_zip()
        self.__prepare_dict_with_path()
        self.__replace_tabs_with_space()
    
        for plotter in self.__experiment_plotts:
            self.__resoult_data.append(plotter.start(self.__load_all_yamls(plotter.get_task_type())))
            
        self.__save_resoults_to_file()
        print("Plotter --- Done")
        
        
class Iperf3Plotter:
    def __init__(self) -> None:
        self.__task_type = "iperf3"
        
    def get_task_type(self):
        return self.__task_type
    
    def __iperf3_av_speed(self, list_with_yamls):
        bits_per_second = []
        for interval in list_with_yamls[0]["intervals"]:
            for stream in interval["streams"]:
                bits_per_second.append(stream["bits_per_second"])
                
        av_bits_per_second = sum(bits_per_second) / len(bits_per_second)
        
        return ("Average bits per second: ",av_bits_per_second)
        
        
    def start(self,list_with_yamls):
        return self.__iperf3_av_speed(list_with_yamls)
        
# class pip: