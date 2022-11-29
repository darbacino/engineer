from connect_setup import PrepareDevices
from Plotter import Plotter
        

class ExperimentRunner:
    # __prepare_devices = PrepareDevices()
    
    def __init__(self, reruns = 1):
        self.__experiments = []
        self.__experiment_reruns = reruns
        self.__plotter = Plotter()
    # def __del__(self):
    #     self.start()
    
    def addStrategy(self, __object) :
        self.__experiment_strategies.append(__object)
        
    def addPlotter(self, __object):
        self.__plotter.addPlotter(__object)
        
    def setReruns(self, num:int):
        if num>0:
            self.__experiment_reruns = num
        else:
            print(f"Error in setReruns({num}) -- value '{num}' must be bigger than 0. Exit")
            exit(1)
 
    def start(self):
        for _ in range(self.__experiment_reruns):
            PrepareDevices(cleanup=True).start() # checking/preparing data each rerun
            
            for strategy in self.__experiment_strategies:
                strategy.start()

            PrepareDevices().start() # checking/preparing data each rerun
            self.__plotter.start()
                
        
            

