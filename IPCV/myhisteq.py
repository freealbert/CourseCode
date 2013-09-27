# -*- coding:utf-8 -*-

import matplotlib.pylab as pl
import matplotlib.cm as cm
import numpy as np
from PIL import Image

def myhisteq(image_0):
    # 原图像是uint8
    (M,N) = image_0.shape
    # 统计原图每级灰度出现的概率
    hist_0 ,x_0 = np.histogram(image_0.flatten(),bins=256,range=(0,256))
    prob_0 = hist_0/float(M*N)
    # 计算累计灰度概率s_k
    # s_1的索引号为原始的灰度值，值为应该变换成的灰度级。
    # s_1的索引号和值构成了灰度变化曲线
    # s_2将s_1整数化
    s_1 = np.asarray([0.0]*256)
    for i in range(256):
        for j in range(i+1):
            s_1[i] += prob_0[j] 
    s_2 = np.round(s_1*255)
        
    image_1 = image_0.copy()
    flat_image_1 = image_1.flatten()
    flat_image_0 = image_0.flatten()
    for n in range(256):
        flat_image_1[np.argwhere(flat_image_0==n)] = s_2[n]
    image_1 = flat_image_1.reshape(M,N)
    hist_1,x_1 = np.histogram(image_1.flatten(),bins=256,range=(0,256))
    return(image_1,hist_1,hist_0,x_1[:-1],x_0[:-1])

fileName = 'D:\\DYM Exp. Images\\lena_gray.bmp'
im = np.asarray(Image.open(fileName).convert('L'))
(eqIm, eqHist, origHist, eqX, origX) = myhisteq(im)

fig = pl.figure()
ax1 = fig.add_subplot(221)
ax1.plot(origX, origHist)

ax2 = fig.add_subplot(222)
ax2.plot(eqX, eqHist)

ax3 = fig.add_subplot(223)
ax3.imshow(im, cmap=cm.gray,norm=pl.Normalize(vmin=0,vmax=255))

ax4 = fig.add_subplot(224)
ax4.imshow(eqIm, cmap=cm.gray,norm=pl.Normalize(vmin=0,vmax=255))

fig.savefig('haha.jpg')
fig.show()