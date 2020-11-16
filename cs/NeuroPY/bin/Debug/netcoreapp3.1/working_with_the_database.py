import pyodbc
import cv2
from PIL import Image
import io


# вывод всех строк из таблицы
def select_all_from_table(table_name):
    cursor.execute("SELECT COUNT(id) FROM `" + table_name + "`")
    number_of_id = cursor.fetchone()[0]
    cursor.execute("SELECT * FROM `" + table_name + "`")
    row = cursor.fetchall()
    for i in range(int(number_of_id)):
        line = row[i]
        print(str(line))


# занесение изображения в БД
def insert_img_in_DB(frame):
    cv2.imwrite('templage_frame.jpg', frame)
    return open('templage_frame.jpg', 'rb').read()


# взятие изображения из БД
def select_img_from_DB(sql_request):
    cursor.execute(sql_request)
    data = cursor.fetchone()
    file_like = io.BytesIO(data[0])
    img = Image.open(file_like)
    img.save('templage_frame.jpg')
    return cv2.imread('templage_frame.jpg')


def img_from_DB_with_data(data):
    file_like = io.BytesIO(data)
    img = Image.open(file_like)
    img.save('templage_frame.jpg')
    return cv2.imread('templage_frame.jpg')


# сжатие изображения
def image_compression(image, compression):
    height = image.shape[0]
    width = image.shape[1]
    output_width = int(width / compression)
    dim = (output_width, int(height * (float(output_width) / width)))
    image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    return image


"""
РАБОТА С ИЗОБРАЖЕНИЯМИ
"""

"""
#frame = cv2.imread('1.jpg')

# занесение изображения в БД
# cursor.execute("INSERT INTO `table`(id, user_name, picture) VALUES ('6', 'daunnnn', ?)", (insert_img_in_DB(frame)), )
# cnxn.commit()

# взятие изображения из БД
# frame2 = select_img_from_DB("SELECT picture FROM `table` WHERE id = 5")
"""
