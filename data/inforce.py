import os 

imgs = [i for i in os.listdir() if '_1' in i]
for i in imgs:
	for j in range(50):
		os.system(f'cp {i} {j}-{i}')
	print('Finish %s'%i)
