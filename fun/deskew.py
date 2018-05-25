# -*- coding: utf-8 -*-
"""
Macro to deskew MLS stage scans.
Adam Tyson | adam.tyson@icr.ac.uk | 2018-05-25
"""

import numpy as np
from scipy.ndimage import shift
from skimage.external.tifffile import imsave
import tkinter
import tkinter.filedialog
import os


def deskew(img, direc, shiftStep):
    nslice = img.shape[0]
    padding = 10 + round(nslice*shiftStep)

    print('Padding image')
    if direc == 1:
        img = np.pad(img, [(0, 0), (0, 0), (0, padding)],
                     mode='constant')
    else:
        img = np.pad(img, [(0, 0), (0, 0), (padding, 0)],
                     mode='constant')

    print('Shifting image')
    deskewed = np.empty(img.shape)

    for i in range(0, nslice):
        print('Shifting frame ', i+1, ' of ', nslice)
        if direc is 'Left2Right':
            deskewed[i] = shift(img[i], (0, i*shiftStep),
                                mode='constant')
        else:
            deskewed[i] = shift(img[i], (0, -i*shiftStep),
                                mode='constant')

    deskewed = np.int16(deskewed)
    return deskewed


def IJ_save(img, fileout):
    # saves a ZYX volume for ImageJ import

    print('Saving image')
    # reshape to save as ImageJ TZCYXS format
    img = np.expand_dims(img, axis=1)
    img = np.expand_dims(img, axis=0)

    imsave(fileout, img, imagej=True)


def chooseDir():
    # choose a directory and move into it
    root = tkinter.Tk()
    root.withdraw()
    imDir = tkinter.filedialog.askdirectory(title='Select image directory')
    os.chdir(imDir)
