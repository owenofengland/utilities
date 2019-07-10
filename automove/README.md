# Automove Copy Utility
Owen England

## Installation and Packages


* Python 3 was used to write this utility
* Using anaconda
* OS, sys, subprocess, datetime, and timeit were used (these should already be included with your python installation)


## Anaconda Install Information


 * For a tutorial on installing anaconda via CLI: https://www.digitalocean.com/community/tutorials/how-to-install-anaconda-on-ubuntu-18-04-quickstart
 * For a tutorial on setting up an environment after, and installing OSGEO with GDAL and OGR: https://hackernoon.com/install-python-gdal-using-conda-on-mac-8f320ca36d90


## Using this utility


* The only file in this directory is autoMove.py
* This file will recursively copy all files with the user given file extensions from an origin to a destination
* It can be used in one of two ways:
1. `$ python autoMove.py [origin] [destination] [filetypes]`
This method will copy all filetypes in `filetypes` from the user provided `origin` to the user provided `destination`
2. `$ python autoMove.py [origin] [filetypes]`
This method will copy all filetypes in `filetypes` from the user provided `origin` to the **current directory** (aka *where the script is*)

* Origin and destination arguments are file paths
* Filetypes argument is a text file with newline separated file extensions, as an example:

.txt

.png

.doc

.pdf


* Running this script will copy everything that matches the provided file types to the destination (with exact filenames, extensions, directory naming, etc.) and generate a report of the operation, called `analysis.txt`, as well as information about how long it took to run the operation



