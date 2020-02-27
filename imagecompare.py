#!/usr/bin/python

"""
    This tool aims to find out similar or equal image-files.
    The basic idea has two parts:
        1) reducing the data of the comparison while being accurate enough
        2) comparing the files via the reduced data

    Solution to 1): comparing black-/white-thumbnails of the images,
    scaled down to a fixed rectangle shape.
    Solution to 2): calculate the pixel-difference of the images, and take the average
    of the absolute value of that difference, and compare that value with a
    threshold.
    $ coeff = \frac{1}{n}\sum_{i=1}^n | x_i - y_i | $
    Thresholds:   1.5  for very similar / nearly equal images
                  10.0 for similar files

    Similar files will be printed into a file that can be called as shell-script,
    which then calls the image-viewer qiv in fullscreen-mode.
    The image viewer will be invoked for two files each.
    Then deleting the files that can be deleted is done 'by hand'.
    If a file has more than one file that is similar, they nevertheless
    will be called pairwise. So, for already deleted files the viewer might
    be called nevertheless. Don't become confused by that.
    Have also in mind, that an image an it's thumbnail (or an image just scaled
    to different resolutions) will be regarded as similar images.
"""
 
import sys
import os.path as path

from time import perf_counter as pc

from PIL import Image
import numpy as np

import gc


# Settings, hardcoded
# -------------------
outfilename = "view-results.bash" # hardcode value: filename


#############
# FUNCTIONS #
#############

def fixedscalebwthumb(filename):
    """
    Creates onedim. array of the b/w image data of image-file.
    """
    img = Image.open(filename)

    thumb = img.resize([100,100], Image.LANCZOS) # hardcode value: fixed thumb-size
    bwthumb = thumb.convert('L')

    data = np.array(bwthumb.getdata())

    img.close()

    return data


def calc_imagediffcoeff( bwimg_1, bwimg_2 ):
    """
    The arguments bwimg_1 and bwimg_2 are numpy-arrays,
    repesenting the black-white/grayscale-images and must have the
    same dimensions (same shape).
    $ coeff = \frac{1}{n}\sum_{i=1}^n | x_i - y_i | $
    """
    absdiff = abs(bwimg_1 - bwimg_2)
    return sum(absdiff)/len(absdiff)


def print_dot():
    print(".", end='', flush = True)

def print_val_if_modulo(value, modulo, prepend):
    if not value % modulo:
        print("{} {}".format(prepend, value))


# =============================================================================
# =============================================================================
# =============================================================================

if __name__ == '__main__':

    t0 = pc() # starting timer value

    # check if filenames were given at all. Ifnot: message and exit
    if len(sys.argv) < 2:
        print("filenames as arguments needed!")
        exit(1)

    files_argv = sys.argv[1:]
    files = [] # list of accepted files

    print("# {} filenames given on command line.".format(len(files_argv)), file=sys.stderr, flush=True)

    outfile = open(outfilename, "w")

    # Now read the image-files and store the b/w-data of the their thumbnails
    # -----------------------------------------------------------------------
    print("# Reading in files.", file=sys.stderr, flush=True)
    print("# Reading in files.", file=outfile, flush=True)

    filedata = {}
    idx = 0
    for fileidx, fn in enumerate(files_argv):
        print_dot()
        print_val_if_modulo(idx + 1, 100, "Read file number")
        try:
            if path.islink(fn):
                print("\nignoring symbolic link \"{}\" ({}. file from command line)".format(fn, fileidx + 1), file=sys.stderr, flush=True)
                continue

            if path.isdir(fn):
                print("\nignoring dir \"{}\" ({}. file from command line)".format(fn, fileidx + 1), file=sys.stderr, flush=True)
                continue

            bwdata = fixedscalebwthumb(fn) # calculate filedata
            filedata[idx] = bwdata
            files.append(fn) # accepted file
            idx = idx + 1

        except:
            print("\nignoring file \"{}\" ({}. file from command line, could not be opened as image.)".format(fn, fileidx + 1), file=sys.stderr, flush=True)

    print("") # to have a newline after the dots.

    filecount = idx # number of files

    t1 = pc() # timer value after reading the files and creating the bw-imagedata of the thumbs

    resultmatrix = np.zeros((filecount, filecount), 'f') # does sparse-matrix-Array make sense?!

    t2 = pc() # timer value after creating the result-array

    print("# Comparing {} files.".format(filecount), file=sys.stderr, flush=True)
    print("# Comparing {} files.".format(filecount), file=outfile, flush=True)

    # Pairwise comparison of thumbs (1/2 * num^2 comparisons)
    # -------------------------------------------------------
    len_of_array = len(filedata[0]) # actual length of the thumbnail-array
    for vert in range(1,filecount):
        print_val_if_modulo(vert + 1, 100, " Comparing files with file number:")
        print_dot()
        for hor in range(vert):
            #diffval = np.average(np.abs(bw1 - bw2))# dies ist langsamer!
            diffval = np.sum(np.abs(filedata[vert] - filedata[hor])) / len_of_array
            resultmatrix[vert, hor] = diffval

    print("")

    t3 = pc() # timer value after calculating the diff-value

    print("# t3 - t2", t3 - t2, file=outfile)

    print("# These files seem to have the same contents, but may differ in size:", file=outfile, flush=True)

    # Writing the results: pairwise print similar files on one line with
    # call of image-viewer 'qiv'
    # ------------------------------------------------------------------
    for idx1, fn1 in enumerate(files):
        gc.collect() # is that necessary? performance might be tested again.
        for idx2, fn2 in enumerate(files):
            if idx2 >= idx1:
                continue # don't compare a file with itself; half matrix is sufficient

            diffval = resultmatrix[idx1, idx2]
            if diffval < 1.5: # hardcoded value very-similar images
                print("qiv -f {} {} # -> {}".format(fn1, fn2, diffval), file=outfile, flush=True)
            elif diffval >= 1.5 and diffval < 10: # hard coded value similar images
                print("#qiv -f {} {} # -> {}".format(fn1, fn2, diffval), file=outfile, flush=True)

    t4 = pc() # timer value after writing the results to the outfile

    print("# Dateien einlesen: {:8.3f}".format(t1 - t0), file=outfile)
    print("# Berechnung        {:8.3f}".format(t3 - t2), file=outfile)
    print("# Ausgabe (Datei)   {:8.3f}".format(t4 - t3), file=outfile)
    print("#", file=outfile)
    print("# GESAMTZEIT        {:8.3f}".format(t4 - t0), file=outfile)

    outfile.close()
    print("Result has been written to \"{}\"".format(outfilename))
