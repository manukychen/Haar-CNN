import cv2
import os.path
import numpy as np
from imutils import paths
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.layers.core import Flatten, Dense

imagedir = "data"  #訓練資料
modelname = "carplate_model.hdf5"  #模型名稱
data = []  #資料串列
labels = []  #標籤串列

#讀取資料
for image_file in paths.list_images(imagedir):
    image = cv2.imread(image_file)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  #轉為灰階
    label = image_file.split(os.path.sep)[-2]  #擷取文字資料夾名稱
    data.append(image)  #加入圖形
    labels.append(label)  #加入標籤
data = np.array(data)  #轉換為numpy array
labels = np.array(labels)

#訓練資料佔85%
(X_train, X_test, Y_train, Y_test) = train_test_split(data, labels, test_size=0.15, random_state=0)
#標準化資料
X_train_normalize=X_train.reshape(X_train.shape[0],38,18,1).astype("float") / 255.0
X_test_normalize=X_test.reshape(X_test.shape[0],38,18,1).astype("float") / 255.0
#轉換標籤為one-hot
lb = LabelBinarizer().fit(Y_train)
Y_train_OneHot = lb.transform(Y_train)
Y_test_OneHot = lb.transform(Y_test)

#建立模型
model = Sequential()
#神經網路
model.add(Conv2D(20, (5, 5), padding="same", input_shape=(38, 18, 1), activation="relu"))
model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
model.add(Conv2D(50, (5, 5), padding="same", activation="relu"))
model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
model.add(Flatten())
model.add(Dense(500, activation="relu"))
model.add(Dense(34, activation="softmax"))  #34類
model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
#開始訓練
model.fit(X_train_normalize, Y_train_OneHot, validation_split=0.2, batch_size=32, epochs=10, verbose=1)
model.save(modelname)  #儲存模型

#準確率
scores = model.evaluate(X_train_normalize , Y_train_OneHot)
print(scores[1])
scores2 = model.evaluate(X_test_normalize , Y_test_OneHot)
print(scores2[1])
