from ExperimentRunner import ExperimentRunner

from iperf3_tool import Iperf3Tool
from connect_setup import *
from Plotter import Iperf3Plotter

def main():
    runner = ExperimentRunner()
    runner.addStrategy(Iperf3Tool())
    #runner.addPlotter(Iperf3Plotter())


    runner.start()
    

if __name__ == "__main__":
    main()
    
# get data from folders
# parser that data 
# simple module to analize thad, np av

#DONE 
## DONE when we will rerun the data can be overrided carefull good will be add data of created foldere it will cause problems 
# solution each save to fille will have time full time and the main follder will take them all. The analizer will analize with correct name like generate sth for iperf and time will make differecnes :)
# self.addStrategy(PrepareDevices(cleanup=True)) # That will be added on the end of the list (last task) to take data
## DONE what if there will be execution of that ? maybe i should take data while plotting them 
# DONE zip


