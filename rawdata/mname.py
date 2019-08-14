#manage name
import os 
import glob

for i in range(2):
	ns = glob.glob(f'*_{i}.jpg');ns = [ii for ii in ns if 'train' not in ii]
	ns = [eval(j.split('_')[0]) for j in ns]
	m = max(ns)
	ls = []
	for k in range(1,m):
		if k not in ns:
			ls.append(k)
	num = len(ls)
	for ii in range(num):
		site = -1-ii
		if ls:
			newnum = ls.pop(0)
			ns_use = ns[site]
			if ns_use > newnum:
				os.rename(f'{ns_use}_{i}.jpg',f'{newnum}_{i}.jpg')
