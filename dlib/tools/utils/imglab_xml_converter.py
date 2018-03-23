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

reload(sys)
sys.setdefaultencoding("utf-8")

parser = argparse.ArgumentParser()
parser.add_argument("--mode", default="convert")
args = parser.parse_args()
mode = args.mode

data_loc = "/home/nlp/bigsur/data/"
xml_loc = "/home/nlp/bigsur/devel/dlib/tools/imglab/build/"

def get_bndbox_lst(img_file_path):
    xml_file_path = img_file_path.split('.')[0] + '.xml'
    if not os.path.exists(xml_file_path):
        return []
    tree = ET.ElementTree(file=xml_file_path)
    tree_root = tree.getroot()
    objs = tree_root.findall('object')
    ret_lst = []
    for obj in objs:
        obj_name = obj.find('name')
        if obj_name.text in ['QiTa_C']: 
            bnd_box = obj.find('bndbox')
            xmin = bnd_box.find('xmin').text
            xmax = bnd_box.find('xmax').text
            ymin = bnd_box.find('ymin').text
            ymax = bnd_box.find('ymax').text
            ret_lst.append((obj_name.text, xmin, xmax, ymin, ymax))
    return ret_lst

def convert():
    imglab_xml_file = "/home/nlp/bigsur/devel/dlib/tools/imglab/build/s0.xml"
    #imglab_xml_file = xml_loc + "/t0.xml" 

    imglab_tree = ET.ElementTree(file=imglab_xml_file)
    #imglab_tree_detail = deepcopy(imglab_tree)

    images_root = imglab_tree.getroot()
    images_lst = images_root.findall('images')

    #details_root = imglab_tree_detail.getroot()
    #details_images_lst = details_root.findall('images')

    for images in images_lst:
        image_lst = images.findall('image')
        for image in image_lst:
            image_file_path = image.attrib.get('file')
            bndboxes = get_bndbox_lst(image_file_path)
            if len(bndboxes) == 0:
                images.remove(image)
                continue
            for bndbox in bndboxes:
                box = ET.SubElement(image, 'box')
                name, xmin, xmax, ymin, ymax = bndbox
                width = int(xmax) - int(xmin)
                height = int(ymax) - int(ymin)
                box.set('top', ymin)
                box.set('left', xmin)
                box.set('width', str(width))
                box.set('height', str(height))
                # part = ET.SubElement(box, 'part')
                # part.set('name', '1')
                # part.set('x', '67')
                # part.set('y', '68')

    with open(xml_loc + "/s0_convert.xml", "w") as fh:
        imglab_tree.write(fh)

def clean():
    invalid_file_list_f = open("/tmp/invalid.txt", 'r')
    lines = invalid_file_list_f.readlines()

    target_clean_file = xml_loc + "/t0_bk_cleanbyratio.xml"
    tree = ET.ElementTree(file=target_clean_file)
    tree_root = tree.getroot()
    images_lst = tree_root.findall('images')
    for images in images_lst:
        image_lst = images.findall('image')
        for image in image_lst:
            image_file_path = image.attrib.get('file')
            if image_file_path + '\n' in lines:
                images.remove(image)

    with open(xml_loc + "/t0_bk_cleanbyratio_clean.xml", "w") as fh:
        tree.write(fh)

def clean_by_ratio():
    target_clean_file = xml_loc + "/t0_bk.xml"
    tree = ET.ElementTree(file=target_clean_file)
    tree_root = tree.getroot()
    images_lst = tree_root.findall('images')
    for images in images_lst:
        image_lst = images.findall('image')
        for image in image_lst:
            boxes = image.findall('box')
            valid = True
            for box in boxes:
                if not valid:
                    break
                height = box.attrib.get('height')
                width = box.attrib.get('width')
                if int(height) > int(width):
                    images.remove(image)
                    valid = False

    with open(xml_loc + "/t0_bk_cleanbyratio.xml", "w") as fh:
        tree.write(fh)

def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)

def img_stats():
    import matplotlib.pyplot as plt
    src_img_folder = data_loc + "/data_ssd_id_train/"
    heights = []
    widths = []
    ratios = []
    ctr = 0
    for root, dir_names, file_names in os.walk(src_img_folder):
        for file_name in fnmatch.filter(file_names, "*.jpg"):
            jpg_file_path = os.path.join(root, file_name)
            img_data = cv2.imread(jpg_file_path)
            (h, w) = img_data.shape[:2]
            heights.append(h)
            widths.append(w)
            ratios.append(float(w)/float(h))
            ctr += 1
            if ctr > 1000:
                break
    print(mean(widths))
    print(mean(heights))
    print(mean(ratios))
    plt.plot(np.arange(0, len(heights), 1), heights)
    plt.show()         

def finetune_xml(xml_file, dst_folder, ratio_x, ratio_y):
    tree = ET.ElementTree(file=xml_file)
    root = tree.getroot()
    objs = root.findall('object')
    for obj in objs:
        bnd_box = obj.find('bndbox')
        xmin = int(float(bnd_box.find('xmin').text)/ratio_x)
        ymin = int(float(bnd_box.find('ymin').text)/ratio_y)
        xmax = int(float(bnd_box.find('xmax').text)/ratio_x)
        ymax = int(float(bnd_box.find('ymax').text)/ratio_y)
        bnd_box.find('xmin').text = str(xmin)
        bnd_box.find('ymin').text  = str(ymin)
        bnd_box.find('xmax').text  = str(xmax)
        bnd_box.find('ymax').text  = str(ymax)
    dst_xml_file = os.path.join(dst_folder, xml_file.split('/')[-1])
    tree.write(dst_xml_file)

def resize_img():
    src_img_folder = data_loc + '/data_ssd_id_train' 
    target_folder = data_loc + '/data_ssd_id_train_resized'
    if os.path.exists(target_folder):
        shutil.rmtree(target_folder)
    os.makedirs(target_folder)
    for root, dir_names, file_names in os.walk(src_img_folder):
        for file_name in fnmatch.filter(file_names, "*.jpg"):
            jpg_file_path = os.path.join(root, file_name)
            xml_file_path = jpg_file_path[:-4] + '.xml'
            img_data = cv2.imread(jpg_file_path)
            (h, w) = img_data.shape[:2]
            if w > h:
                resized_img = cv2.resize(img_data, (500, 450), interpolation=cv2.INTER_CUBIC)
                cv2.imwrite(os.path.join(target_folder, jpg_file_path.split('/')[-1]), resized_img)
                finetune_xml(xml_file_path, target_folder, float(w)/500.0, float(h)/450.0)

def select(num):
    tree = ET.ElementTree(file=xml_loc + "/t.xml")
    root = tree.getroot()
    images_lst = root.findall("images")
    for images in images_lst:
        image_lst = images.findall("image")
        ctr = 0
        for image in image_lst:
            ctr += 1
            if ctr > num:
                images.remove(image)

    tree.write(xml_loc + "/t0.xml")

def save_frames():
    import imutils

    #src = "/home/nlp/bigsur/tmp/han/VID_20180323_084232.mp4"
    src = "/home/nlp/bigsur/tmp/han/VID_20180323_084214.mp4"
    vidcap = cv2.VideoCapture(src)
    success,image = vidcap.read()
    count = 0; 
    interval = 15;
    while success:
        success,image = vidcap.read()
        if count%interval == 0:
            rotated = imutils.rotate(image, 270)
            res = cv2.resize(rotated, dsize=(450, 500), interpolation=cv2.INTER_CUBIC)
            cv2.imwrite("./output/frame%d.jpg" % int(count/interval), res)     # save frame as JPEG file
            if cv2.waitKey(10) == 27:                     # exit if Escape is hit
                break
        count += 1

if __name__ == '__main__':
    if mode == "convert":
        convert()
    elif mode == "clean":
        clean()
    elif mode == "cleanbyratio":
        clean_by_ratio()
    elif mode == "stat":
        img_stats()
    elif mode == "resize":
        resize_img()
    elif mode == "select":
        select(6000)
    elif mode == "capture":
        save_frames()
