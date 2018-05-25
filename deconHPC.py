# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 11:28:21 2018

@author: Adam Tyson
Intel Xeon E5-2650 v3 @ 2.30Ghz 2.29Ghz, 64GB RAM:
    31 seconds for 1 iteration of 50 x 500 x 500
    163 seconds for 10 iterations of 50 x 500 x 500
    139 seconds for 1 iteration of 150 x 1024 x 1024 (Beatrice's cells)
    1383 seconds for 10 iterations of 150 x 1024 x 1024 (Beatrice's cells)
    2022 seconds for 1 iteration of 150 x 2048 x 2058 (Barry's spheroids)

HPC - 1 iteration on 150 x 1024 x 1024 (Beatrices cells) max mem approx 20GB,
        mean memory approx 11GB
            2 core:
            4 core: 78s
            8 core: 76s
            12 core: 75s
            16 core: 76s

    - 1 iteration of 150 x 2048 x 2048, max mem 81GB, mean 42GB
                4 core: reached mem limit
                8 core: 292s, 336, 320
                12 core: 304s
                16 core: 325s
    - 10 iterations of 150 x 2048 x 2048 - 2875s on 8 cores
- No multicore improvement, just use the number of cores needed for memory
"""


#def RLdecon(direc, imgFile, psfFile, iter=1, test=False, save=True):
import os
from skimage import restoration, io
import numpy as np
import sys
direc = sys.argv[1]
imgFile = sys.argv[2]
psfFile = sys.argv[3]

iter = 10
test=False
save=True

os.chdir(direc)
print(imgFile)
prefix = imgFile.rsplit('.')[0]  # remove .tif
fileout = prefix + '_decon.tif'

# Only run if exists and not decon'd allready

if not os.path.isfile(fileout):
    if os.path.isfile(imgFile):
        if os.path.isfile(psfFile):
            # 'pil' option prevents attempt to
            # load of all original timepoints in ome-tiff
            img = io.imread(imgFile, plugin='pil')
            psf = io.imread(psfFile, plugin='pil')

            if test:
                imsz = img.shape
                xmin = int(0.4*(imsz[1]))
                ymin = int(0.4*(imsz[2]))
                zmin = int(0.4*(imsz[0]))

                xmax = int(0.6*(imsz[1]))
                ymax = int(0.6*(imsz[2]))
                zmax = int(0.6*(imsz[0]))

                img = img[zmin:zmax, xmin:xmax, ymin:ymax]

            decon = restoration.richardson_lucy(
                    img, psf, iterations=iter, clip=False)
            decon = np.int16(decon)

            if save:
                io.imsave(fileout, decon)
        else:
            print('PSF does not exist')

    else:
        print('Image does not exist')

else:
    print('Image already deconvolved')
