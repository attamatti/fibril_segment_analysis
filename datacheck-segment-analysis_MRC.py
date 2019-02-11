#!/usr/bin/python
version = "1.0.4"

# data check for segment-analysis.py.  Read the box files and trace the fibrils and draw them to make sure they are where they're expected to be

### variables ###



## imports
import glob
import os
import math
import matplotlib.pyplot as plt
import sys
# read an mrc file
from numpy import *
import numpy as np
import struct

if len(sys.argv) < 2:
    sys.exit('\nUSAGE: datacheck-segment-analysis_MRC.py <threshold>\nThreshold is length in px for segments taht are considered so long as to be suspect')
distthresh = float(sys.argv[1])     # threshold past which a segment's crossover length is considered suspect


########---------------------------- functions ------------------------------###
##----calculate distance----#
def calcdist(x2,x1,y2,y1):
    xdist = (x2-x1)**2
    ydist = (y2-y1)**2
    return math.sqrt(xdist + ydist)
##---------------------------#
##--------------------------------------------------------------------------###

#------------- READ MRCs--------------
# from David Stokes
class mrc_image:
    def __init__(self,filename):
        self.numbytes1=56           # 56 long ints
        self.numbytes2=80*10          # 10 header lines of 80 chars each
        self.filename=filename

def read(self):
    input_image=open(self.filename,'rb')
    self.header1=input_image.read(self.numbytes1*4)
    self.header2=input_image.read(self.numbytes2)
    byte_pattern='=' + 'l'*self.numbytes1   #'=' required to get machine independent standard size
    self.dim=struct.unpack(byte_pattern,self.header1)[:3]   #(dimx,dimy,dimz)
    self.imagetype=struct.unpack(byte_pattern,self.header1)[3]  #0: 8-bit signed, 1:16-bit signed, 2: 32-bit float, 6: unsigned 16-bit (non-std)
    if (self.imagetype == 0):
        imtype='b'
    elif (self.imagetype == 1):
        imtype='h'
    elif (self.imagetype == 2):
        imtype='f4'
    elif (self.imagetype == 6):
        imtype='H'
    else:
        imtype='unknown'   #should put a fail here
    input_image_dimension=(self.dim[1],self.dim[0])  #2D images assumed
    self.image_data=fromfile(file=input_image,dtype=imtype,count=self.dim[0]*self.dim[1]).reshape(input_image_dimension)
    input_image.close()
    return(self.image_data)
#---------------------------

## program ##

print "\n\n** data check vers %s **" % version


# get the files
boxfiles = glob.glob("*.box")
indfibril = {}          
filefilms = []
missingfiles = []
for i in boxfiles:
    coords = []
    filefilm = i.split('.')
    filename = filefilm[0]
    filefilms.append(filename)
    f = open(i)
    data = f.readlines()
    oboxsize = (float(data[0].split("\t")[2]))/2
    f.close()

## make sure the png files exist
    if os.path.isfile("%s.mrc" % filefilm[0]) == False:
        print "%s.mrc file not found - skipping" % filefilm[0]
        missingfiles.append("%s.mrc" % filefilm[0])

## split the data into individual fibrils
    indfibno = 1
    for j in data:
        coords.append((float(j.split('\t')[0]),float(j.split('\t')[1])))    
    for point in coords:
        if "%s-%.4d" % (filename,indfibno) not in indfibril.keys():
            indfibril["%s-%.4d" % (filename,indfibno)] = []
        if point[0] >= 0:
            indfibril["%s-%.4d" % (filename,indfibno)].append(point)
        else:
            indfibno = indfibno+1





## make the gif files with the illustrated fibrils
    if "%s.mrc" % filename not in missingfiles:
        print filename
        mrcim = mrc_image('%s.mrc' % filename)
        image = read(mrcim)        
        fig, ax = plt.subplots()
        ax.imshow(image,cmap='gray')
        plt.ylim((0, image.shape[0]))   # set the xlim to xmin, xmax
        plt.xlim(0, image.shape[1])     # set the xlim to xmin, xmax
        filename = i.split('.')[0].split('-')
        print"\ndrawing fibrils for %s" % (filename[0])         
        for i in indfibril:
            if i.split("-")[0] == filename[0]:
                pointsx = []
                pointsy = []
                for j in indfibril[i]:
                    pointsx.append(j[0]+oboxsize)
                    pointsy.append(j[1]+oboxsize)
                ax.plot(pointsx,pointsy, '-', linewidth=5, color='firebrick')
        plt.savefig("%s_f.png" % filename[0])
        
# check all segment lengths for ones that are obviously too long

suspect = []
for i in indfibril:
    for k in range(1,len(indfibril[i])-2):
        distance = calcdist(indfibril[i][k+1][0],indfibril[i][k][0],indfibril[i][k+1][1],indfibril[i][k][1])
        if distance > distthresh:
           suspect.append("%s-%.5d\t%.2f\t%s\t%s" % (i,k, distance, indfibril[i][k],indfibril[i][k+1]))
if len(suspect) > 0:
    print "\n ** suspect segments **"
    print "name\t\t\tlength\tcoordinates"
    for i in suspect:
        print i