import time
import my_os
import my_task
import my_fsm
import my_ai
if True:
    my_os.operation_system.add_process(my_task.check_waiting_task, 0, 5)
    my_os.operation_system.add_process(my_task.check_running_task, 0, 1)
    
    my_os.operation_system.add_process(my_fsm.get_humidity, 20, 100)
    my_os.operation_system.add_process(my_fsm.get_temperature, 0, 100)
    my_os.operation_system.add_process(
        my_ai.temperature_model.retrain, 36000, 36000)
    my_os.operation_system.add_process(
        my_ai.humidity_model.retrain, 36000, 36000
    )
cnt = 0
second = 0

while True:
    if cnt == 10:
        cnt = 0
        second += 1
        print(second)
        # print("status: ", status)
        # print("wating task", my_task.waiting)
        # print("running task", my_task.running)
        # print(my_os.operation_system)
    else:
        cnt += 1
    my_os.operation_system.dispatch_process()
    time.sleep(0.1)
