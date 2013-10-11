# import numpy as np
from numpy import *

def bin_imread(fileName):
    f = open(fileName, 'rb') 
     
    # Check whether it is a BMP file      
    f.seek(0)     
    if f.read(2)!= b'BM':
        print('BMP file Please')
        
    # Get the Offset where the real image data begins
    f.seek(10)
    imDataOffset = int.from_bytes(f.read(4), byteorder='little')
    
    # f.seek(14)
    # infoHeaderLength = int.from_bytes(f.read(4), byteorder='little')
    
    # Get image Width and Height
    f.seek(18)
    imWidth = int.from_bytes(f.read(4), byteorder='little')
    imHeight = int.from_bytes(f.read(4), byteorder='little')
    
    # Get the image matrix
    f.seek(imDataOffset)
#     im = np.zeros((imHeight, imWidth))
    im = zeros((imHeight, imWidth))
    for mRow in range(imHeight-1, -1, -1):
        for nCol in range(0, imWidth, 1):        
            im[mRow, nCol] = int.from_bytes(f.read(1), byteorder='little')
            
    # Close the file
    f.close()  
    return im
    
def my_imhist(im):
    vectIm = im.flatten()
#     histArray = np.zeros(256)
    histArray = zeros(256)
    for i in range(len(vectIm)):
        histArray[ vectIm[i] ] += 1
    return histArray
        
def my_histeq(image_0):
    # 原图像是uint8
    (M,N) = image_0.shape
    # 统计原图每级灰度出现的概率
    hist_0 = my_imhist(image_0)
    prob_0 = hist_0/float(M*N)
    # 计算累计灰度概率s_k
    # s_1的索引号为原始的灰度值，值为应该变换成的灰度级。
    # s_1的索引号和值构成了灰度变化曲线
    # s_2将s_1整数化
#     s_1 = np.asarray([0.0]*256)
    s_1 = asarray([0.0]*256)
    for i in range(256):
        for j in range(i+1):
            s_1[i] += prob_0[j] 
#     s_2 = np.round(s_1*255)
    s_2 = round(s_1*255)
        
    image_1 = image_0.copy()
    flat_image_1 = image_1.flatten()
    flat_image_0 = image_0.flatten()
    for n in range(256):
#         flat_image_1[np.argwhere(flat_image_0==n)] = s_2[n]
        flat_image_1[argwhere(flat_image_0==n)] = s_2[n]
    image_1 = flat_image_1.reshape(M,N)
    hist_1 = my_imhist(image_1)
    return (image_1, hist_1)
    
def point_operate(im, LUT):
#     (imHeight, imWidth) = np.shape(im)
#     imOut = np.zeros(np.shape(im))
    (imHeight, imWidth) = shape(im)
    imOut = np.zeros(shape(im))
    for i in range(imHeight):
        for j in range(imWidth):
            imOut[i,j] = LUT[ im[i,j] ]
    return imOut
        
def image_minus_abs(im1, im2):
    if im1.shape != im2.shape:
        print('Error !!! Image sizes must be same.')
    imOut = abs(im1 - im2)
    return imOut

def rotate_bilinear_backward_interp(im, alpha):
    beta = -alpha
    imOut = zeros(im.shape)
    (imRows, imCols) = im.shape
    cos_beta_x1_list = cos(beta) * arange(imRows)  
    sin_beta_y1_list = sin(beta) * arange(imCols)
    sin_beta_x1_list = sin(beta) * arange(imRows)
    cos_beta_y1_list = cos(beta) * arange(imCols)
    for x1 in range(imRows):        
        for y1 in range(imCols):            
            x0 = cos_beta_x1_list[x1] + sin_beta_y1_list[y1]            
            y0 = -sin_beta_x1_list[x1] + cos_beta_y1_list[y1]
            if x0 >= 0 and x0 < imRows-1 and y0 >= 0 and y0 < imCols-1:
                # 用双线性插值求出 整数的x0, y0， 
                # 并把im[x0,y0]的值（灰度）赋给imOut[x1,y1]
                a = floor(x0)
                b = floor(y0)
                f_x_b = (x0-a)*im[a+1,b] + (a+1-x0)*im[a,b]
                f_x_b_plus_1 = (x0-a)*im[a+1,b+1] + (a+1-x0)*im[a,b+1]
                imOut[x1,y1] = (b+1-y0)*f_x_b + (y0-b)*f_x_b_plus_1
    return imOut
                
# haha = image_minus_abs(im,im)  
import pylab as pl  
import matplotlib.cm as cm
im = bin_imread(fileName)    
im = zeros((128,128))
im[32:96, 32:96] = 255
imOut = rotate_bilinear_backward_interp(im, 45/180*pi)
fig = pl.figure()
ax = fig.add_subplot(111)
ax.imshow(imOut, cmap=cm.gray,norm=pl.Normalize(vmin=0,vmax=255))
fig.show()