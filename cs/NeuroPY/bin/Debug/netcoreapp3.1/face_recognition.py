from mtcnn.mtcnn import MTCNN
import statistics
import cv2
import numpy
import keras
import imutils
import datetime
import pyodbc
import sys
import os
from working_with_the_database import image_compression
from delay_loop import delay_record

# Создание сети нахождения лиц
detector = MTCNN()

# Загрузка модели сети определения лиц
embedder = keras.models.load_model('../bin/model/facenet_keras.h5', compile=False)

# Подключение БД
conn_string = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    r'DBQ=./../bin/Database.mdb;')
cnxn = pyodbc.connect(conn_string)
cursor = cnxn.cursor()


# получение дистанции лица
def get_distance(model, face):
    face = face.astype('float32')
    face = (face - face.mean()) / face.std()
    face = numpy.expand_dims(face, axis=0)
    return embedder.predict(face)[0]


# создание базы с известными лицами
base = {}

# узнаём сколько всего людей в БД
cursor.execute("SELECT COUNT(id) FROM `known_person`")
number_of_id = cursor.fetchone()[0]

cursor.execute("SELECT * FROM `known_person`")

# берём информацию о всех людях
row = cursor.fetchall()

# "пробегаемся" по каждому человеку
for i in range(int(number_of_id)):

    # записываем данные о человеке
    # Делаем ФИО из фамилии, имени и отчества человека, записываем группу и куратора
    person_state = row[i][1] + ' ' + row[i][2] + ' ' + row[i][3] + ',' + row[i][4] + ',' + row[i][5]

    base[person_state] = []

    # пробегаемся по каждому файлу в папке человека
    for file in os.listdir('../demo/people/' + person_state):

        # если файл с расширением jpg
        if file.endswith('.jpg'):

            # загрузка изображение с лицом
            image = cv2.imread('../demo/people/' + person_state + '/' + file)

            # Получение списка лиц с координатами и значением уверенности
            faces_boxes = detector.detect_faces(image)

            # Работа с лицами
            if faces_boxes:
                # Сохранение суммы евклидова пространства
                base[person_state].append(get_distance(embedder, image))

# Для нумерации изображений при занесении нового человека
global new_person_frame_id

new_person_frame_id = 0

name_first_frame = True


def faces(frame, frame_with_faces, new_person, place):
    # Увеличение/уменьшение наименьшей стороны изображения до 1000 пикселей

    global new_person_frame_id, name_first_frame
    if frame.shape[0] < frame.shape[1]:
        frame = imutils.resize(frame, height=1000)

        # Копия изображения для рисования рамок на нём
        frame_with_faces = imutils.resize(frame_with_faces, height=1000)
    else:
        frame = imutils.resize(frame, width=1000)

        # Копия изображения для рисования рамок на нём
        frame_with_faces = imutils.resize(frame_with_faces, height=1000)

    # Получить размеры изображения
    image_size = numpy.asarray(frame.shape)[0:2]

    # Получение списка лиц с координатами и значением уверенности
    faces_boxes = detector.detect_faces(frame)

    # Замена BGR на RGB (так находит в два раза больше лиц)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    name_faces = ''

    none_person_id = 0
    none_person = ''

    # Работа с лицами
    if faces_boxes:

        for face_box in faces_boxes:

            # Координаты лица
            x, y, w, h = face_box['box']

            # Выравнивание лица
            d = h - w  # Разница между высотой и шириной
            w = w + d  # Делаем изображение квадратным
            x = numpy.maximum(x - round(d / 2), 0)
            x1 = numpy.maximum(x, 0)
            y1 = numpy.maximum(y, 0)
            x2 = numpy.minimum(x + w, image_size[1])
            y2 = numpy.minimum(y + h, image_size[0])

            # Получение картинки с лицом
            cropped = frame[y1:y2, x1:x2, :]
            face_image = cv2.resize(cropped, (160, 160), interpolation=cv2.INTER_AREA)

            # Получение дистанции
            distance = get_distance(embedder, face_image)

            # Координаты лица
            x, y, w, h = face_box['box']

            # Отступы для увеличения рамки
            d = h - w  # Разница между высотой и шириной
            w = w + d  # Делаем изображение квадратным
            x = numpy.maximum(x - round(d / 2), 0)
            x1 = numpy.maximum(x - round(w / 4), 0)
            y1 = numpy.maximum(y - round(h / 4), 0)
            x2 = numpy.minimum(x + w + round(w / 4), image_size[1])
            y2 = numpy.minimum(y + h + round(h / 4), image_size[0])

            # если уверенность сети в процентах что это лицо больше указанной (0.99)
            if face_box['confidence'] > 0.80:

                identity = None
                min_difference = 8
                min_median = 8
                faces = {}

                # Сверка расстояний с известными лицами
                for person, base_distances in base.items():
                    faces[person] = []
                    for base_distance in base_distances:
                        difference = numpy.linalg.norm(base_distance - distance)
                        if difference < min_difference:
                            print('difference - ' + str(difference))
                            faces[person].append(difference)

                # Нахождение минимальной мидианы среди проголосовавших лиц
                if faces:
                    for person, items in faces.items():
                        # Идентификация только участвуют два и больше лиц
                        if items and len(items) >= 2:
                            print(person)
                            print(items)
                            median = statistics.median(items)
                            if median < min_median:
                                print('median - ' + str(median))
                                min_median = median
                                identity = person

                # если лицо опознано
                if identity and new_person is None:
                    identity_array = identity.split(',')

                    full_name = str(identity_array[0])
                    group = str(identity_array[1])
                    curator = str(identity_array[2])

                    name_faces += full_name + '(' + group + ',' + curator + ')' + ';'

                    # Пишем имя под лицом
                    cv2.putText(frame_with_faces, full_name, (x1 + 10, y2 + 20),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    # Пишем группу под лицом
                    cv2.putText(frame_with_faces, group, (x1 + 10, y2 + 35),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    # Пишем куратора под лицом
                    cv2.putText(frame_with_faces, curator, (x1 + 10, y2 + 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                    # Рисует зелёный квадрат на картинке по координатам
                    cv2.rectangle(frame_with_faces, (x1, y1), (x2, y2), (0, 255, 0, 1), 2)

                # если лицо не опознонно
                else:

                    # если это занесение нового лица в БД
                    if new_person and new_person_frame_id < 30:
                        new_person_frame_id += 1

                        # сохраняем в папку новое лицо
                        cv2.imwrite(
                            '../demo/people/' + new_person + '/' + str(new_person_frame_id)
                            + '.jpg', face_image)
                        if new_person_frame_id == 30:
                            sys.exit()

                    # если это не занесение нового лица в БД
                    else:
                        none_person_id += 1
                        name_faces += 'NonePerson' + str(none_person_id) + ';'

                        # пишем имя под лицом
                        cv2.putText(frame_with_faces, 'NonePerson' + str(none_person_id), (x1 + 10, y2 + 20),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

                        # рисуем красный квадрат на картинке по координатам
                        cv2.rectangle(frame_with_faces, (x1, y1), (x2, y2), (0, 0, 255, 1), 2)

                # если это не занесение нового человека в БД, то сохраняем кадр с (не)распознанными лицами
                if new_person is None:
                    now = datetime.datetime.now()

                    date = str(now.day) + '.' + str(now.month) + '.' + str(now.year)
                    time = str(now.hour) + ':' + str(now.minute) + ':' + str(now.second)

                    # заносим в БД данные о кадре
                    cursor.execute("INSERT INTO `frames`(`time`,`date`,`place`,`people`) VALUES (?,?,?,?)",
                                   (time, date, place, name_faces))
                    cnxn.commit()

                    # берём имя кадра
                    cursor.execute("SELECT MAX(frame) FROM `frames`")
                    name_frame = cursor.fetchone()[0]

                    # чтобы знать с какого файлка начинать "Отображение" в C#
                    if name_first_frame:
                        name_first_frame = False
                        delay_record(str(name_frame))

                    # Уменьшаем размер изображения с распознаными лицами в 1.5 раза и сохраняем его
                    cv2.imwrite('../demo/recognition_video/output/frames/' + str(name_frame) + '.jpg',
                                image_compression(frame_with_faces, 1.5))
