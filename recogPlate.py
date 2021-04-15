def emptydir(dirname):  #清空資料夾
    if os.path.isdir(dirname):  #資料夾存在就刪除
        shutil.rmtree(dirname)
        sleep(2)  #需延遲,否則會出錯
    os.mkdir(dirname)  #建立資料夾

from keras.models import load_model
from PIL import Image
import numpy as np
import cv2
import shutil, os
from time import sleep 

labels = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','J','K','L','M','N','P','Q','R','S','T','U','V','W','X','Y','Z']  #標籤值
#擷取車牌
imgname = '3M6605.jpg'
dirname = 'recogdata'
emptydir(dirname)
img = cv2.imread('predictPlate/' + imgname)
detector = cv2.CascadeClassifier('haar_carplate.xml')
signs = detector.detectMultiScale(img, scaleFactor=1.1, minNeighbors=4, minSize=(20, 20))
if len(signs) > 0 :
    for (x, y, w, h) in signs:          
        image1 = Image.open('predictPlate/' + imgname)
        image2 = image1.crop((x, y, x+w, y+h))
        image3 = image2.resize((140, 40), Image.ANTIALIAS)
        image3.save('tem.jpg')
        image4 = cv2.imread('tem.jpg')
        gray = cv2.cvtColor(image4, cv2.COLOR_RGB2GRAY)
        _, img_thre = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
        cv2.imwrite('tem.jpg', img_thre)
    #分割文字
    img_tem = cv2.imread('tem.jpg')
    gray = cv2.cvtColor(img_tem, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)  #轉為黑白
    contours1 = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  #尋找輪廓
    contours = contours1[1]  #取得輪廓
    letter_image_regions = []  #文字圖形串列
    for contour in contours:  #依序處理輪廓
        (x, y, w, h) = cv2.boundingRect(contour)  #單一輪廓資料
        letter_image_regions.append((x, y, w, h))  #輪廓資料加入串列
    letter_image_regions = sorted(letter_image_regions, key=lambda x: x[0])  #按X坐標排序
    #存檔
    i=1
    for letter_bounding_box in letter_image_regions:  #依序處理輪廓資料
        x, y, w, h = letter_bounding_box
        if w>=5 and h>32 and h<40:  #長度>6且高度在30-48才是文字
            letter_image = gray[y:y+h, x:x+w]  #擷取圖形
            letter_image = cv2.resize(letter_image, (18, 38))
            cv2.imwrite(dirname + '/{}.jpg'.format(i), letter_image)  #存檔
            i += 1
    #辨識車牌
    datan = 0  #車牌文字數,即檔案數
    for fname in os.listdir(dirname):
        if os.path.isfile(os.path.join(dirname, fname)):
            datan += 1
    tem_data = []
    for index in range(1, (datan+1)):  #讀取預測資料
        tem_data.append((np.array(Image.open("recogdata/" + str(index) +".jpg")))/255.0)
    real_data = np.stack(tem_data)
    real_data1 = np.expand_dims(real_data, axis=3)  #(7,38,18,1)
    model = load_model("carplate_model.hdf5")  #讀取模型
    predictions = model.predict_classes(real_data1)  #預測資料
    print('車牌號碼為：')
    for i in range(len(predictions)):  #顯示結果
        print(labels[int(predictions[i])], end='') 
else:
    print('無法擷取車牌！')
os.remove('tem.jpg')