# prepare car image
import numpy as np
import os
#import matplotlib.image as mpimg
import cv2
#np.random.seed(50)

seg_imgs = {}
with open(\
	'/media/ruiyuan/FourTB1/Yanan_seg_singleClassify_acc/voc/val.txt', 'r') as f:
	for line in f.readlines():
		line_ = line.strip()
		year = line_[:4]
		number = line_[5:]
		if year not in seg_imgs:
			seg_imgs[year] = [number]
		else:
			seg_imgs[year].append(number)

#count = 0
car_seg_imgs = []
with open(\
	'/media/ruiyuan/FourTB1/Yanan_seg_singleClassify_acc/voc/car_val.txt', 'r') as f:
	lines = f.readlines()
	#indx = np.random.choice(len(lines), len(lines))
	#print len(lines)
	#print indx
	for i in range(len(lines)):
		line_ = lines[i].strip()
		if '-1' not in line_: # and count < 500:
			year = line_[:4]
			number = line_[5:11]
			if year in seg_imgs and number in seg_imgs[year]:
				car_seg_imgs.append(line_[:11])
				#count += 1
print len(car_seg_imgs)
print len(set(car_seg_imgs))
#assert 1 == 0
#102

# create train data set
save_folder_prefix = \
'/media/ruiyuan/FourTB1/Yanan_seg_singleClassify_acc/voc/VOC2012_CAR'
save_train_imgs_path = os.path.join(save_folder_prefix, 'test','images')
save_train_masks_path = os.path.join(save_folder_prefix, 'test', 'masks')
save_train_masks_visual_path = os.path.join(save_folder_prefix, 'test', 'mask_visual')
if not os.path.isdir(save_train_imgs_path): os.makedirs(save_train_imgs_path)
if not os.path.isdir(save_train_masks_path):os.makedirs(save_train_masks_path)
if not os.path.isdir(save_train_masks_visual_path):os.makedirs(save_train_masks_visual_path)

train_imgs_path = \
'/media/ruiyuan/FourTB1/Yanan_seg_singleClassify_acc/voc/VOCdevkit/VOC2012/JPEGImages'
max_H, max_W = 0, 0
for img_name in car_seg_imgs:
	img = cv2.imread(os.path.join(train_imgs_path, img_name+'.jpg'))
	max_H, max_W = max(img.shape[0], max_H), max(img.shape[1], max_W)
#max 500 500
#min 112 339

IMG_SIZE = max(max_H, max_W)
#image_count = 0
for img_name in car_seg_imgs:
	'''
	img = mpimg.imread(os.path.join(train_imgs_path, img_name+'.jpg'))
	mask = mpimg.imread(os.path.join(train_imgs_path.replace('JPEGImages',\
		'SegmentationClass'), img_name+'.png'))
	# png image rescale to 0~1
	'''

	img = cv2.imread(os.path.join(train_imgs_path, img_name+'.jpg'))
	mask = cv2.imread(os.path.join(train_imgs_path.replace('JPEGImages',\
		'SegmentationClass'), img_name+'.png'))
	#mask = cv2.imread('/media/ruiyuan/FourTB1/Yanan_seg_singleClassify_acc/voc/VOC2012_CAR/train/masks/2008_004080.png')
	#print img.dtype
	#print mask.dtype
	#assert 1 == 0
	H,W,_ = img.shape

	if H < IMG_SIZE:
		delta = (IMG_SIZE - H)/2
		if (IMG_SIZE - H)%2 == 0:
			img = np.pad(img, ((delta,delta),(0,0),(0,0)), 'edge')
			mask = np.pad(mask, ((delta,delta),(0,0),(0,0)), 'edge')
		else:
			img = np.pad(img, ((delta,delta+1),(0,0),(0,0)), 'edge')
			mask = np.pad(mask, ((delta,delta+1),(0,0),(0,0)), 'edge')

	if W < IMG_SIZE:
		delta = (IMG_SIZE - W)/2
		if (IMG_SIZE - W)%2 == 0:
			img = np.pad(img, ((0,0), (delta,delta),(0,0)), 'edge')
			mask = np.pad(mask, ((0,0),(delta,delta),(0,0)), 'edge')
		else:
			img = np.pad(img, ((0,0),(delta,delta+1),(0,0)), 'edge')
			mask = np.pad(mask, ((0,0),(delta,delta+1),(0,0)), 'edge')

	mask_ = np.zeros((IMG_SIZE, IMG_SIZE), dtype=np.uint8)
	count = 0
	#print img.dtype
	#print mask.dtype
	#assert 1 == 0
	for i in range(IMG_SIZE):
		for j in range(IMG_SIZE):
			if list(np.copy(mask[i,j,:])) == [128,128,128]:
				#print "aaaaaaaaaaaaaaaaaaaa"
				mask_[i,j] = 1
				count += 1
	if count >= (IMG_SIZE*IMG_SIZE)/20:
		'''
		mpimg.imsave(os.path.join(save_train_imgs_path, img_name+'.png'), img)
		mpimg.imsave(os.path.join(save_train_masks_path, img_name+'.png'), mask_)
		mpimg.imsave(os.path.join(save_train_masks_visual_path, img_name+'.png'), mask_*255)
		'''

		cv2.imwrite(os.path.join(save_train_imgs_path, img_name+'.png'), img)
		cv2.imwrite(os.path.join(save_train_masks_path, img_name+'.png'), mask_)
		cv2.imwrite(os.path.join(save_train_masks_visual_path, img_name+'.png'), mask_*255)
	#image_count += 1
#print image_count