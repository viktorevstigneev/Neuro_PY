import cv2


def connecting_to_the_camera():
    caps = {}
    i = 0
    ret = True
    # узнаём сколько камер подключено
    while ret:
        caps['plase' + str(i) + ''] = cv2.VideoCapture(i)
        ret, frame = caps['plase' + str(i) + ''].read()
        i += 1
    caps.pop('plase' + str(i - 1) + '')
    caps.pop('plase' + str(i - 2) + '')
    return caps

    # # Включаем камеру
    # cap = cv2.VideoCapture(0)
    # return cap
