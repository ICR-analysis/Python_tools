# -*- coding: utf-8 -*-
"""
Macro to deskew MLS stage scans.
Adam Tyson | adam.tyson@icr.ac.uk | 2018-05-24

Adapted from ImageJ macro by Min Guo & Hari Shroff (2016)
http://dispim.org/software/imagej_macro

Define deskew parameters, and choose directory containing skewed images (.tif)
All images in the directory will be deskewed, and saved to /deskew


TODO: add deskewing, then make into deskew function
"""

import os
from skimage import io
from datetime import datetime
from fun.deskew import chooseDir, deskew, IJ_save
startTime = datetime.now()

chooseDir()


class var:
    save = True
    direc = 'Left2Right'  # or 'Right2Left'
    stepType = 'Z_spacing'  # or 'StageDistance'
    interval = 0.8
    pixelsize = 0.1625


if var.stepType is 'StageDistance':
    shiftStep = var.interval/1.414/var.pixelsize
else:
    shiftStep = var.interval/var.pixelsize

allFiles = os.listdir('.')
for file in allFiles:
    if file.endswith(".tif"):
        prefix = file.rsplit('.')[0]  # remove .tif
        fileout = prefix + '_deskew.tif'

        # Only run if not deskewed allready
        if not os.path.isfile(fileout):

            print('Loading image: ', file)

            # 'pil' option prevents attempt to
            # load of all original timepoints in ome-tiff
            img = io.imread(file, plugin='pil')

            deskewed = deskew(img, var.direc, shiftStep)

            if var.save:
                IJ_save(deskewed, fileout)

        else:
            print('Image already deskewed')


print('Done!')
print('Total time taken: ', datetime.now() - startTime)
