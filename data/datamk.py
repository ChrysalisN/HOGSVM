import os
import glob

pospath = './images/pos_person'
negpath = './images/neg_person'
aimpath = [negpath,pospath]
for  i in range(2):
    if not os.path.exists(aimpath[i]):
        os.makedirs(aimpath[i])
    imgs = glob.glob(f'*_{i}.jpg')
    for j in imgs:
        os.system(f'cp {j} {aimpath[i]}/{j}')
        print(f'已完成图片{j}')
