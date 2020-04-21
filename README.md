# imagecompare - a tool to compare images

## What imagecompare does

This tool is intended to find image files that contain equal or similar image contents
and be started from the command line of a shell.

## Use Cases

Find out and possibly remove duplicate images, which means images, that have same or
similar contents but may differ in file contents.

An image and a thumbnail of that image, even though they have different size,
can be seen as providing the same image contents.

Jpg files with same image information but different jpg comments / different exif information
will be detected.


# Dependencies / Installation / Invocation

This program is written in Python and **Python3** is neded.

The following packages are also needed:

**Numpy**

**PIL** (Python Pillow)

The tool is completely contained in one python file, so it's sufficient to
copy it into your ~/bin directory (or call it directly).
You may also need to check / change executable flags with chmod.


# Usage

## How imagecompare will be used and some background information

Files that has been detected as similar are gathered into sets, and each set of similar
files is printed space-seperated on its own line into an output file.
The name of the output file is **view-results.bash**.

This output file is meant to be run from the shell as shell script (with bash shell in mind).

So this file contains bash commands to start an image viewer on each set of similar files,
as well as some additional information in form of bash comments.

The files of each detected set are sorted by size before printed to the file,
so that the largest file is mentioned first on each line (descending order of size).

The default viewer command - and at the moment implemented fixed as the only one -
is the call to the imageviewer **qiv** in fullscreenmode
and without sorting of the filenames.

After calling **imagecompare**, the output file can be called as
bash script.
When calling the output file as a script from the shell prompt,
the viewer shows the images that are detected to be similar (if there are some),
with the first one shown being the largest one.
After quitting **qiv** it may be called again by that bash script on the next set of similar images.

Use 'space' to view the next image and 'd' to delete them.
(They will be moved to .qiv-trash not deleted.)



## Usage example


The program is invoked with the filenames as arguments:

    $ imagecompare *.jpg *.png

Then the program reads the images and compares them,
and finally writes the output file.
This file then can be called as shell script:

    $ bash view-results.bash

Then the set of similar images can be viewed and possibly deleted by the user.


## Command line switches

The switch ***```--help```*** or ***```-h```*** will print a help message,
listing usage syntax and command line arguments.

When command line switch ***```--bare```*** or ***```-b```*** is given,
only the lines with similar files are printed.
No extra information and no viewer command will be written.

For selecting the treshold of the comparison of images,
the command line argument ***```--treshold```*** or ***```-t```***
is available. It is a float argument, and the default value is 1.5.

Using a treshold of 1.5 means the images will be very similar.
Sometimes a value up to 3.0 might make sense.
These values make sense to detect images with / without some text overlayed as similar.

With values of about 10.0 images may look similar, but will likely already differ in
the overall contents (not just some overlayed text).


Possible command line switch in the future:

- select other output filename,
- select other viewer command,

Stay tuned to get a newer version of this tool.


# More information

For a more into details description, when you are in the directory that contains
imagecompare, you can type at your shell prompt ($):

    $ head -72 imagecompare | less


