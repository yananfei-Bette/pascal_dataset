import xml.etree.ElementTree as ET
import numpy as np
import scipy.misc
import glob,os

#########
'''
use Bresnham algorithm
code is from: http://www.roguebasin.com/index.php?title=Bresenham%27s_Line_Algorithm#Python
'''
#########
def get_line(start, end):
    """
    Bresenham's Line Algorithm
    Produces a list of tuples from start and end
 
    >>> points1 = get_line((0, 0), (3, 4))
    >>> points2 = get_line((3, 4), (0, 0))
    >>> assert(set(points1) == set(points2))
    >>> print points1
    [(0, 0), (1, 1), (1, 2), (2, 3), (3, 4)]
    >>> print points2
    [(3, 4), (2, 3), (1, 2), (1, 1), (0, 0)]
    """
    # Setup initial conditions
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1
 
    # Determine how steep the line is
    is_steep = abs(dy) > abs(dx)
 
    # Rotate line
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
 
    # Swap start and end points if necessary and store swap state
    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True
 
    # Recalculate differentials
    dx = x2 - x1
    dy = y2 - y1
 
    # Calculate error
    error = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1
 
    # Iterate over bounding box generating points between start and end
    y = y1
    points = []
    for x in range(x1, x2 + 1):
        coord = (y, x) if is_steep else (x, y)
        points.append(coord)
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx
 
    # Reverse the list if the coordinates were swapped
    if swapped:
        points.reverse()
    return points

############
# Label
############
labelDic = {'plane':2, 'bike':3, 'bird':4, 'boat':5, 'bottle':6, 'bus':7, 'car':8, 'cat':9, 'chair':10, 'cow':11, 'table':12, 'dog':13, 'horse':14, 'motorbike':15,  'person':16, 'plant':17, 'sheep':18, 'sofa':19, 'train':20, 'monitor':21, 'sky':22, 'grass':23, 'ground':24, 'road':25, 'building':26, 'tree':27, 'water':28, 'mountain':29, 'wall':30, 'floor':31, 'track':32, 'keyboard':33, 'ceiling':34, 'bag':35, 'bed':36, 'bedclothes':37, 'bench':38, 'book':39, 'cabinet':40, 'cloth':41, 'computer':42, 'cup':43, 'curtain':44, 'door':45, 'fence':46, 'flower':47, 'food':48, 'mouse':49, 'plate':50, 'platform':51, 'rock':52, 'shelves':53, 'sidewalk':54, 'sign':55, 'snow':56, 'truck':57, 'window':58, 'wood':59, 'light':60}

#############
# main
#############
xmlPath = 'pascal_2012/*.xml'
saveFolder = 'pascal_2012_label'
labelPath = os.path.join(saveFolder,'label')
labelVisualPath = os.path.join(saveFolder,'labelVisualize')
if not os.path.isdir(labelPath): os.makedirs(labelPath)
if not os.path.isdir(labelVisualPath): os.makedirs(labelVisualPath)

fLog = open(os.path.join(saveFolder,'log.txt'),'w')

xmlFileAddrs = glob.glob(xmlPath)

for xml in xmlFileAddrs:

    #xml = 'pascal_2012/2008_001196.xml'
    #xml = 'demo/2008_003147.xml'

    print('Processing {}................'.format(xml))
    fLog.write('Processing {}................\n'.format(xml))
    xmlName = os.path.basename(xml).split('.')[0]

    # spaser xml file
    tree = ET.parse(xml)
    root = tree.getroot()

    width = int(root.find('size').find('width').text)
    height = int(root.find('size').find('height').text)
    print(width, height)

    assert int(root.find('segmented').text) == 1, "Segmentation annotation should be true."

    polygons = root.findall('polygon')
    polyDic = {}
    for polygon in polygons:
        classTag = str(polygon.find('tag').text)
        print(classTag)

        ###
        # don't consider background
        if classTag == 'background':
            continue
        ###

        points = polygon.findall('point')
        coord = []
        for point in points:
            X = int(point.find('X').text)
            Y = int(point.find('Y').text)
            coord.append((X,Y))
        if classTag not in polyDic:
            polyDic[classTag] = [coord]
        else:
            polyDic[classTag].append(coord)

    # create label
    img = np.zeros((height, width), dtype=np.uint8)
    labelNames = polyDic.keys()

    for l in labelNames:
        lNum = labelDic[l]
        print(l, len(polyDic[l]))
        for polygon in polyDic[l]:
            assert len(polygon) > 1, 'Not enough points.'
            points = []
            start, end = polygon[0], polygon[1]
            for i in range(1, len(polygon)-1):
                points.extend(get_line(start, end))
                points.pop(-1)
                start, end = polygon[i], polygon[i+1]
            points.append(polygon[-1])
            '''
            print('***************polygon')
            print(polygon)
            print('***************points')
            print(points)
            print('*********************')
            '''

            for point in points:
                #print(point)
                x, y = point

                ###
                # xml file contains some points that out of image.
                ###
                if x >= width or y >= height:
                    print('height and width ({},{})   y and x ({}, {})'.format(height, width, y, x))
                    fLog.write('label and number of stribble ({}, {})\n'.format(l, len(polyDic[l])))
                    fLog.write('height and width ({},{})  y and x ({}, {})\n'.format(height, width, y, x))
                    continue

                img[y, x] = lNum


    # save visualized image
    #print(np.max(img))
    scipy.misc.imsave(os.path.join(labelPath, xmlName+'.png'), img.astype(np.uint8))
    #scipy misc imsave will rescale image.
    scipy.misc.imsave(os.path.join(labelVisualPath, xmlName+'.png'), img)
    #break

fLog.close()