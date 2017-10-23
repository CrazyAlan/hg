import xml.etree.ElementTree as ET
import os
from xml.etree.ElementTree import ElementTree
import glob
import string 
import numpy as np
# import cv2
from scipy import misc

label_set = ['face', 'hand']

images = ET.Element('images')
labels = glob.glob('/home/xc/github/darknet/dataset/VOCdevkit/VOC2010/labels/*.txt')
labels = np.sort(labels)
# imgs = '/home/xc/dataset/voc_person/train/image'
for label_path in labels:
    img_path = string.replace(label_path, 'labels', 'JPEGImages')
    img_path = img_path[:-3]+'jpg'
    image_array = misc.imread(img_path)

    new_image = True

    test_file = open(label_path, 'r')
    test_lines = test_file.readlines()
    # import pdb
    # pdb.set_trace()
    for line in test_lines:
        info = line.strip().split()
        lid = int(info[0])
        box_info = np.asarray(info[1:], dtype=np.float32)
        img_size = np.asarray(image_array.shape)[0:2]
        
        left = int(np.round((box_info[0]-box_info[2]/2.)*img_size[1]))
        top = int(np.round((box_info[1]-box_info[3]/2.)*img_size[0]))
        width = int(np.round(box_info[2]*img_size[1]))
        height = int(np.round(box_info[3]*img_size[0]))
        label_text = label_set[lid]

        if new_image == True: # First met this image, then create a new entry
            image = ET.SubElement(images, 'image', file=img_path)
            new_image = False
        box = ET.SubElement(image, 'box', top=str(top), \
                                          left=str(left),\
                                          width=str(width) ,\
                                          height=str(height))
        label = ET.SubElement(box, 'label')
        label.text = label_text



# header = """<?xml version='1.0' encoding='ISO-8859-1'?><?xml-stylesheet type='text/xsl' href='image_metadata_stylesheet.xsl'?><dataset><name>The VOC2011 Database</name><comment>Created by imglab tool</comment>"""   
output = ET.tostring(images)
output = "<?xml version='1.0' encoding='ISO-8859-1'?>" \
        "<?xml-stylesheet type='text/xsl' href='image_metadata_stylesheet.xsl'?>"\
        "<dataset>"\
        "<name>imglab dataset</name>"\
        "<comment>Created by imglab tool.</comment>'" + output

output += '</dataset>'
# output = header+output

with open('face_hand_test.xml', 'w') as f:
    f.write(output)