# prepare car image
import numpy as np
import os
import cv2

seg_imgs = {}
with open('/media/ruiyuan/Backup/Yanan/voc/train.txt', 'r') as f:
	for line in f.readlines():
		line_ = line.strip()
		year = line_[:4]
		number = line_[5:]
		if year not in seg_imgs:
			seg_imgs[year] = [number]
		else:
			seg_imgs[year].append(number)

car_seg_imgs = []
with open('/media/ruiyuan/Backup/Yanan/voc/car_train.txt', 'r') as f:
	lines = f.readlines()
	for i in range(len(lines)):
		line_ = lines[i].strip()
		if '-1' not in line_: # and count < 500:
			year = line_[:4]
			number = line_[5:11]
			if year in seg_imgs and number in seg_imgs[year]:
				car_seg_imgs.append(line_[:11])

#print len(car_seg_imgs)
#print len(set(car_seg_imgs))
#102

# create train data set
save_folder_prefix = '/media/ruiyuan/Backup/Yanan/voc/VOC2012_CAR_crop'
save_train_imgs_path = os.path.join(save_folder_prefix, 'train','images')
save_train_masks_path = os.path.join(save_folder_prefix, 'train', 'masks')
save_train_masks_visual_path = os.path.join(save_folder_prefix, 'train', 'mask_visual')
if not os.path.isdir(save_train_imgs_path): os.makedirs(save_train_imgs_path)
if not os.path.isdir(save_train_masks_path):os.makedirs(save_train_masks_path)
if not os.path.isdir(save_train_masks_visual_path):os.makedirs(save_train_masks_visual_path)

train_imgs_path = '/media/ruiyuan/Backup/Yanan/voc/VOCdevkit/VOC2012/JPEGImages'
'''
max_H, max_W = 0, 0
for img_name in car_seg_imgs:
	img = cv2.imread(os.path.join(train_imgs_path, img_name+'.jpg'))
	max_H, max_W = max(img.shape[0], max_H), max(img.shape[1], max_W)
#max 500 500
#min 112 339

IMG_SIZE = max(max_H, max_W)
'''
IMG_SIZE = 300

def crop_imgs(img, mask, indx):

	img = img[indx[0]:,indx[1]:,:]
	mask = mask[indx[0]:,indx[1]:,:]
	assert img.shape == mask.shape, 'Image shape should equal to mask shape'
	H,W,_ = img.shape

	if H < IMG_SIZE:
		delta = (IMG_SIZE - H)/2
		if (IMG_SIZE - H)%2 == 0:
			img = np.pad(img, ((delta,delta),(0,0),(0,0)), 'edge')
			mask = np.pad(mask, ((delta,delta),(0,0),(0,0)), 'edge')
		else:
			img = np.pad(img, ((delta,delta+1),(0,0),(0,0)), 'edge')
			mask = np.pad(mask, ((delta,delta+1),(0,0),(0,0)), 'edge')

	if H >= IMG_SIZE:
		img = img[:IMG_SIZE,:,:]
		mask = mask[:IMG_SIZE,:,:]

	if W < IMG_SIZE:

		delta = (IMG_SIZE - W)/2
		if (IMG_SIZE - W)%2 == 0:
			img = np.pad(img, ((0,0), (delta,delta),(0,0)), 'edge')
			mask = np.pad(mask, ((0,0),(delta,delta),(0,0)), 'edge')
		else:
			img = np.pad(img, ((0,0),(delta,delta+1),(0,0)), 'edge')
			mask = np.pad(mask, ((0,0),(delta,delta+1),(0,0)), 'edge')

	if W >= IMG_SIZE:
		img = img[:, :IMG_SIZE, :]
		mask = mask[:, :IMG_SIZE, :]

	return (img, mask)


for img_name in car_seg_imgs:

	img = cv2.imread(os.path.join(train_imgs_path, img_name+'.jpg'))
	mask = cv2.imread(os.path.join(train_imgs_path.replace('JPEGImages',\
		'SegmentationClass'), img_name+'.png'))

	H,W,_ = img.shape
	crops = []
	for i in range(0, H-IMG_SIZE/3, IMG_SIZE/3):
		for j in range(0, W-IMG_SIZE/3, IMG_SIZE/3):
			print i,j,H,W
			crops.append(crop_imgs(np.copy(img), np.copy(mask),(i,j)))

	for indx in range(len(crops)):
		(img, mask) = crops[indx]
		print img.shape
		#print mask.shape
		assert img.shape[:2] == mask.shape[:2] == (IMG_SIZE, IMG_SIZE)

		mask_ = np.zeros((IMG_SIZE, IMG_SIZE), dtype=np.uint8)
		count = 0

		for i in range(IMG_SIZE):
			for j in range(IMG_SIZE):
				if list(np.copy(mask[i,j,:])) == [128,128,128]:
					mask_[i,j] = 1
					count += 1
		if count >= (IMG_SIZE*IMG_SIZE)/20:
			cv2.imwrite(os.path.join(save_train_imgs_path, img_name+'_'+str(indx)+'.png'), img)
			cv2.imwrite(os.path.join(save_train_masks_path, img_name+'_'+str(indx)+'.png'), mask_)
			cv2.imwrite(os.path.join(save_train_masks_visual_path,\
				img_name+'_'+str(indx)+'.png'), mask_*255)