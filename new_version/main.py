from monitor_transmission import MonitorTransmission


def main():
    
    monitor_tool = MonitorTransmission()

    monitor_tool.test_iperf3()
    monitor_tool.set_counter_reruns(1)
    
    
    monitor_tool.start()
    

if __name__ == "__main__":
    main()
    