# -*- coding: utf-8 -*-
import numpy as np
import pylab as pl
import matplotlib.cm as cm
# fileName = 'D:\\DYM Exp. Images\\lena512.bmp'
fileName = 'D:\\DYM Exp. Images\\lena_gray.bmp'
f = open(fileName, 'rb')
    
f.seek(0)     
if f.read(2)!= b'BM':
    print('BMP file Please')
 
f.seek(10)
imDataOffset = int.from_bytes(f.read(4), byteorder='little')

# f.seek(14)
# infoHeaderLength = int.from_bytes(f.read(4), byteorder='little')

f.seek(18)
imWidth = int.from_bytes(f.read(4), byteorder='little')
imHeight = int.from_bytes(f.read(4), byteorder='little')

f.seek(imDataOffset)
im = np.zeros((imHeight, imWidth))
for mRow in range(imHeight-1, -1, -1):
    for nCol in range(0, imWidth, 1):        
        im[mRow, nCol] = int.from_bytes(f.read(1), byteorder='little')

f.close()  
fig = pl.figure()
ax = fig.add_subplot(111)
ax.imshow(im, cmap=cm.gray,norm=pl.Normalize(vmin=0,vmax=255))
fig.savefig('haha.jpg')

fig.show()


