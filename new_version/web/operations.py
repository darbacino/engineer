import json


import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import main


def add_to(dict_data, d):
    
    new_task = {}
    tmp_index = 0
    tmp_key = ""
    for k,v in d.items():
        
        if v:
            if tmp_index % 2 ==0:
                tmp_key = v
                new_task[v] = ""
            else:
                new_task[tmp_key] = v
        
        tmp_index += 1
            
    return new_task

def remove_task_dev(dict_data, user_data,task):
    for k,v in user_data.items():
        for i in range(len(dict_data["dev"])):
            if dict_data[task][i]['name'] == v:
                del dict_data[task][i]
                return dict_data
    
def dev_prepare_config(d:dict):
    dict_data = None
    with open('./configuration.json') as json_file:
        dict_data = json.load(json_file)
    

    if "btn_add_dev" in d.keys():
        prepared = add_to(dict_data=dict_data, d=d)
        dict_data["dev"].append(prepared)
        
        
    elif "btn_rm_dev" in d.keys():
        
        dict_data = remove_task_dev(dict_data,d,task="dev")
            
        print("rm dev")
        
    elif "btn_add_task" in d.keys():
        prepared = add_to(dict_data=dict_data, d=d)
        dict_data["task"].append(prepared)
 
        
    elif "btn_rm_task" in d.keys():
        dict_data = remove_task_dev(dict_data,d,task="task")
            
        print("rm task")
        
    print(json.dumps(dict_data, indent=4))
    with open("configuration.json", "w") as outfile:
        json.dump(dict_data, outfile)
          
def show_config(data = None):
    if data == None:
        with open("./configuration.json", "r") as file:
            data = file.read()
    
    data = json.loads(data)
    return json.dumps(data, indent=4)

def run_tasks(task_dict:dict):
    print(task_dict)
    iperf3_task = False
    task_ping = False
    plotter_iperf = False
    
    if "task_iperf3" in task_dict:
        iperf3_task = True
        
    if "task_ping" in task_dict:
        task_ping = True
    
    if "plotter_iperf3" in task_dict:
        plotter_iperf = True
    
    # main.run_selected_tasks(iperf3_task, task_ping, plotter_iperf)
    main.run_selected_tasks(Plotter_iperf=True)