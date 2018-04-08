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
        if obj_name.text in ['X_YinZhang']:
            bnd_box = obj.find('bndbox')
            xmin = bnd_box.find('xmin').text
            xmax = bnd_box.find('xmax').text
            ymin = bnd_box.find('ymin').text
            ymax = bnd_box.find('ymax').text
            ret_lst.append((obj_name.text, xmin, xmax, ymin, ymax))
    return ret_lst

def convert():
    imglab_xml_file = "/home/nlp/bigsur/tmp/han/dlib/tools/imglab/build/yz.xml"
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

    with open("/home/nlp/bigsur/tmp/han/dlib/tools/imglab/build/yz_cvt.xml", "w") as fh:
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

def newname(file_name):
    return file_name[:-4] + '_.' + file_name.split('.')[-1]

def rename():
    src_img_folder = data_loc + 'chanxian/Xings_ssd_rec/selected'
    for root_dir, dir_names, file_names in os.walk(src_img_folder):
        for file_name in fnmatch.filter(file_names, "*.jpg"):
            jpg_file_path = os.path.join(root_dir, file_name)
            xml_file_path = jpg_file_path[:-4] + '.xml'
            print(jpg_file_path)
            print(xml_file_path)
            tree = ET.ElementTree(file=xml_file_path)
            root = tree.getroot()
            objs = root.findall('object')
            for obj in objs:
                if 'QiTa_C' == obj.find('name').text:
                    obj.find('name').text = 'ID_Kuang_1'

            tree.write(xml_file_path)
            os.rename(jpg_file_path, newname(jpg_file_path))
            os.rename(xml_file_path, newname(xml_file_path))

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
    interval = 1;
    while success:
        success,image = vidcap.read()
        if count%interval == 0:
            rotated = imutils.rotate(image, 270)
            #res = cv2.resize(rotated, dsize=(450, 500), interpolation=cv2.INTER_CUBIC)
            cv2.imwrite("./output/frame%d.jpg" % int(count/interval), rotated)     # save frame as JPEG file
            if cv2.waitKey(10) == 27:                     # exit if Escape is hit
                break
        count += 1

def not_grey(img_path):
    img_data = cv2.imread(img_path)
    r, g, b = np.mean(img_data, axis=(0,1))
    if r>150 and g>150 and b>150:
        return False
    return True

def pick():
    from shutil import copyfile

    src_img_folder = "/home/nlp/bigsur/tmp/chanxian_shuju"
    dst_folder = "/home/nlp/bigsur/tmp/chanxian_shuju_xsz"
    if os.path.exists(dst_folder):
        shutil.rmtree(dst_folder)
    os.makedirs(dst_folder)
    ctr = 0
    for root_dir, dir_names, file_names in os.walk(src_img_folder):
        for xml_file_name in fnmatch.filter(file_names, "*.xml"):
            xml_file_path = os.path.join(root_dir, xml_file_name)
            tree = ET.ElementTree(file=xml_file_path)
            root = tree.getroot()
            objs = root.findall('object')
            valid = False
            for obj in objs:
                if 'X_Kuang_1' == obj.find('name').text:
                    valid = True
                    break

            if valid:
                ctr += 1
                img_name = ''
                img_path = ''
                for suffix in ['.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG']:
                    img_name = xml_file_name[:-4] + suffix
                    img_path = os.path.join(root_dir, img_name)
                    if os.path.exists(img_path):
                        break
                if not_grey(img_path):
                    dst_xml_path = os.path.join(dst_folder, str(ctr) + '_' + xml_file_name)
                    copyfile(xml_file_path, dst_xml_path)
                    dst_img_path = os.path.join(dst_folder, str(ctr) + '_' + img_name)
                    copyfile(img_path, dst_img_path)

def rotate_bound(image, angle):
    # grab the dimensions of the image and then determine the
    # center
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)

    # grab the rotation matrix (applying the negative of the
    # angle to rotate clockwise), then grab the sine and cosine
    # (i.e., the rotation components of the matrix)
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])

    # compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))

    # adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY

    # perform the actual rotation and return the image
    return cv2.warpAffine(image, M, (nW, nH))

def rotate_img(img_path):
    img_data = cv2.imread(img_path)
    new_img = rotate_bound(img_data, 90)
    return new_img

def trans_coord(x, y, angel, W, H, xmin, ymin):
    x = int(x)
    y = int(y)
    if angel == 90:
        return (H-y, x)
    if angel == 180:
        return (W-x, H-y)
    if angel == 270 or angel == -90:
        return (y, W-x)
    if angel == 0:
        return (x-xmin, y-ymin)

    return (x, y)

def fix_bndbox(sizes, objs, angel, W, H, xmin_, ymin_):
    if len(sizes) == 0:
        return

    if angel == -90 or angel == 90  or  angel == 270:
        sizes[0].find('width').text = str(H)
        sizes[0].find('height').text = str(W)
    else:
        sizes[0].find('width').text = str(W)
        sizes[0].find('height').text = str(H)

    #fix bouding box
    for obj in objs:
        bndbox = obj.find('bndbox')
        xmin = bndbox.find('xmin').text
        ymin = bndbox.find('ymin').text
        xmax = bndbox.find('xmax').text
        ymax = bndbox.find('ymax').text
        x, y = trans_coord(xmin, ymin, angel, W, H, xmin_ , ymin_)
        bndbox.find('xmin').text = str(x)
        bndbox.find('ymin').text = str(y)
        x, y = trans_coord(xmax, ymax, angel, W, H, xmin_ , ymin_)
        bndbox.find('xmax').text = str(x)
        bndbox.find('ymax').text = str(y)

def rotateall():
    from shutil import copyfile
    src_img_folder = "/home/nlp/bigsur/tmp/chanxian_shuju_yz"
    for root_dir, dir_names, file_names in os.walk(src_img_folder):
        for xml_file_name in fnmatch.filter(file_names, "*.xml"):
            xml_file_path = os.path.join(root_dir, xml_file_name)
            tree = ET.ElementTree(file=xml_file_path)
            root = tree.getroot()
            sizes = tree.findall('size')
            objs = root.findall('object')
            for obj in objs:
                if 'X_Kuang_1' == obj.find('name').text:
                    bnd_box = obj.find('bndbox')
                    xmin = int(bnd_box.find('xmin').text)
                    xmax = int(bnd_box.find('xmax').text)
                    ymin = int(bnd_box.find('ymin').text)
                    ymax = int(bnd_box.find('ymax').text)
                    if abs(int(xmax) - int(xmin)) < abs(int(ymax) - int(ymin)):
                        img_name = ''
                        img_path = ''
                        for suffix in ['.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG']:
                            img_name = xml_file_name[:-4] + suffix
                            img_path = os.path.join(root_dir, img_name)
                            if os.path.exists(img_path):
                                break
                        rotated_img = rotate_img(img_path)

                        img_data = cv2.imread(img_path)
                        img_width = img_data.shape[1]
                        img_height = img_data.shape[0]

                        fix_bndbox(sizes, objs, 90, img_width, img_height, 0, 0)
                        cv2.imwrite(img_path, rotated_img)
                        tree.write(xml_file_path)

                    break

if __name__ == '__main__':
    if mode == "rename":
        rename()
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
    elif mode == "pick":
        pick()
    elif mode == "rotate":
        rotateall()
