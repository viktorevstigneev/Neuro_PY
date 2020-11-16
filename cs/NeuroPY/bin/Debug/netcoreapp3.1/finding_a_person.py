import numpy as np
import cv2
from face_recognition import faces

classes_for_people = ["background", "aeroplane", "bicycle", "bird", "boat",
                      "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
                      "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
                      "sofa", "train", "tvmonitor"]

# Жёлтый цвет для образа человека
color_for_people = [0, 255, 255]

# загрузка модели для распознования образа человека
net = cv2.dnn.readNetFromCaffe('../bin/model/MobileNetSSD_deploy.prototxt.txt',
                               '../bin/model/MobileNetSSD_deploy.caffemodel')


def finding_a_person(frame, new_person, place):
    # создаём копию кадра для рисования рамок
    frame_with_people = frame.copy()
    # захватываем размеры кадра и преобразовываем его в большой двоичный объект
    (h, w) = frame.shape[:2]
    resized = cv2.resize(frame, (300, 300))
    blob = cv2.dnn.blobFromImage(resized, 0.007843, (300, 300), (104, 117, 124))

    # передаём большой двоичный объект через сеть и получаем обнаружение и предсказание
    net.setInput(blob)
    detections = net.forward()

    # цикл по детекции
    for i in np.arange(0, detections.shape[2]):
        # извлекаем уверенность (то есть вероятность), связанную с предсказанием
        confidence = detections[0, 0, i, 2]

        # отфильтруем слабые обнаружения, убедившись, что "предсказание" больше, чем минимальная уверенность
        if confidence > 0.2:
            # извлечение индекса из ' detections`,
            idx = int(detections[0, 0, i, 1])
            # если был найден человек
            if classes_for_people[idx] == 'person':
                # затем вычисляем (x, y) - координаты ограничивающего
                # прямоугольника для объекта
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                # нарисуем рамку на кадре
                cv2.rectangle(frame_with_people, (startX, startY), (endX, endY),
                              (0, 255, 255, 1), 2)

                # сохраняем общий кадр
                cv2.imwrite('../demo/recognition_video/input/frame_with_finding_people.jpg', frame_with_people)

    faces(frame, frame_with_people, new_person, place)
