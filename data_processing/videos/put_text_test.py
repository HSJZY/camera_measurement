#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 20:25:06 2018

@author: jiang
"""

#coding=utf-8
#import cv2
#import numpy as np
#from pylab import *

#font=cv2.FONT_HERSHEY_SIMPLEX#使用默认字体
#im=np.zeros((540,960,3),np.uint8)#新建图像，注意一定要是uint8
#img=cv2.putText(im,'直线编队过程',(0,40),font,1.2,(255,255,255),2)#添加文字，1.2表示字体大小，（0,40）是初始的位置，(255,255,255)表示颜色，2表示粗细
#cv2.imshow("image:",img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

# -*- coding: utf-8 -*- 
import cv2 
import numpy 
from PIL import Image, ImageDraw, ImageFont
  
img_OpenCV = cv2.imread('img/IMG_20180508_134820.jpg') 
 
img_PIL = Image.fromarray(cv2.cvtColor(img_OpenCV, cv2.COLOR_BGR2RGB))
# 字体 字体*.ttc的存放路径一般是： /usr/share/fonts/opentype/noto/ 查找指令locate *.ttc 
font = ImageFont.truetype('NotoSansCJK-Black.ttc', 40) 
# 字体颜色 
fillColor = (255,0,0) 
# 文字输出位置 
position = (100,100) 
# 输出内容 
str = '在图片上输出中文'
  
# 需要先把输出的中文字符转换成Unicode编码形式 
if not isinstance(str, unicode): 
    str = str.decode('utf8') 
  
draw = ImageDraw.Draw(img_PIL) 
draw.text(position, str, font=font, fill=fillColor) 
# 使用PIL中的save方法保存图片到本地 
# img_PIL.save('02.jpg', 'jpeg') 
  
# 转换回OpenCV格式 
img_OpenCV = cv2.cvtColor(numpy.asarray(img_PIL),cv2.COLOR_RGB2BGR) 
cv2.imshow("print chinese to image",img_OpenCV) 
cv2.waitKey() 
cv2.destroyAllWindows()
#cv2.imwrite('03.jpg',img_OpenCV)
