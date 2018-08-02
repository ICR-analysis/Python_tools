# -*- coding: utf-8 -*-
"""

Adam Tyson | adam.tyson@icr.ac.uk | 2018-003-12

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
