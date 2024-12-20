#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys
import os
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement
from lxml import etree
import codecs
from libs.constants import DEFAULT_ENCODING

TXT_EXT = '.txt'
ENCODE_METHOD = DEFAULT_ENCODING

class YOLOOBBWriter:

    def __init__(self, foldername, filename, imgSize, databaseSrc='Unknown', localImgPath=None):
        self.foldername = foldername
        self.filename = filename
        self.databaseSrc = databaseSrc
        self.imgSize = imgSize
        self.boxlist = []
        self.localImgPath = localImgPath
        self.verified = False

    # Original
    # def addBndBox(self, centre_x, centre_y, height, width, angle, name, difficult):
    #     bndbox = {'centre_x': centre_x, 'centre_y': centre_y, 'height': height, 'width': width, 'angle': angle}
    #     bndbox['name'] = name
    #     bndbox['difficult'] = difficult
    #     self.boxlist.append(bndbox)
    
    # Tuan Anh
    def addBndBox(self, corner_1, corner_2, corner_3, corner_4, imageHeight, imageWidth, centre_x, centre_y, height, width, angle, name, difficult):
        bndbox = {'corner_1': corner_1, 'corner_2': corner_2, 'corner_3': corner_3, 'corner_4': corner_4}
        bndbox.update({
            'centre_x': centre_x,
            'centre_y': centre_y,
            'height': height,
            'width': width,
            'angle': angle,
            'name': name,
            'difficult': difficult,
            'imageHeight': imageHeight,
            'imageWidth': imageWidth
            })
        bndbox['name'] = name
        bndbox['difficult'] = difficult
        bndbox['imageHeight'] = imageHeight
        bndbox['imageWidth'] = imageWidth
        self.boxlist.append(bndbox)


    def save(self, classList=[], targetFile=None):

        out_file = None # Display annotation file
        annotation_file = None # Annotation file
        out_class_file = None   #Update class list .txt

        if targetFile is None:
            out_file = open(
            self.filename + TXT_EXT, 'w', encoding=ENCODE_METHOD)
            classesFile = os.path.join(os.path.dirname(os.path.abspath(self.filename)), "classes.txt")
            out_class_file = open(classesFile, 'w')

            annotation_folder = os.path.join(os.path.dirname(os.path.abspath(self.filename)), "annotation")
            os.makedirs(annotation_folder, exist_ok=True)
            annotationFilePath = os.path.join(annotation_folder, os.path.basename(self.filename) + ".txt")
            annotation_file = open(annotationFilePath, 'w', encoding=ENCODE_METHOD)

        else:
            out_file = codecs.open(targetFile, 'w', encoding=ENCODE_METHOD)
            classesFile = os.path.join(os.path.dirname(os.path.abspath(targetFile)), "classes.txt")
            out_class_file = open(classesFile, 'w')

            annotation_folder = os.path.join(os.path.dirname(os.path.abspath(targetFile)), "annotation")
            os.makedirs(annotation_folder, exist_ok=True)
            annotationFilePath = os.path.join(annotation_folder, os.path.basename(targetFile))
            annotation_file = open(annotationFilePath, 'w', encoding=ENCODE_METHOD)
        out_file.write("YOLO_OBB\n")
        for box in self.boxlist:
            # Tuan Anh
            imageHeight = box['imageHeight']
            imageWidth = box['imageWidth']
            #
            boxName = box['name']
            if boxName not in classList:
                classList.append(boxName)
            classIndex = classList.index(boxName)
            # Display annotation file saving
            out_file.write("%d %.6f %.6f %.6f %.6f %.6f\n" % (classIndex, box['centre_x'], box['centre_y'], box['height'], box['width'], box['angle'])) # Original save format
            
            # Tuan Anh
            # Annotation Yolo format file
            annotation_file.write(
                "%d %.6f %.6f %.6f %.6f %.6f %.6f %.6f %.6f\n" % (
                    classIndex,
                    box['corner_1'].x() / imageWidth, box['corner_1'].y() / imageHeight,
                    box['corner_2'].x() / imageWidth, box['corner_2'].y() / imageHeight,
                    box['corner_3'].x() / imageWidth, box['corner_3'].y() / imageHeight,
                    box['corner_4'].x() / imageWidth, box['corner_4'].y() / imageHeight
                )
            )

        # print (classList)
        # print (out_class_file)
        for c in classList:
            out_class_file.write(c+'\n')

        out_class_file.close()
        out_file.close()
        annotation_file.close()



class YoloOBBReader:

    def __init__(self, filepath, image, classListPath=None):
        # shapes type:
        # [labbel, [(x1,y1), (x2,y2), (x3,y3), (x4,y4)], color, color, difficult]
        self.shapes = []
        self.filepath = filepath

        if classListPath is None:
            dir_path = os.path.dirname(os.path.realpath(self.filepath))
            self.classListPath = os.path.join(dir_path, "classes.txt")
        else:
            self.classListPath = classListPath

        # print (filepath, self.classListPath)

        classesFile = open(self.classListPath, 'r')
        self.classes = classesFile.read().strip('\n').split('\n')

        # print (self.classes)

        imgSize = [image.height(), image.width(),
                      1 if image.isGrayscale() else 3]

        self.imgSize = imgSize

        self.verified = False
        # try:
        self.parseYoloOBBFormat()
        # except:
            # pass

    def getShapes(self):
        return self.shapes

    def addShape(self, label, centre_x, centre_y, height, width, angle, difficult):
        self.shapes.append((label, float(centre_x), float(centre_y), float(height), float(width), float(angle), None, None, difficult)) # The 2 None's are for shape colors

    def parseYoloOBBFormat(self):
        bndBoxFile = open(self.filepath, 'r')
        next(bndBoxFile) # Skip first line ("YOLO_OBB")
        for bndBox in bndBoxFile:
            classIndex, centre_x, centre_y, height, width, angle = bndBox.split(' ')
            label = self.classes[int(classIndex)]

            # Caveat: difficult flag is discarded when saved as yolo format.
            self.addShape(label, centre_x, centre_y, height, width, angle, False)
