def emptydir(dirname):  #清空資料夾
    if os.path.isdir(dirname):  #資料夾存在就刪除
        shutil.rmtree(dirname)
        sleep(2)  #需延遲,否則會出錯
    os.mkdir(dirname)  #建立資料夾

import cv2
import shutil, os
from time import sleep

emptydir('cropMono')
image = cv2.imread('cropPlate/MRR7715.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  #灰階
_,thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)  #轉為黑白
contours1 = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  #尋找輪廓
contours = contours1[1]  #取得輪廓
letter_image_regions = []  #文字圖形串列
for contour in contours:  #依序處理輪廓
    (x, y, w, h) = cv2.boundingRect(contour)  #單一輪廓資料
    letter_image_regions.append((x, y, w, h))  #輪廓資料加入串列
letter_image_regions = sorted(letter_image_regions, key=lambda x: x[0])  #按X坐標排序
print(letter_image_regions)
#存檔
i=1
for letter_bounding_box in letter_image_regions:  #依序處理輪廓資料
    x, y, w, h = letter_bounding_box
    if w>=5 and h>32 and h<40:  #長度>6且高度在33-39才是文字
        letter_image = gray[y:y+h, x:x+w]  #擷取圖形
        letter_image = cv2.resize(letter_image, (18, 38))
        cv2.imwrite('cropMono/{}.jpg'.format(i), letter_image)  #存檔
        i += 1
