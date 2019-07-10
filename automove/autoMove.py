import os
from sys import argv, exit
from subprocess import call
from datetime import datetime
from timeit import default_timer

def usage():
    print("Please use this script as follows with these exact arguments: \n")
    print("For copying from an origin to a destination other than current directory\n")
    print("`$ python autoMove.py [origin] [destination] [filetypes (this is a .txt file)]\n`")
    print("OR\n")
    print("For copying from an origin to current directory destination\n")
    print("`$ python autoMove.py [origin] [filetypes (this is a .txt file)]\n`")
    print("Format the filetypes.txt file as follows with file extensions!: \n")
    print(".txt\n.png\n.jpg\n.mov\n.shp\n")

def validPath(testPath):
    if os.path.exists(testPath):
        return True
    return False

def parseFile(filetypes):
    try:
        with open(filetypes, "r") as ft:
            return [line.strip() for line in ft.readlines()]
    except:
        usage()
        print("Failed to open and extract format types from: %s\nPlease ensure the document is a text file and is correctly formatted as indicated by the above example.\n" % (filetypes))

def coreCopyUtil(formats, origin, destination):
    analysisWrite = destination + "/analysis.txt"
    os.makedirs(os.path.dirname(analysisWrite), exist_ok=True)
    analysis = open(analysisWrite, "w")
    analysis.write("Operation performed at " + str(datetime.now()) + "\n")
    analysis.write("Analysis of copy operation performed from %s to %s\n" % (origin, destination))
    analysis.write("Analysis performed on the following filetypes\n")
    for filetypes in formats:
        analysis.write(filetypes + "\n")
    analysis.write("File paths that failed to copy:\n")
    recordSuccess = 0
    recordFailure = 0
    originLen = len(origin)
    for (dirpath, dirnames, filenames) in os.walk(origin):
        for file in filenames:
            extension = '.'+'.'.join(file.split(".")[1:])
            if extension in formats:
                toCopy = dirpath+"/"+file
                writePath = destination + dirpath[originLen:] + "/" + file
                os.makedirs(os.path.dirname(writePath), exist_ok=True)
                try:
                    call(['cp',toCopy,writePath])
                    recordSuccess += 1
                except:
                    recordFailure += 1
                    analysis.write(toCopy + "\n")
    if recordFailure == 0:
        ratio = 1
    else:
        ratio = recordSuccess/recordFailure
    analysis.write("%f\n" % ratio)
    analysis.close()

def main():
    start = default_timer()
    if len(argv) < 3 :
        usage()
        exit(1)
    elif len(argv) > 4:
        usage()
        exit(1)
    else:
        if len(argv) == 4:
            origin, destination, filetypes = argv[1].strip(), argv[2].strip(), argv[3].strip()
        else:
            origin, destination, filetypes = argv[1].strip(), os.getcwd(), argv[2].strip()
        if origin[-1] != "/":
            origin = origin + "/"
        if destination[-1] != "/":
            destination = destination + "/"
        if validPath(origin) and validPath(destination) and validPath(filetypes) and origin != destination:
            formats = parseFile(filetypes)
            print(origin)
            print(destination)
            print(formats)
            coreCopyUtil(formats, origin, destination)
            stop = default_timer()
            print("Operation finished\n")
            print("Operation took: %f seconds" % (stop-start))
            print("Wrote analysis of operation to %s\n" % (destination))
        elif origin == destination:
            usage()
            print("Please ensure that origin and destination are not the same!\n")
            exit(1)
        else:
            usage()
            print("Please ensure the following paths exist and are correct:\nOrigin: %s\nDestination: %s\nFiletypes: %s\n" % (origin, destination, filetypes))
            exit(1)

if __name__ == "__main__":
    main()