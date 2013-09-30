import numpy as np

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
    im = np.zeros((imHeight, imWidth))
    for mRow in range(imHeight-1, -1, -1):
        for nCol in range(0, imWidth, 1):        
            im[mRow, nCol] = int.from_bytes(f.read(1), byteorder='little')
            
    # Close the file
    f.close()  
    return im
    
def my_imhist(im):
    vectIm = im.flatten()
    histArray = np.zeros(256)
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
    hist_1 = my_imhist(image_1)
    return (image_1, hist_1)
    
def point_operate(im, LUT):
    (imHeight, imWidth) = np.shape(im)
    imOut = np.zeros(np.shape(im))
    for i in range(imHeight):
        for j in range(imWidth):
            imOut[i,j] = LUT[ im[i,j] ]
    return imOut
        
    
    
        