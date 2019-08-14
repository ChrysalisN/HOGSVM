#提取图片hog特征
import cv2
from sklearn.externals import joblib
import glob
import os
from config import *

hog = cv2.HOGDescriptor(win_size,block_size,block_stride,cell_size,num_bins)

def getHog(imgs):
	X = []
	for filename in imgs:
		img = cv2.imread(filename)
		if img is None:
			print('Could not find image %s'%filename)
			continue
		X.append(hog.compute(img,(img_avg,img_avg)))
	return X

def extract_features():
	des_type = 'HOG'
	
	# If feature directories don't exist, create them
	if not os.path.isdir(pos_feat_ph):
		os.makedirs(pos_feat_ph)

	# If feature directories don't exist, create them
	if not os.path.isdir(neg_feat_ph):
		os.makedirs(neg_feat_ph)

	print("Calculating the descriptors for the positive samples and saving them")
	X_pos = getHog(glob.glob(os.path.join(pos_im_path, "*")))
	X_neg = getHog(glob.glob(os.path.join(neg_im_path, "*")))
	imgs_pos = os.listdir(pos_im_path)
	imgs_neg = os.listdir(neg_im_path)
	for i in range(len(X_pos)):		
		im_path = imgs_pos[i]
		fd = X_pos[i]
		fd_name = os.path.split(im_path)[1].split(".")[0] + ".feat"
		fd_path = os.path.join(pos_feat_ph, fd_name)
		joblib.dump(fd, fd_path)
	print("Positive features saved in {}".format(pos_feat_ph))

	for i in range(len(X_neg)):		
		im_path = imgs_neg[i]
		fd = X_neg[i]
		fd_name = os.path.split(im_path)[1].split(".")[0] + ".feat"
		fd_path = os.path.join(neg_feat_ph, fd_name)
		joblib.dump(fd, fd_path)
	print("Positive features saved in {}".format(neg_feat_ph))
	
	print("Completed calculating features from training images")

if __name__=='__main__':
	extract_features()
