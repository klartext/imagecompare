#!/usr/bin/python
 
import sys
import os.path as path

from time import perf_counter as pc

from PIL import Image
import numpy as np
import hashlib as hl

import gc



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


def print_dot():
    print(".", end='', flush = True)

def print_val_if_modulo(value, modulo, prepend):
    if not value % modulo:
        print("{} {}".format(prepend, value))


# =============================================================================
# =============================================================================
# =============================================================================

if __name__ == '__main__':

    t0 = pc() # starting-time

    files_argv = sys.argv[1:]
    files = [] # list of accepted files

    print("# Try to compare {} files.".format(len(files_argv)), file=sys.stderr, flush=True)

    outfilename = "view-results.bash"
    outfile = open(outfilename, "w")
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


            bwdata = fixedscalebwthumb(fn) # filedata berechnen
            #print("idx: {}/{}, fn: {}".format(idx, len(files_argv), fn), flush=True)
            #filedata[fn]  = bwdata
            filedata[idx] = bwdata
            files.append(fn) # akzeptierte Datei
            idx = idx + 1
        except:
            print("\nignoring file \"{}\" ({}. file from command line)".format(fn, fileidx + 1), file=sys.stderr, flush=True)

    print("") # to have a newline after the dots.

    num_of_used_files = idx


    t1 = pc() # time after reading the files and creating the bw-imagedata of the thumbs

    n = num_of_used_files
    resultmatrix = np.zeros((n,n), 'f') # does sparse-matrix-Array make sense?!

    t2 = pc() # time after creating the result-array

    print("# Comparing {} files.".format(n), file=sys.stderr, flush=True)
    print("# Comparing {} files.".format(n), file=outfile, flush=True)

    # Pairwise comparison of thumbs
    # -----------------------------
    len_of_array = len(filedata[0])
    for vert in range(1,num_of_used_files):
        #print("comparing: {} with the other files.".format(files[vert]))
        print_val_if_modulo(vert + 1, 100, "vertical Count:")
        print_dot()
        for hor in range(vert):
            #print("comparing: {} with {}".format(files[vert], files[hor]))

            #diffval = np.average(np.abs(bw1 - bw2))# dies ist langsamer!
            diffval = np.sum(np.abs(filedata[vert] - filedata[hor])) / len_of_array
            resultmatrix[vert, hor] = diffval

    print("")

    #t2_2 = pc() # time after creating the result-array

    t3 = pc() # time after calculating the diff-value
    #print(resultmatrix)

    #print("# t2_2 - t2", t2_2 - t2, file=outfile)
    print("# t3 - t2", t3 - t2, file=outfile)

    print("# These files seem to have the same contents, but may differ in size:", file=outfile, flush=True)

    for idx1, fn1 in enumerate(files):
        gc.collect()
        for idx2, fn2 in enumerate(files):
            if idx2 >= idx1:
                continue # don't compare a file with itself; half matrix is sufficient

            diffval = resultmatrix[idx1, idx2]
            if diffval < 1.5:
                print("qiv -f {} {} # -> {}".format(fn1, fn2, diffval), file=outfile, flush=True)
            elif diffval >= 1.5 and diffval < 10:
                print("#qiv -f {} {} # -> {}".format(fn1, fn2, diffval), file=outfile, flush=True)


        

    t4 = pc() # time after writing the results to the outfile

t5 = pc()
print("# Dateien einlesen: {:8.3f}".format(t1 - t0), file=outfile)
#print("# t2 - t1", t2 - t1, file=outfile)
print("# Berechnung        {:8.3f}".format(t3 - t2), file=outfile)
print("# Ausgabe (Datei)   {:8.3f}".format(t4 - t3), file=outfile)
print("#", file=outfile)
print("# GESAMTZEIT        {:8.3f}".format(t4 - t0), file=outfile)

outfile.close()
print("Result has been written to \"{}\"".format(outfilename))
