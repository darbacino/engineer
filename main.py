# from terminal_operations import Terminal as term
# import subprocess
# from threading import Thread

# # TODO should i create one more data file with all neccesar methods (sth like operations.py) ?


# def run_operation(user, host, pswd, operation):
#     prepare_data_place  = f'mkdir output > /dev/null 2> /dev/null; cd output; '
#     # connect_to_vm       = f"sshpass -p '{pswd}' ssh {user}@{host} '{operation}' > {user}.txt"
    
#     # connect_to_vm       = f"sshpass -p '{pswd}' ssh {user}@{host} '{operation}' "
#     connect_to_vm       = "ping 192.168.0.10"
#     subprocess.Popen(f'{prepare_data_place + connect_to_vm}', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    
# def run_for_all(num_of_runs, *data, ):
    
#     pass
# # TODO third VM or set server 
# # TODO json for data server, clients iperf3
# # TODO 
# def main():
    
#     user_name = 'vmclient01'
#     host_addr = '192.168.0.52'
#     password  = '456123789'
#     operation = f'whoami; ping -c 10 192.168.0.10'
    
#     user_name2 = 'vmclient02'
#     host_addr2 = '192.168.0.10'
#     password2  = '456123789'
#     operation2 = f'whoami; ping -c 10 192.168.0.52'
    
#     Thread(target=run_operation, args=[user_name,host_addr,password,operation]).start()
#     # Thread(target=run_operation, args=[user_name2, host_addr2, password2, operation2]).start()


# if '__main__' == __name__:
#     main()









from terminal_operations import Terminal as term
import subprocess
from threading import Thread

# TODO shoudl i create one more data file with all neccesar methods?


def run_operation(user, host, pswd, operation):
     # tmp = term()
    
    
    # cmd  = f'ping 192.168.0.10 > ping{user}.txt'
    # cmd  = f'whoami > ping{user}.txt'
    # print(cmd)
    # operation  = f'whoami'
    
    prepare_data_place  = f'mkdir output > /dev/null 2> /dev/null; cd output; '
    connect_to_vm       = f"sshpass -p '{pswd}' ssh {user}@{host} '{operation}' > {user}.txt"
    # connect_to_vm       = f"sshpass -p '{pswd}' ssh {user}@{host} '{operation}' "
    
    # cmd  = prepare_data_place + connect_to_vm
    print(cmd := prepare_data_place + connect_to_vm)
    # pipe = tmp.connect_vm_via_ssh(user, host, cmd)
    
    pipe = subprocess.Popen(f'{cmd}', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    # pipe = tmp.connect_vm_via_ssh(user, host, prepare_data_place + connect_to_vm)

    for i in pipe:
        print(i.decode())


    # ssh vmclient01@192.168.0.52
    # ssh vmclient02@192.168.0.10


def main():
    
    user_name = 'vmclient01'
    host_addr = '192.168.0.52'
    password  = '456123789'
    operation = f'whoami; ping -c 10 192.168.0.10'
    
    # run_operation(user_name,host_addr,password,operation)
    t1 = Thread(target=run_operation, args=[user_name,host_addr,password,operation])
    
    user_name2 = 'vmclient02'
    host_addr2 = '192.168.0.10'
    password2  = '456123789'
    operation2 = f'whoami; ping -c 10 192.168.0.52'

    t2 = Thread(target=run_operation, args=[user_name2, host_addr2, password2, operation2])
    
    t1.start()
    t2.start()

if '__main__' == __name__:
    main()
