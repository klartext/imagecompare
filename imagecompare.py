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
    for idx, fn in enumerate(files):
        try:
            filedata[fn] = fixedscalebwthumb(fn) # filedata berechnen
            filedata[idx] = filedata[fn]
        except:
            print("ignoring file \"{}\"".format(fn), file=sys.stderr, flush=True)
            files.remove(fn)


    #print(filedata.keys())
    t1 = pc() # time after reading the files and creating the bw-imagedata of the thumbs

    n = len(files)
    resultmatrix = np.zeros((n,n), 'f') # does sparse-matrix-Array make sense?!

    t2 = pc() # time after creating the result-array

    print("# Comparing files.", file=outfile, flush=True)

    #len_of_array = len(filedata[0])
    #aver_div = 1.0 / len_of_array
    len_files = len(files)
    for vert in range(1,len_files):
        for hor in range(vert):
            bw1 = filedata[vert]
            bw2 = filedata[hor]
            #print("idx1/vert, idx2/hor: {} , {}".format(vert, hor))

            diffval = np.average(np.abs(bw1 - bw2))
            #diffval = np.sum(np.abs(filedata[fn1] - filedata[fn2])) / len(bw1)
            resultmatrix[vert, hor] = diffval

    #t2_2 = pc() # time after creating the result-array

    """
    for idx1, fn1 in enumerate(files):
        for idx2, fn2 in enumerate(files):
            if idx2 >= idx1:
                continue # compare only below the diagonal
            bw1 = filedata[fn1]
            bw2 = filedata[fn2]
            #print("idx1, idx2: {} , {}".format(idx1, idx2))

            diffval = np.sum(np.abs(bw1 - bw2)) / len(bw1)
            #diffval = np.sum(np.abs(filedata[fn1] - filedata[fn2])) / len(bw1)
            resultmatrix[idx1, idx2] = diffval
    """

    t3 = pc() # time after calculating the diff-value
    #print(resultmatrix)

    #print("# t2_2 - t2", t2_2 - t2, file=outfile)
    print("# t3 - t2", t3 - t2, file=outfile)

    print("# These files seem to have the same contents, but may differ in size:", file=outfile, flush=True)

    for idx1, fn1 in enumerate(files):
        for idx2, fn2 in enumerate(files):
            if idx2 >= idx1:
                continue # don't compare a file with itself; half matrix is sufficient

            diffval = resultmatrix[idx1, idx2]
            if diffval < 1.5:
                #print("{} / {} -> {}".format(fn1, fn2, diffval), file=outfile, flush=True)
                print("qiv -f {} {} # -> {}".format(fn1, fn2, diffval), file=outfile, flush=True)


        

    t4 = pc() # time after writing the results to the outfile

t5 = pc()
print("# t1 - t0", t1 - t0, file=outfile)
print("# t2 - t1", t2 - t1, file=outfile)
print("# t3 - t2", t3 - t2, file=outfile)
print("# t4 - t3", t4 - t3, file=outfile)
print("#", file=outfile)
print("# t4 - t0", t4 - t0, file=outfile)

print("prints:", t5-pc())
outfile.close()
print("Result has been written to \"{}\"".format(outfilename))
