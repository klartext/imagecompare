#!/usr/bin/python
 
import sys
from time import perf_counter as pc

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



# =============================================================================
# =============================================================================
# =============================================================================

if __name__ == '__main__':

    t0 = pc() # starting-time

    files = sys.argv[1:]


    outfilename = "view-results.bash"
    outfile = open(outfilename, "w")
    print("# Reading in files.", file=outfile, flush=True)
    filedata = {}
    for fn in files:
        filedata[fn] = fixedscalebwthumb(fn)

    t1 = pc() # time after reading the files and creating the bw-imagedata of the thumbs

    n = len(files)
    resultmatrix = np.zeros((n,n), 'f') # does sparse-matrix-Array make sense?!

    t2 = pc() # time after creating the result-array

    print("# Comparing in files.", file=outfile, flush=True)
    for idx1, fn1 in enumerate(files):
        for idx2, fn2 in enumerate(files):
            if idx2 >= idx1:
                continue # don't compare a file with itself; half matrix is sufficient
            bw1 = filedata[fn1]
            bw2 = filedata[fn2]

            diffval = sum(abs(bw1 - bw2)) / len(bw1)
            resultmatrix[idx1, idx2] = diffval

    t3 = pc() # time after calculating the diff-value
    #print(resultmatrix)


    print("# These files seem to have the same contents, but may differ in size:", file=outfile, flush=True)

    for idx1, fn1 in enumerate(files):
        for idx2, fn2 in enumerate(files):
            if idx2 >= idx1:
                continue # don't compare a file with itself; half matrix is sufficient

            diffval = resultmatrix[idx1, idx2]
            if diffval < 10:
                #print("{} / {} -> {}".format(fn1, fn2, diffval), file=outfile, flush=True)
                print("qiv -f {} / {} # -> {}".format(fn1, fn2, diffval), file=outfile, flush=True)


        

    t4 = pc() # time after writing the results to the outfile

print("# t1 - t0", t1 - t0, file=outfile)
print("# t2 - t1", t2 - t1, file=outfile)
print("# t3 - t2", t3 - t2, file=outfile)
print("# t4 - t3", t4 - t3, file=outfile)
print("#", file=outfile)
print("# t4 - t0", t4 - t3, file=outfile)

outfile.close()
print("Result has been written to \"{}\"".format(outfilename))
