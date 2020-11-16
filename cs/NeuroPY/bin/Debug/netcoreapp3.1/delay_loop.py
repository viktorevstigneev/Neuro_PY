import time

path = r"temp.txt"


def delay_record(value):
    while not open(path, "r"):
        time.sleep(1)
        pass
    file = open(path, "w")
    file.write(value)
    file.close()


def get_file_value():
    while not open(path, "r"):
        time.sleep(1)
        pass
    file = open(path, "r")
    value = file.read()
    file.close()
    return value
