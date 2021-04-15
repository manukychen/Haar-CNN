def emptydir(dirname):  #清空資料夾
    if os.path.isdir(dirname):  #資料夾存在就刪除
        shutil.rmtree(dirname)
        sleep(2)  #需延遲,否則會出錯
    os.mkdir(dirname)  #建立資料夾

import glob
import shutil, os
from time import sleep

print('開始建立文字庫！')
emptydir('platefont')
fontlist = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','J','K','L','M','N','P','Q','R','S','T','U','V','W','X','Y','Z']
for i in range(len(fontlist)):  #建立文字資料夾
    emptydir('platefont/' + fontlist[i])
dirs = os.listdir('cropNum')  #讀取所有檔案及資料夾
picnum = 1  #圖片記數器,讓檔名不會重複
for d in dirs:
    if os.path.isdir('cropNum/' + d):  #只處理資料夾
        myfiles = glob.glob('cropNum/' + d + '/*.jpg')
        for i, f in enumerate(myfiles):
            shutil.copyfile(f, 'platefont/{}/{}.jpg'.format(d[i], picnum))  #存入對應資料夾
            picnum += 1
print('建立文字庫結束！')
