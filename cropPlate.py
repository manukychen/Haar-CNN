def emptydir(dirname):  #清空資料夾
    if os.path.isdir(dirname):  #資料夾存在就刪除
        shutil.rmtree(dirname)
        sleep(2)  #需延遲,否則會出錯
    os.mkdir(dirname)  #建立資料夾

import cv2
from PIL import Image
import glob
import shutil, os
from time import sleep

print('開始擷取車牌！')
print('無法擷取車牌的圖片：')
dstdir = 'cropPlate'
myfiles = glob.glob("realPlate\*.JPG")
emptydir(dstdir)
for imgname in myfiles:
    filename = (imgname.split('\\'))[-1]  #取得檔案名稱
    img = cv2.imread(imgname)  #讀入圖形
    detector = cv2.CascadeClassifier('haar_carplate2.xml')
    signs = detector.detectMultiScale(img, scaleFactor=1.1, minNeighbors=4, minSize=(20, 20))  #框出車牌
    #割取車牌
    if len(signs) > 0 :
        for (x, y, w, h) in signs:          
            image1 = Image.open(imgname)
            image2 = image1.crop((x, y, x+w, y+h))  #擷取車牌圖形
            image3 = image2.resize((140, 40), Image.ANTIALIAS)  #轉換尺寸為140X40
            image3.save(dstdir + '/tem.jpg')
            image4 = cv2.imread(dstdir + '/tem.jpg')  #以opencv讀車牌檔
            img_gray = cv2.cvtColor(image4, cv2.COLOR_RGB2GRAY)  #灰階
            _, img_thre = cv2.threshold(img_gray, 100, 255, cv2.THRESH_BINARY)  #黑白
            cv2.imwrite(dstdir + '/'+ filename, img_thre)
    else:
        print(filename)

os.remove(dstdir + '/tem.jpg')  #移除暫存檔
print('擷取車牌結束！')
