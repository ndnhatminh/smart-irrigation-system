crc_lists = {
    "MIXER1_ON": [1, 6, 0, 0, 0, 255],
    "MIXER1_OFF": [1, 6, 0, 0, 0, 0],
    "MIXER2_ON": [2, 6, 0, 0, 0, 255],
    "MIXER2_OFF": [2, 6, 0, 0, 0, 0],
    "MIXER3_ON": [3, 6, 0, 0, 0, 255],
    "MIXER3_OFF": [3, 6, 0, 0, 0, 0],
    "SELECTOR1_ON": [4, 6, 0, 0, 0, 255],
    "SELECTOR1_OFF": [4, 6, 0, 0, 0, 0],
    "SELECTOR2_ON": [5, 6, 0, 0, 0, 255],
    "SELECTOR2_OFF": [5, 6, 0, 0, 0, 0],
    "SELECTOR3_ON": [6, 6, 0, 0, 0, 255],
    "SELECTOR3_OFF": [6, 6, 0, 0, 0, 0],
    "PUMP_IN_ON": [7, 6, 0, 0, 0, 255],
    "PUMP_IN_OFF": [7, 6, 0, 0, 0, 0],
    "PUMP_OUT_ON": [8, 6, 0, 0, 0, 255],
    "PUMP_OUT_OFF": [8, 6, 0, 0, 0, 0],
    "SOIL_TEMPERATURE":[10 ,3, 0, 6, 0, 1],
    "SOIL_HUMIDITY": [10, 3, 0, 7, 0, 1]
}

# Speed of the mixer (ml/s)
SPEED = 2

# for my_server.py
LIST_OF_FEEDS = ["iot-mobile", "iot-gateway", "iot-temperature", "iot-humidity"]
HOST = "io.adafruit.com"
USER = "nemo2602"
PASSWORD = ""

#for state machine
ST_IDLE = 0
ST_MIXER1 = 1
ST_MIXER2 = 2
ST_MIXER3 = 3
ST_PUMP_IN = 4
ST_SELECTOR = 5
ST_PUMP_OUT = 6
ST_END_STATE = 7

ST_MID_1_2 = 8
ST_MID_2_3 = 9
ST_MID_3_4 = 10
ST_MID_4_5 = 11
ST_MID_5_6 = 12
ST_MID_6_7 = 13

#for Task
WAITING = 0
RUNNING = 1
DONE = 2

status = WAITING