from creating_an_image import creating_an_image
from connecting_to_the_camera import connecting_to_the_camera
from finding_a_person import finding_a_person
from delay_loop import delay_record
from delay_loop import get_file_value
import pyodbc
import os
import cv2
import ctypes
import win32process
import time

# hwnd = ctypes.windll.kernel32.GetConsoleWindow()
# if hwnd != 0:
#     ctypes.windll.user32.ShowWindow(hwnd, 0)
#     ctypes.windll.kernel32.CloseHandle(hwnd)
#     _, pid = win32process.GetWindowThreadProcessId(hwnd)
#     os.system('taskkill /PID ' + str(pid) + ' /f')

# запись в файл temp, для того чтобы c# продолжил работу
delay_record("loaded")

# чтобы знать в какую папку сохранять фото и нужно ли вообще заносить нового пользователя
new_person = None

while True:
    time.sleep(1)
    choice = get_file_value()
    if choice == "adding_a_new_face":
        while True:
            time.sleep(1)
            person_value = get_file_value()
            if person_value != "adding_a_new_face" and person_value != "":
                # подключаемся к БД
                conn_string = (
                    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
                    r'DBQ=./../bin/Database.mdb;')
                cnxn = pyodbc.connect(conn_string)
                cursor = cnxn.cursor()

                person_state = {'surname': None, 'name': None,
                                 'middle_name': None, 'group': None,
                                 'curator': None, }
                value = get_file_value().split(" ")
                k = 0
                for i in person_state.keys():
                    person_state[i] = value[k]
                    k += 1

                # добавляем человека в БД
                cursor.execute(
                    "INSERT INTO `known_person`(surname, `name`, middle_name, `group`, curator) VALUES ('" + person_state[
                        'surname'] + "','" + person_state['name'] + "','" + person_state['middle_name'] + "','" + person_state[
                        'group'] + "','" + person_state['curator'] + "')")
                cnxn.commit()

                # закрываем БД
                cnxn.close()

                # чтобы знать в какую папку сохранять изображения лица нового человека
                new_person = person_state['surname'] + ' ' + person_state['name'] + ' ' + person_state['middle_name'] + ',' + \
                             person_state['group'] + ',' + person_state['curator']

                # создаём папку
                os.mkdir("../demo/people/" + new_person)

                break
            elif person_value == "":
                break

    if (choice == "adding_a_new_face" and new_person) or choice == "recognation":
        caps = {}
        # Подключаем камеры
        if new_person is None:
            caps = connecting_to_the_camera()
        else:
            caps['add'] = cv2.VideoCapture(0)

        while True:
            # последовательно переключаемся между камерами
            for cap in caps.items():
                # имя камеры(место, где находится камера)
                place = cap[0]
                # делаем изображение и сохраняем его
                ret, frame = creating_an_image(cap[1])
                # находим на изображении человека
                finding_a_person(frame, new_person, place)
