#* Copyright (C) Gurmehar Singh 2019 - All Rights Reserved
#* Unauthorized copying or distribution of this file, via any medium is strictly prohibited
#* Proprietary and confidential
#* Written by Gurmehar Singh <gurmehar@gmail.com>, October 2019
#*/

import numpy, random
import matplotlib.pyplot as plt
import matplotlib.image as mpimg 
import cv2
import pygame
import os
import sys
import scipy.stats
import time
import PIL
from PIL import Image
import shutil
from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen
import io
import getpass
 
user = requests.Session()

arglist = sys.argv
arglist[1] = int(arglist[1]) #where to start
arglist[2] = int(arglist[2]) #iterations
savedir = arglist[3]
plottype = arglist[4]

print('sys.argv is', sys.argv)

url = 'http://psrsearch.wvu.edu/psc/index.php/'
url2 = "http://psrsearch.wvu.edu/psc/"

user.get(url)

username = input("Enter username: ")
password = getpass.getpass()
print(username)
payload = {"username": username, "password": password, "submit": "Sign in"}

resp = user.post(url, data=payload)

resp1 = user.get('http://psrsearch.wvu.edu/psc/skymap.php')
resp1 = resp1.text

resp1 = resp1.replace("preview.php?datasetID", '', arglist[1]-1)
resp1 = resp1.replace(">View", '', arglist[1]-1)

for i in range(arglist[2]):
    dataset = resp1[resp1.index("preview.php?datasetID"):resp1.index('''>View''')]
    resp1 = resp1.replace(dataset+">View", '')
    print(dataset)
    datasetnum = dataset.split('=')[1]
    dataset = user.get(url2+dataset)
    dataset = dataset.content
    dataset = str(dataset)
    if plottype == 'fft':
        dataset = dataset[0:dataset.index("SinglePulse")]
    skip = 0
    num = 0
    while "display_plot.php?" in dataset:
        skip += 1
        num += 1
        index = dataset.index("display_plot.php?")
        plot = dataset[index:index+35]
        plot = plot[0:plot.index(">")]
        dataset = dataset.replace(plot, '')
        plot = user.get(url2+plot)
        plot = plot.content
        plot = str(plot)
        if plottype == 'singlepulse' and skip > 30:
            plot = plot[plot.index('''/results'''):plot.index('''class="sp"''')]
        else:
            plot = plot[plot.index('''/results'''):plot.index('''class="fft"''')]
        plot = plot[0:plot.index('''"''')]
        plot = plot.replace("/results/", '')
        print(str(num)+" : "+plot)
        if plottype == 'singlepulse':
            if skip <= 30:
                continue

        plot1 = user.get('http://psrsearch.wvu.edu/psc/results/'+plot)
        im = Image.open(io.BytesIO(plot1.content))
        plot = plot.replace("/", "@")
        plot = plot.replace("png", "")
        plot = plot + 'datasetID=' + datasetnum + '.png'
        im.save(savedir+plot)
