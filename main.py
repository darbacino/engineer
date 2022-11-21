import json
from rerun import Rerun
from terminal_operations import Terminal as term
from threading import Thread

import subprocess



# f"sshpass -p '{pswd}' ssh {user}@{host} '{operation}' "

def get_ssh_command(data:dict):
    info = {"server":{"ssh":"", "ip":""}, "clients":[]}
    
    for dev in data:
        if dev["type"] == 'server':
                             
            info["server"]["ssh"] = f'sshpass -p "{dev["password"]}" ssh {dev["name"]}@{dev["ip"]}'
            info["server"]["ip"] = dev["ip"]
        else:
            info["clients"].append(f'sshpass -p "{dev["password"]}" ssh {dev["name"]}@{dev["ip"]}')

    return info

def main():
    
    # rerun = Rerun(repeat_num=2)
    # rerun.start(print,print, sth)
    terminal = term().terminal
    
    # print(terminal(["ls"]))
    # terminal("ls")
    # with subprocess.Popen(["ls"], stdout= subprocess.PIPE) as proc:
    #     print(proc.stdout.read())
    #     proc.
        

    repeat_num = 10
    communications = get_ssh_command(get_config()["dev"])
    # print(communications)
    # print(communications["server"]["ssh"] + " iperf3 -s")
    # for i in range(repeat_num):
    server = Thread(target=terminal, args=[f'"{communications["server"]["ssh"]} iperf3 -s" > oss.txt '])
    client = Thread(target=terminal, args=[f'"{communications["clients"][0]} iperf3 -c {communications["server"]["ip"]}" > ozz.txt'])
    
    # print(communications["server"]["ssh"] + " iperf3 -s")
    # print(communications["clients"][0]+" iperf3 -c "+ communications["server"]["ip"])
    server.start()
    client.start()
        # terminal('ls')
    
    #rerun
    # connect and set server and client
    # run operation
    # get data 
    # close server and client
    
    

if __name__ == "__main__":
    main()






























# # Requrements: python, git, ssh, sshpass 




# from terminal_operations import Terminal as term
# import subprocess
# from threading import Thread


# # TODO third VM or set server 
# # TODO json for data server, clients iperf3
# # TODO 
# def run_operation(user, host, pswd, operation):
#      # tmp = term()
    
    
#     # cmd  = f'ping 192.168.0.10 > ping{user}.txt'
#     # cmd  = f'whoami > ping{user}.txt'
#     # print(cmd)
#     # operation  = f'whoami'
    
#     # prepare_data_place  = f'mkdir output > /dev/null 2> /dev/null; cd output; '
#     prepare_data_place  = f'mkdir output > /dev/null 2> /dev/null; cd output; '
#     connect_to_vm       = f"sshpass -p '{pswdinfom
#     print(cmd := prepare_data_place + connect_to_vm)
#     # pipe = tmp.connect_vm_via_ssh(user, host, cmd)
    
#     pipe = subprocess.Popen(f'{cmd}', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
#     # pipe = tmp.connect_vm_via_ssh(user, host, prepare_data_place + connect_to_vm)

#     for i in pipe:
#         print(i.decode())


#     # ssh vmclient01@192.168.0.52
#     # ssh vmclient02@192.168.0.10


# def main():
    
#     user_name = 'vmclient01'
#     host_addr = '192.168.0.52'
#     password  = '456123789'
#     operation = f'whoami; ping -c 10 192.168.0.10'
    
#     # run_operation(user_name,host_addr,password,operation)
#     t1 = Thread(target=run_operation, args=[user_name,host_addr,password,operation])
    
#     user_name2 = 'vmclient02'
#     host_addr2 = '192.168.0.10'
#     password2  = '456123789'
#     operation2 = f'whoami; ping -c 10 192.168.0.52'

#     t2 = Thread(target=run_operation, args=[user_name2, host_addr2, password2, operation2])
    
#     t1.start()
#     t2.start()

# if '__main__' == __name__:
#     main()
    
    

# # from terminal_operations import Terminal as term
# # import subprocess
# # from threading import Thread

# # # TODO should i create one more data file with all neccesar methods (sth like operations.py) ?


# # def run_operation(user, host, pswd, operation):
# #     prepare_data_place  = f'mkdir output > /dev/null 2> /dev/null; cd output; '
# #     # connect_to_vm       = f"sshpass -p '{pswd}' ssh {user}@{host} '{operation}' > {user}.txt"
    
# #     # connect_to_vm       = f"sshpass -p '{pswd}' ssh {user}@{host} '{operation}' "
# #     connect_to_vm       = "ping 192.168.0.10"
# #     subprocess.Popen(f'{prepare_data_place + connect_to_vm}', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    
# # def run_for_all(num_of_runs, *data, ):
    
# #     pass
# # # TODO third VM or set server 
# # # TODO json for data server, clients iperf3
# # # TODO 
# # def main():
    
# #     user_name = 'vmclient01'
# #     host_addr = '192.168.0.52'
# #     password  = '456123789'
# #     operation = f'whoami; ping -c 10 192.168.0.10'
    
# #     user_name2 = 'vmclient02'
# #     host_addr2 = '192.168.0.10'
# #     password2  = '456123789'
# #     operation2 = f'whoami; ping -c 10 192.168.0.52'
    
# #     Thread(target=run_operation, args=[user_name,host_addr,password,operation]).start()
# #     # Thread(target=run_operation, args=[user_name2, host_addr2, password2, operation2]).start()


# # if '__main__' == __name__:
# #     main()


