import my_parameters
import my_os
import my_serial
import my_crc
import my_server
import my_ai

class Command:
    def __init__(self, data=0, flag=0):
        self.data = data
        self.flag = flag

    def read_connection(self):
        self.data = my_serial.serialUART.ReadSerial()

    def send_command(self, command):
        my_serial.serialUART.ser.write(my_crc.crc_calc.export(command))

    def turn_mixer_1_on(self):
        self.send_command("MIXER1_ON")

    def turn_mixer_1_off(self):
        self.send_command("MIXER1_OFF")

    def turn_mixer_2_on(self):
        self.send_command("MIXER2_ON")

    def turn_mixer_2_off(self):
        self.send_command("MIXER2_OFF")

    def turn_mixer_3_on(self):
        self.send_command("MIXER3_ON")

    def turn_mixer_3_off(self):
        self.send_command("MIXER3_OFF")

    def select_area(self, area):
        self.send_command(f"SELECTOR{area}_ON")

    def unselect_area(self, area):
        self.send_command(f"SELECTOR{area}_OFF")

    def turn_in_pump_on(self):
        self.send_command("PUMP_IN_ON")

    def turn_in_pump_off(self):
        self.send_command("PUMP_IN_OFF")

    def turn_out_pump_on(self):
        self.send_command("PUMP_OUT_ON")

    def turn_out_pump_off(self):
        self.send_command("PUMP_OUT_OFF")

    def get_temperature(self):
        self.send_command("SOIL_TEMPERATURE")

    def get_humidity(self):
        self.send_command("SOIL_HUMIDITY")


command = Command()
count_temp = 0

def my_fsm_temperature():
    global command, count_temp
    data = my_serial.serialUART.ReadSerial()
    if data < 0:
        if count_temp % 10 == 0:   
            my_os.operation_system.add_process(command.get_temperature)
            print("Sent temperature")
        elif count_temp // 10 > 3:
            print("Temperature timeout")
            my_os.operation_system.remove_process(my_fsm_temperature)
            count_temp = 0
    else:
        print(data)
        my_ai.humidity_model.verification(data)
        my_server.server_gateway.client.publish("nemo2602/feeds/iot-temperature", data / 100)
        my_os.operation_system.remove_process(my_fsm_temperature)
    count_temp += 1

def get_temperature():
    global count_temp
    count_temp = 0
    my_os.operation_system.add_process(my_fsm_temperature, 0, 1)
    my_os.operation_system.add_process(command.get_temperature)

count_humid = 0

def my_fsm_humidity():
    global command, count_humid
    data = my_serial.serialUART.ReadSerial()
    if data < 0:
        if count_humid % 10 == 0:
            my_os.operation_system.add_process(command.get_humidity)
            print("Sent humidity")
        elif count_humid // 10 > 3:
            print("Humidity timeout")
            my_os.operation_system.remove_process(my_fsm_humidity)
            count_humid = 0
    else:
        print(data)
        my_ai.humidity_model.verification(data)
        my_server.server_gateway.client.publish("nemo2602/feeds/iot-humidity", data / 100)
        my_os.operation_system.remove_process(my_fsm_humidity)
    count_humid += 1

def get_humidity():
    global count_humid
    count_humid = 0
    my_os.operation_system.add_process(my_fsm_humidity, 0, 1)
    my_os.operation_system.add_process(command.get_humidity)


def my_fsm(state, task, command, count, flag):
    my_os.operation_system.add_process(command.read_connection, 0, 0)
    actions = {
        my_parameters.ST_IDLE: ("turn_mixer_1_on", my_parameters.ST_MIXER1, "Turn on mixer1: "),
        my_parameters.ST_MIXER1: ("turn_mixer_1_on", my_parameters.ST_MID_1_2, "Turn off mixer 1: ", 0),
        my_parameters.ST_MID_1_2: ("turn_mixer_1_off", my_parameters.ST_MIXER2, "Turn on mixer2: "),
        my_parameters.ST_MIXER2: ("turn_mixer_2_on", my_parameters.ST_MID_2_3, "Turn off mixer 2"),
        my_parameters.ST_MID_2_3: ("turn_mixer_2_off", my_parameters.ST_MIXER3, "Turn on mixer 3"),
        my_parameters.ST_MIXER3: ("turn_mixer_3_on", my_parameters.ST_MID_3_4, "Turn off mixer 3"),
        my_parameters.ST_MID_3_4: ("turn_mixer_3_off", my_parameters.ST_PUMP_IN, "Turn in pump on"),
        my_parameters.ST_PUMP_IN: ("turn_in_pump_on", my_parameters.ST_MID_4_5, "Turn in pump off", 20),
        my_parameters.ST_MID_4_5: ("turn_in_pump_off", my_parameters.ST_SELECTOR, "Selector"),
        my_parameters.ST_SELECTOR: ("turn_out_pump_on", my_parameters.ST_PUMP_OUT, "Turn on out pump"),
        my_parameters.ST_PUMP_OUT: ("turn_out_pump_on", my_parameters.ST_MID_6_7, "Turn out pump off", 20),
        my_parameters.ST_MID_6_7: ("turn_out_pump_off", my_parameters.ST_END_STATE, "Unselect"),
        my_parameters.ST_END_STATE: ("unselect_area", my_parameters.DONE, "Done"),
    }

    if state in actions:
        action, next_state, message = actions[state][:3]
        timeout = actions[state][3] if len(actions[state]) > 3 else None

        if command.data < 0 and not command.flag:
            if count % 10 == 0:
                getattr(command, action)()
            if count // 10 > 3:
                print(f"Timeout {message.lower()}")
                if state == my_parameters.ST_END_STATE:
                    my_parameters.status = next_state
                    flag = False
                count = 0
                state = next_state
        else:
            command.flag = 1 if command.data >= 0 else 0
            if timeout and count >= timeout * 10:
                getattr(command, action)()
                count = 0
                state = next_state
                command.flag = 0
            else:
                print(message, getattr(task, action.split('_')[1].lower()))
                getattr(command, action)()
                count = 0
                state = next_state

    count += 1
    return state, task, command, count, flag


class FSM:
    def __init__(self, fsm, task, command, flag=True, count=0):
        self.state = my_parameters.ST_IDLE
        self.count = count
        self.fsm = fsm
        self.task = task
        self.command = command
        self.flag = flag

    def run_fsm(self):
        self.state, self.task, self.command, self.count, self.flag = self.fsm(
            self.state, self.task, self.command, self.count, self.flag)

    def add(self):
        my_os.operation_system.add_process(self.run_fsm, 0, 1)

    def remove(self):
        my_os.operation_system.remove_process(self.run_fsm)

    def check(self):
        if not self.flag:
            self.remove()