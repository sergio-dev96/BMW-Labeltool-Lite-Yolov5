# -*- coding: utf-8 -*-
"""
This script is to convert the BMW-Labeltool-Lite json annotation files to appropriate format needed by YOLOv5

Based on previous work by: Guanghan Ning (gnxr9@mail.missouri.edu)
"""

import os
from os import walk
from PIL import Image
import argparse
import json
import pybboxes as pbx

parser = argparse.ArgumentParser(description='JSON to YOLO format')
parser.add_argument('--dir', type=str,default="", help='Directory of json files')
args = parser.parse_args()

    
""" Configure Paths"""   
mypath = args.dir
print(mypath)
outpath = f"{args.dir}\\..\\YOLO"
imgdir = f"{args.dir}\\..\\..\\images"

if not os.path.exists(outpath):
    os.mkdir(outpath)

""" Get input json file list """
json_name_list = []
for (dirpath, dirnames, filenames) in walk(mypath):
    json_name_list.extend(filenames)
    break

""" Process """
for json_name in json_name_list:    
    """ Open input text files """
    txt_path = f"{mypath}\\{json_name}"
    print("Input:" + txt_path)
    
    items : str
    with open(txt_path, "r") as txt_file:
        items = json.loads(txt_file.read())
    
    """ Open output text files """
    txt_outpath = f"{outpath}\\{os.path.splitext(json_name)[0]}.txt"
    print("Output:" + txt_outpath)
    with open(txt_outpath, "w") as txt_outfile:
        """ Convert the data to YOLOv5 format """
        for item in items:
            print(item)
            imgpath = str('%s/%s.png'%(imgdir, os.path.splitext(json_name)[0]))
            if not os.path.exists(imgpath):
                imgpath = str('%s/%s.jpg'%(imgdir, os.path.splitext(json_name)[0]))
            if not os.path.exists(imgpath):
                continue

            with Image.open(imgpath) as im:    
                w= int(im.size[0])
                h= int(im.size[1])
            
            yolo = pbx.convert_bbox((item['Left'],item['Top'],item['Right'],item['Bottom']), from_type="voc", to_type="yolo", image_size=(w, h))
            txt_outfile.write(f"{item['ObjectClassId']} {' '.join([str(i) for i in yolo])}\n")