#encoding:utf-8
import cv2
import os
import numpy as np
import easyocr
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
font = cv2.FONT_HERSHEY_SIMPLEX

distance = 15
threld = 120
path = "./tup" #文件夹目录
disDir = "./tup" # 目标目录
reader = easyocr.Reader(['en'])
list_data=os.listdir(path)
def handlerImg(imgFileName):
    imgPath = path + '/' + imgFileName
    src = cv2.imread(imgPath)
    height, width, channels = src.shape
    img = src[int(height / 2.1): int(height / 1.1), int(width / 4):int(width / 1.2)]
    # img = Image.fromarray(img).rotate(3)
    # img = np.array(img)
    h, w, c = img.shape
    # 图像灰度化处理
    grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    grayimg = np.zeros((h, w, 3), np.uint8)
    # print(h, w, c, img)
    for i in range(h):
       for j in range(w):
          if grayImage[i, j]> threld:
             grayimg[i, j] = np.uint8(0)
          else:
             grayimg[i, j] = np.uint8(255)

    # 显示图像
    kernel = np.ones((6, 6), np.uint8);
    eroded_img = cv2.erode(grayimg, kernel, iterations=1)
    # eroded_img = grayimg



    result = reader.readtext(eroded_img, allowlist='0123456789')
    resText = ''
    if len(result) > 0:
       for i in range(0, len(result)):
          resText+=result[i][1]
    filename = "{}/{}_num_{}.jpg".format(disDir,imgFileName, resText)
    cv2.imshow(filename, eroded_img)
    cv2.imwrite(filename, src)
    print("写入文件名:", filename)
    return resText


index=0
for imgFileName in list_data:
    if imgFileName.endswith('.jpg'):
        index += 1
        print("开始识别{}个：".format(index),  imgFileName)
        text = handlerImg(imgFileName)
        print("结果：", text)
print("全部识别结束")
# cv2.waitKey(0)
cv2.destroyAllWindows()

