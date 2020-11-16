import cv2


def creating_an_image(cap):
    # Делаем снимок
    ret, frame = cap.read()

    # Записываем в файл
    cv2.imwrite('../demo/recognition_video/input/frame.jpg', frame)

    return ret, frame
