from my_parameters import crc_lists

class CRC_MOD_BUS:
    crc_lists = dict()

    def __init__(self, crc_lists: dict) -> None:

        self.crc_lists = crc_lists
        pass

    def calculate(self, para: list) -> list:
        temp_crc = 0xFFFF
        for idx in para:
            temp_crc ^= idx
            for jdx in range(8):
                if (temp_crc & 0x0001):
                    temp_crc = temp_crc >> 1
                    temp_crc ^= 0xA001
                else:
                    temp_crc = temp_crc >> 1

        crc_high = temp_crc >> 8
        crc_low = temp_crc % 256
        return [crc_low, crc_high]
        # return [crc_high, crc_low]

    def export(self, name: str) -> list:
        crc_check = self.calculate(self.crc_lists[name])
        crc_format = self.crc_lists[name] + crc_check
        return crc_format

crc_calc = CRC_MOD_BUS(crc_lists)
# for testing   
# from my_parameters import crc_lists
# crc_calc = CRC_MOD_BUS(crc_lists)
# print(crc_calc.export("MIXER1_ON"))

