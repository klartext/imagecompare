import pytest
import numpy as np
from imagecompare import *

def test_fixedshapebwthumb_imgsize_of_testimg_is_correct():
    """Test returned imagesize for the 100x100 images - all must be 10000."""

    expected_size = 100 * 100

    filelist = \
    [
        "testimages/100x100_white.png",
        "testimages/100x100_black.png",
        "testimages/100x100_red.png",
        "testimages/100x100_green.png",
        "testimages/100x100_blue.png",
    ]


    img_sizes = [ fixedshapebwthumb(file)[1] for file in filelist] # grab sizes

    assert all( [ size == expected_size for size in img_sizes ] )




def test_fixedshapebwthumb_black_all_zeros():
    """Read testimage and check imagedata."""

    filename = "testimages/100x100_black.png"
    imgdata, imgsize = fixedshapebwthumb(filename)
    assert all(imgdata == 0)


def test_fixedshapebwthumb_white_all_255():
    """Read testimage and check imagedata."""

    filename = "testimages/100x100_white.png"
    imgdata, imgsize = fixedshapebwthumb(filename)
    assert all(imgdata == 255)


def test_fixedshapebwthumb_red_check_imgdata():
    """Read testimage and check imagedata."""

    filename = "testimages/100x100_red.png"
    imgdata, imgsize = fixedshapebwthumb(filename)
    assert all(imgdata == 76)


def test_fixedshapebwthumb_green_check_imgdata():
    """Read testimage and check imagedata."""

    filename = "testimages/100x100_blue.png"
    imgdata, imgsize = fixedshapebwthumb(filename)
    assert all(imgdata == 29)


def test_fixedshapebwthumb_blue_check_imgdata():
    """Read testimage and check imagedata."""

    filename = "testimages/100x100_blue.png"
    imgdata, imgsize = fixedshapebwthumb(filename)
    assert all(imgdata == 29)
