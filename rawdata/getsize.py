import os
import pylab as plt
import numpy as np

ls = os.listdir()
ls = [i for i in ls if '.jpg' in i]
f = open('img_shape.txt','w')
Fir = True
for i in ls:
    if Fir:
        Fir = False
    else:
        f.write('\n')
        
    img = plt.imread(i)
    x,y=img.shape[:2]
    f.write(i+'\t'+str(x)+'\t'+str(y))
f.close()
