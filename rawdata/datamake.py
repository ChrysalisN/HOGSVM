import os 
from PIL import Image

if not os.path.exists('../data/'):
	os.mkdir('../data')
imgs = os.listdir()
imgs = [i for i in imgs if '.jpg' in i]
for i in imgs:
	img = Image.open(i)
	img = img.resize((120,120))
	img.save(f'../data/{i}')
	print(f'已完成第{i}张图片')
