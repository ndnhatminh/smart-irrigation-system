import serial.tools.list_ports
import time

NONE = "None"


class UART:
    ser = NONE
    mess = ""

    def __init__(self) -> None:
        try:
            self.ser = serial.Serial(port=self.getPort(), baudrate=9600)
            print(self.ser)
            if self.ser == NONE:
                self.port_error = True
        except:
            self.ser = NONE
            self.port_error = True
            print("Error in serial")

    def getPort(self):
        ports = serial.tools.list_ports.comports()
        N = len(ports)
        commPort = NONE
        for i in range(0, N):
            port = ports[i]
            strPort = str(port)
            # print(strPort)
            if "USB" in strPort:
                splitPort = strPort.split(" ")
                commPort = (splitPort[0])
        return commPort
        # return "COM5"

    def ProcessData(self, data):
        pass

    def ReadSerial(self):
        bytesToRead = self.ser.inWaiting()
        if bytesToRead > 0:
            out = self.ser.read(bytesToRead)
            data_array = [b for b in out]
            if data_array[0] == 0:
                data_array.pop(0)
            print(data_array)
            if len(data_array) >= 7:
                array_size = len(data_array)
                value = data_array[array_size - 4] * 256 + data_array[array_size - 3]
                # print(value)
                return value
            else:
                return -1
        return -2
        
serialUART = UART()
# # for testing
# temp = UART()
# while True:
#     # temp.ser.write("hahahhaha".encode())
#     # temp.ReadSerial()
#     print(1)
#     time.sleep(1)
