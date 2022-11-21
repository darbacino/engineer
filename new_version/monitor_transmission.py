from iperf3_tool import Iperf3Tool

class MonitorTransmission:
    __counter_reruns = 0
    __test_iperf3 = False

    def __init__(self):
        pass
    
    def set_counter_reruns(self, counter:int):
        self.__counter_reruns = counter

    def test_iperf3(self):
        self.__test_iperf3 = True
        self.__iperf3 = Iperf3Tool()

    def start(self):
        for _ in range(self.__counter_reruns):
            if(self.__test_iperf3):
                # print(self)
                
                self.__iperf3.start()
                
                
                
                
        