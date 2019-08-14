import numpy as np 
from skimage.transform import pyramid_gaussian
from imutils.object_detection import non_max_suppression
import imutils
from sklearn.externals import joblib
import cv2
from config import *
from skimage import color
import matplotlib.pyplot as plt 
import os 
import glob
from PIL import Image
from matplotlib import patches
from multiprocessing import Pool
import time 

hog = cv2.HOGDescriptor(win_size,block_size,block_stride,cell_size,num_bins)

def sliding_window(image, window_size, step_size):
	'''
	This function returns a patch of the input 'image' of size 
	equal to 'window_size'. The first image returned top-left 
	co-ordinate (0, 0) and are increment in both x and y directions
	by the 'step_size' supplied.

	So, the input parameters are-
	image - Input image
	window_size - Size of Sliding Window 
	step_size - incremented Size of Window

	The function returns a tuple -
	(x, y, im_window)
	'''
	for y in range(0, image.shape[0], step_size[1]):
		for x in range(0, image.shape[1], step_size[0]):
			yield (x, y, image[y: y + window_size[1], x: x + window_size[0],:])

def detect_multi(im,scale_size,min_wdw_sz,step_raw,clf):
	detections = []
	scale_size = scale_size/10.
	print('The Scale size is ',scale_size)
	window_size = [int(i*scale_size) for i in min_wdw_sz]
	step_size = [int(i*scale_size) for i in step_raw]
	num = 0
	for (x, y, im_window) in sliding_window(im, window_size, step_size):
		im_window = Image.fromarray(im_window)
		im_window = im_window.resize((img_avg,img_avg))
		im_window = np.array(im_window)
		num+=1
		print(f'已检测{num}个窗口,现在是\t{x},{y}')
		fd = hog.compute(im_window,(img_avg,img_avg))
		fd = fd.reshape(1, -1)
		pred = clf.predict(fd)
		if pred == 1:
			cdf = clf.decision_function(fd)
			if cdf>=cdf_threshold:
				detections.append((x,y,cdf,window_size[0],window_size[1]))		
	return detections

def coincide(rects):
	tset = []
	rec = rects.pop()
	#for s in rects:
	#	if 

def save_wrong(im,found):
	img_cut = im.copy()
	img_cut = cv2.cvtColor(img_cut,cv2.COLOR_BGR2RGB)
	if not os.path.exists('../rawdata/temp/0'):
		os.makedirs('../rawdata/temp/0')
	num = os.listdir('../rawdata/temp')
	num = [i for i in num if '.jpg' not in i]
	num = [eval(i) for i in num ]
	num = max(num)+1
	os.mkdir(f'../rawdata/temp/{num}')
	path = f'../rawdata/temp/{num}/'
	count = os.listdir('../rawdata/')
	count = [i for i in count if '_0.jpg' in i and 'train' not in i ]
	count = [eval(i.split('_')[0]) for i in count]
	count = max(count)
	for i in found:
		count += 1
		img_save = img_cut[i[1]:i[1]+i[3],i[0]:i[0]+i[2],:]
		img_save = Image.fromarray(img_save)
		img_save.save(f'{path}{count}_0.jpg')

def detector(filename):
	start = time.time()
	im = cv2.imread(filename)
	if filename.split('.')[-1]=='png':
		os.rename(filename,'test_image/area_'+filename.split('_')[-1])		   #这里是因为原始图片中有些是中文文件名，
		im = cv2.imread('test_image/area_'+filename.split('_')[-1])			   #但imread不支持中文文件名
	min_wdw_sz = (48,48)
	step_raw = (8,8)
	downscale = 1.1
	clf = joblib.load(os.path.join(model_path, 'svm.model'))
	#List to store the detections
	detections = []
	pool = Pool(8)
	res = []
	for i in range(11,42,2):
		r = pool.apply_async(detect_multi,args = (im,i,min_wdw_sz,step_raw,clf))
		res.append(r )
	pool.close()
	pool.join()
	res = [i.get() for i in res]
	for i in res:
		if i:
			for ii in i:
				detections.append(ii)

	end = time.time()
	t = end-start
	print('用时',t,'秒')

	if not os.path.exists(im_save_path):
		os.makedirs(im_save_path)
	count_save_fig = os.listdir(im_save_path)
	if count_save_fig:
		count_save_fig = [eval(i) for i in count_save_fig]
		count_save_fig = max(count_save_fig)+1
	else:
		count_save_fig = 0
	savefig_path = os.path.join(im_save_path,str(count_save_fig))
	if not os.path.exists(savefig_path):
		os.makedirs(savefig_path)

	clone = cv2.cvtColor(im,cv2.COLOR_BGR2RGB)
	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.imshow(clone)
	for (x,y,_,w,h) in detections:
		ax.add_patch(patches.Rectangle((x,y),w,h,color = 'y',linewidth = 3,fill = False))
	plt.title("Raw Detection before NMS")
	plt.savefig(f'{savefig_path}/{filename}_Before_NMS_{threshold}_{cdf_threshold}_{step_raw}.jpg')
	plt.show()
	
	rects = np.array([[x, y, x + w, y + h] for (x, y, _, w, h) in detections])
	rectsave = [[x,y,w,h] for (x,y,_,w,h) in detections]
	
	sc = [score[0] for (x, y, score, w, h) in detections]
	print("sc: ", sc)
	sc = np.array(sc)
	pick = non_max_suppression(rects, probs = sc, overlapThresh = threshold)
		
	fig = plt.figure()
	ax = fig.add_subplot(111)
	clone = cv2.cvtColor(im,cv2.COLOR_BGR2RGB)
	ax.imshow(clone)
	for f in pick:
		ax.add_patch(patches.Rectangle((f[0],f[1]),f[2]-f[0],f[3]-f[1],color = 'y',linewidth = 3,fill = False))
	plt.title("Final Detections after applying NMS")
	plt.savefig(f'{savefig_path}/{filename}_After_NMS_{threshold}_{cdf_threshold}_{step_raw}.jpg')
	plt.show()

	if swrong:
		save_wrong(im,rectsave)

def test_folder(foldername):
	filenames = glob.iglob(os.path.join(foldername, '*'))
	for filename in filenames:
		detector(filename)

if __name__ == '__main__':
	foldername = 'test_image_mine'	  #效果依然奇差。如果一晚上能够搞定那个鬼mcnn的话也行。
	test_folder(foldername)