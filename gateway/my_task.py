from my_fsm import *
from my_parameters import WAITING, RUNNING, DONE
import my_parameters
from datetime import datetime
import my_os
import json
import my_server

class Task:
    def __init__(self, id: str, cycle_num: int, mixer: list, area: str, start_time: str) -> None:
        if len(mixer) == 3:
            self.id = id
            self.cycle_num = cycle_num
            self.cycle_num_const = cycle_num
            self.mixer = mixer
            self.area = area
            self.start_time = start_time
        else:
            print("invalid mixer")

    def __str__(self) -> str:
        return f"Task {self.id}, {self.cycle_num} cycles, {self.mixer}(mixer1, 2, 3), area {self.area}, {self.start_time}"

class Task_List:
    def __init__(self):
        self.task_list = []

    def is_empty(self):
        return len(self.task_list) == 0

    def add(self, task: Task):
        if self.is_empty():
            self.task_list.append(task)
            return
        for i in range(0, len(self.task_list)):
            if self.task_list[i].start_time > task.start_time:
                self.task_list.insert(i, task)
                return
            if i == len(self.task_list) - 1:
                self.task_list.append(task)

    def remove_by_id(self, task_id: str):
        for task in self.task_list:
            if task.id == task_id:
                self.task_list.remove(task)
                print(f"Task with ID {task_id} removed successfully.")
                return
        print(f"No task found with ID {task_id}.")

    def __str__(self) -> str:
        string = str()
        for task in self.task_list:
            string += (str(task)+'\n')
        return string


waiting = Task_List()
running = Task_List()

def check_waiting_task():
    # check the time of tasks in waiting list
    # if there is any in waiting list need to be run, remove that away the list, add that in running
    global waiting, running
    now = datetime.now()
    current_time = now.strftime("%H:%M")

    if not waiting.is_empty():
        for task in waiting.task_list:
            if task.start_time == current_time:
                w2r = {
                    "code": "w2r",
                    "id": task.id,
                    "start time": task.start_time
                }
                w2r = json.dumps(w2r)
                my_server.server_gateway.client.publish("nemo2602/feeds/iot-gateway", w2r)
                running.add(task)
                waiting.task_list.remove(task)

fsm = None

def check_running_task():
    global waiting, running, command, fsm
    if running.is_empty() == False:
        if my_parameters.status == WAITING:
            fsm = FSM(my_fsm, running.task_list[0], command)
            my_parameters.status = RUNNING
            my_os.operation_system.add_process(fsm.run_fsm,0,1)
        elif my_parameters.status == DONE:
            my_os.operation_system.remove_process(fsm.run_fsm)
            fsm = None
            if running.task_list[0].cycle_num <= 0:
                r2w = {
                    "code": "r2w",
                    "id": running.task_list[0].id,
                    "start time": running.task_list[0].start_time
                }
                r2w = json.dumps(r2w)
                my_server.server_gateway.client.publish("nemo2602/feeds/iot-gateway", r2w)
                running.task_list[0].cycle_num = running.task_list[0].cycle_num_const
                waiting.task_list.append(running.task_list.pop(0))
            elif running.task_list[0].cycle_num > 0:
                update = {
                    "code": "update",
                    "id": running.task_list[0].id,
                    "cycle": running.task_list[0].cycle_num
                }
                update = json.dumps(update)
                my_server.server_gateway.client.publish("nemo2602/feeds/iot-gateway", update)
                running.task_list.append(running.task_list.pop(0))
            my_parameters.status = WAITING


# for testing
# from datetime import datetime
# now = datetime.now()
# current_time = now.strftime("%H:%M")
# print("Current Time =", current_time, type(current_time))

# task1 = Task("1", 5, [20, 35, 10], "2", "18:30")
# task3 = Task("3", 5, [20, 35, 10], "2", "19:00")
# task4 = Task("4", 5, [20, 35, 10], "2", "01:35")
# task2 = Task("2", 5, [20, 35, 10], "3", "18:03")
# task_list = Task_List()
# task_list.add(task1)
# task_list.add(task2)
# task_list.add(task3)
# task_list.add(task4)
# print(task_list)
