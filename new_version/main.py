from ExperimentRunner import ExperimentRunner

from ExperimentTemplate import *
from connect_setup import *
from DataAnalysis import *

# poprawki 

# strona https://www.bootdey.com/snippets/view/account-settings

# stroky pod storny do generacji danych czyli config 

# strona do analizy dancyh Data analysis
# baza dancyh


# Na deser ksiazka 


# poprawki czyli trzeba rozpakowac i zebrc to do jednego pliku 
# dodac do generowanego pliku nazwe urzadzenai na ktorym sie wykonuje task albo np 

def run_selected_tasks(Iperf=False, Ping=False, Plotter_iperf=False):
    print("test2")

    runner = ExperimentRunner()

    if Iperf:
        print("here2?")
        # runner.addStrategy(Iperf3Parallel())
    
    if Ping:
        print("here3?")
        #runner.addStrategy(PingTask())
   
    runner.start()
    
    # plot = DataAnalysisPrepare()
    # plot.addPlotter(Iperf3Plotter())
    # plot.start()
    
    path_to_data = "/home/darbacino/Desktop/engineer/engineer/new_version/ExperimentData/experiment(2)/iperf3"
    d_analysis = DataAnalysis(path_to_data)
    d_analysis.withParser(IPerfSpeedParser())
    d_analysis.withAnalyzer(AveragingAnalyzer())
    d_analysis.withPlotter(AveragePlotter())
    
    if Plotter_iperf:
        d_analysis.start_iperf3()
    
def main():
    print("here??")
    runner = ExperimentRunner()

    runner.addStrategy(Iperf3Parallel())
    runner.addStrategy(PingTask())

    runner.start()
    
    # plot = DataAnalysisPrepare()
    # plot.addPlotter(Iperf3Plotter())
    # plot.start()
    
    path_to_data = "/home/darbacino/Desktop/engineer/engineer/new_version/ExperimentData/experiment(2)/iperf3"
    d_analysis = DataAnalysis(path_to_data)
    d_analysis.withParser(IPerfSpeedParser())
    d_analysis.withAnalyzer(AveragingAnalyzer())
    d_analysis.withPlotter(AveragePlotter())
    
    d_analysis.start_iperf3()
    
    

if __name__ == "__main__":
    # main()
    pass
    
# get data from folders
# parser that data 
# simple module to analize thad, np av

#DONE 
## DONE when we will rerun the data can be overrided carefull good will be add data of created foldere it will cause problems 
# solution each save to fille will have time full time and the main follder will take them all. The analizer will analize with correct name like generate sth for iperf and time will make differecnes :)
# self.addStrategy(DevOperations(cleanup=True)) # That will be added on the end of the list (last task) to take data
## DONE what if there will be execution of that ? maybe i should take data while plotting them 
# DONE zip



    # mamy przygotowane miejsce teraz postawic server aby funcja odpalala server i do zmiennej

    # connect and set server and client
    # run operation
    # get data
    # close server and client

    # TODO PREPARE THAT ON THIRD VM


# TODO Prepare that like it is separated class that  have methods that we will use to iperf3
