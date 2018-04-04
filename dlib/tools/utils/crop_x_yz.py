# -*- coding:utf-8 -*-

'''

'''

import os,sys
import xml.etree.cElementTree as ET
import argparse
from copy import deepcopy
import fnmatch
import cv2
import numpy as np
import shutil
import argparse
from random import randint

reload(sys)
sys.setdefaultencoding("utf-8")

parser = argparse.ArgumentParser()
parser.add_argument("--mode", default="convert")
args = parser.parse_args()
mode = args.mode

src_dir = '/home/nlp/bigsur/tmp/han/dlib-test/X_YinZhang_ori/'
dst_dir = '/home/nlp/bigsur/tmp/han/dlib-test/X_YinZhang/pos/'
dst_dir_neg = '/home/nlp/bigsur/tmp/han/dlib-test/X_YinZhang/neg/'

for root_dir, dir_names, file_names in os.walk(src_dir):
    for xml_file_name in fnmatch.filter(file_names, "*.xml"):
        xml_file_path = os.path.join(root_dir, xml_file_name)
        tree = ET.ElementTree(file=xml_file_path)
        root = tree.getroot()

        sizes = root.findall('size')
        img_width = int(sizes[0].find('width').text)
        img_height = int(sizes[0].find('height').text)

        objs = root.findall('object')
        for obj in objs:
            if obj.find('name').text == 'X_YinZhang':
                bnd_box = obj.find('bndbox')
                xmin = int(float(bnd_box.find('xmin').text))
                ymin = int(float(bnd_box.find('ymin').text))
                xmax = int(float(bnd_box.find('xmax').text))
                ymax = int(float(bnd_box.find('ymax').text))

                img_file_name = xml_file_name[:-4] + '.jpg'
                dst_img_path = os.path.join(dst_dir, img_file_name)

                img_data = cv2.imread(xml_file_path[:-4]+'.jpg')
                img_cropped = img_data[ymin:ymax, xmin:xmax]
                resized_image = cv2.resize(img_cropped, (150, 150)) 
                cv2.imwrite(dst_img_path, resized_image)

                # random sample a neg image.
                if img_width > 300 and img_height > 300:
                    start_ofs_x = randint(0, img_width-150)
                    start_ofs_y = randint(0, img_height-150)
                    neg_image = img_data[start_ofs_y:start_ofs_y+150, start_ofs_x:start_ofs_x+150]
                    cv2.imwrite(os.path.join(dst_dir_neg, img_file_name), neg_image)

         