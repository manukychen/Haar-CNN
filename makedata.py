def emptydir(dirname):  #清空資料夾
    if os.path.isdir(dirname):  #資料夾存在就刪除
        shutil.rmtree(dirname)
        sleep(2)  #需延遲,否則會出錯
    os.mkdir(dirname)  #建立資料夾

import cv2
import random
import glob
import shutil, os
from time import sleep

fontlist = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','J','K','L','M','N','P','Q','R','S','T','U','V','W','X','Y','Z']
print('開始建立訓練資料！')
emptydir('data')
for n in range(len(fontlist)):
    print('產生 data/' + fontlist[n] +' 資料夾')
    emptydir('data/' + fontlist[n])
    myfiles = glob.glob('platefont/' + fontlist[n] + '/*.jpg')
    for index, f in enumerate(myfiles):
        pic_total = 500  #每個文字檔案數
        pic_each = int(pic_total / len(myfiles)) + 1
        for i in range(pic_each):  #i 為檔案名稱
            img = cv2.imread(f)
            for j in range(20):  #加入指定數量雜點
                x = random.randint(0, 17)  #以亂數設定位置
                y = random.randint(0, 37)
                cv2.circle(img, (x, y), 1, (0,0,0), -1)  #畫點
            cv2.imwrite('data/' + fontlist[n] + '/{:0>4d}.jpg'.format(index*pic_each+i+1), img)  #存檔
print('建立訓練資料結束！')
