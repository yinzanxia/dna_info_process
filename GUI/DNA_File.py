# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 14:54:55 2018

@author: mayn
"""

import json
import os

def load_dna_by_file_name(file_name):
    f = open(file_name, encoding='utf-8')
    dna = json.load(f)
    return dna



def find_json_files(path):
    file_list=[]
    files = os.listdir(path);
    for f in files:
        npath = path + '/' + f;
        if (os.path.isfile(npath)):
            if npath.find('txt') != -1:
                file_list.append(npath)
            if (os.path.isdir(npath)):
                continue
    return file_list