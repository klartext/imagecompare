#!/usr/bin/python
 
import sys

from PIL import Image
import numpy as np
import hashlib as hl




def fixedscalebwthumb(filename):
    """
    Creates onedim. array of the b/w image data of image-file.
    """
    img = Image.open(filename)

    thumb = img.resize([100,100], Image.LANCZOS)
    #thumb.save("_" + filename)
    bwthumb = thumb.convert('L')

    data = np.array(bwthumb.getdata())

    img.close()

    return data


def calc_imagediffcoeff( bwimg_1, bwimg_2 ):
    """
    The arguments bwimg_1 and bwimg_2 are numpy-arrays,
    repesenting the black-white/grayscale-images and must have the
    same dimensions (same shape).
    """
    absdiff = abs(bwimg_1 - bwimg_2)
    return sum(absdiff)/len(absdiff)



files = sys.argv[1:]


filedata = {}
for fn in files:
    filedata[fn] = fixedscalebwthumb(fn)



print(files)
n = len(files)
resultmatrix = np.zeros((n,n), 'f')

for idx1, fn1 in enumerate(files):
    for idx2, fn2 in enumerate(files):
        if idx2 >= idx1:
            continue # don't compare a file with itself; half matrix is sufficient
        bw1 = filedata[fn1]
        bw2 = filedata[fn2]

        diffval = sum(abs(bw1 - bw2)) / len(bw1)
        resultmatrix[idx1, idx2] = diffval

#print(resultmatrix)

for idx1, fn1 in enumerate(files):
    for idx2, fn2 in enumerate(files):
        if idx2 >= idx1:
            continue # don't compare a file with itself; half matrix is sufficient

        diffval = resultmatrix[idx1, idx2]
        if diffval < 10:
            print("{} / {} -> {}".format(fn1, fn2, diffval))


    
