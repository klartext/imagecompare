import pytest
import numpy as np
from imagecompare import *


# Testing fixedshapebwthumb()
# ===========================
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



# Testing class ImageThumb
# ========================
def test_imagethumb_creates_object_from_testimage():
    """Test if one of the testmages will be read and no exception occurs."""
    file = "testimages/100x100_black.png"

    imgthumb = ImageThumb(file)


def test_imagethumb_throws_exception_for_nonexisting_image():
    """Opening a non-image, ImageThumb() throws exception.

    In the program this exception is caught. But it is expceted to be raised,
    when ImageThumb() is pushed to open a non-image file. So here the occurrence
    of the exception is tested.
    """

    with pytest.raises(PIL.UnidentifiedImageError):
        ImageThumb("imagecompare") # imagethumb can't read itself as an image


def test_imagethumb_returns_correct_length_1():
    """Test correct implementation of __len__ on a testimage."""

    file = "testimages/100x100_black.png"
    imgthumb = ImageThumb(file)
    assert len(imgthumb) == 100 * 100


def test_imagethumb_returns_correct_length_2():
    """Test correct implementation of __len__ on a testimage.

    Tests the number of pixels of the thumbs.
    See docstring of fixedshapebwthumb().
    Curently the shape ius 100 x 100, so the size of bwthumb-data is
    100 * 100 = 10000.
    """

    file = "testimages/10x10_black.png"
    imgthumb = ImageThumb(file)
    assert len(imgthumb) == 100 * 100


def test_imagethumb_size_comparison_lt_correct():

    small_img = "testimages/10x10_black.png"
    large_img = "testimages/100x100_black.png"

    th_smaller = ImageThumb(small_img)
    th_larger  = ImageThumb(large_img)

    assert th_smaller < th_larger


def test_imagethumb_substraction_yields_correct_diff_array_1():
    """Compare difference between the thumb image data arrays."""

    file_1 = "testimages/100x100_red.png"
    file_2 = "testimages/100x100_blue.png"

    thumb_1 = ImageThumb(file_1)
    thumb_2 = ImageThumb(file_2)

    diff = thumb_1 - thumb_2

    assert all(diff == 76 - 29)


def test_imagethumb_substraction_yields_correct_diff_array_2():
    """Compare difference between the thumb image data arrays."""

    file_1 = "testimages/100x100_black.png"
    file_2 = "testimages/100x100_blue.png"

    thumb_1 = ImageThumb(file_1)
    thumb_2 = ImageThumb(file_2)

    diff = thumb_1 - thumb_2

    assert all(diff == (0 - 29))


def test_imagethumb_substraction_yields_correct_diff_array_3():
    """Compare difference between the thumb image data arrays."""

    file_1 = "testimages/100x100_white.png"
    file_2 = "testimages/100x100_blue.png"

    thumb_1 = ImageThumb(file_1)
    thumb_2 = ImageThumb(file_2)

    diff = thumb_1 - thumb_2

    assert all(diff == (255 - 29))


# very simple exaple for the test; might add other testimages and tests later
def test_imagethumb_distance_1():
    """Check staticmethod 'dist' for it's value and on abs()."""
    file_1 = "testimages/100x100_white.png"
    file_2 = "testimages/100x100_blue.png"

    thumb_1 = ImageThumb(file_1)
    thumb_2 = ImageThumb(file_2)

    distance_forward = thumb_1.dist(thumb_1, thumb_2)
    distance_backward = thumb_1.dist(thumb_2, thumb_1)

    assert distance_forward  == 226 # the average distance
    assert distance_backward == 226 # the average distance, where abs() matters


