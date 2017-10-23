from scipy import misc
import sys
import os
import argparse
import numpy as np
from shutil import copyfile

import random
from time import sleep
import xml.etree.ElementTree as ET
import os
from xml.etree.ElementTree import ElementTree

import string

label_set = {'face': "0", 'hand': "1"}

def main(args):
    sleep(random.random())
    output_dir = os.path.expanduser(args.output_dir)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    if not os.path.exists(os.path.join(output_dir,'JPEGImages')):
        os.makedirs(os.path.join(output_dir,'JPEGImages'))
    if not os.path.exists(os.path.join(output_dir,'labels')):
        os.makedirs(os.path.join(output_dir,'labels'))

    # xml tree
    tree = ET.parse(args.input_xml)
    root = tree.getroot()
    images = root.find('images')

    i = 0

    for child in images:
        i += 1
        print i 
        img_path = child.attrib['file']
        image_array = misc.imread(img_path)
        img_size = np.asarray(image_array.shape)[0:2]
        img_h, img_w = img_size[0], img_size[1]

        img_new_path =  os.path.join(output_dir,'JPEGImages', '{0:06d}.'.format(i)+img_path[-3:])
        label_new_path = os.path.join(output_dir,'labels', '{0:06d}.txt'.format(i))

        copyfile(img_path, img_new_path)
        out_file = open(label_new_path, 'w')

        # import pdb
        # pdb.set_trace()

        boxes = child.findall('box')
        for box in boxes:
            top = int(box.attrib['top'])
            left = int(box.attrib['left'])
            width = int(box.attrib['width'])
            height = int(box.attrib['height'])
            label = box[0].text
            l_id = label_set[label]

            bb = np.array([left, top, width, height])
            bb = bb.astype(np.float)
            bb = [(2*bb[0]+bb[2])/(img_w*2.), (2*bb[1]+bb[3])/(2*img_h), bb[2]/img_w, bb[3]/img_h]
            result = l_id + " " + " ".join([str(a) for a in bb]) + '\n'
            out_file.write(result)

    

def parse_arguments(argv):
    parser = argparse.ArgumentParser()
    
    parser.add_argument('input_xml', type=str, help='imglab xml file path.')
    parser.add_argument('output_dir', type=str, help='Directory with aligned face thumbnails.')
    # parser.add_argument('--image_size', type=int,
    #     help='Image size (height, width) in pixels.', default=182)
    # parser.add_argument('--margin', type=int,
    #     help='Margin for the crop around the bounding box (height, width) in pixels.', default=44)
    return parser.parse_args(argv)

if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))