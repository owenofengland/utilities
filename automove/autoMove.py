# Needed imports for the script
# Using from import statements to hopefully make script faster
from os import getcwd, makedirs, walk, listdir
from os.path import exists, dirname, isfile, isdir
from sys import argv, exit
from subprocess import call
from datetime import datetime
from timeit import default_timer
from hashlib import md5
from json import dumps

# usage function
# params: None
# returns: Void function
# Simple usage print statements, explaining how to properly call the script with arguments
def usage():
    print("Please use this script as follows with these exact arguments:")
    print("For copying from an origin to a destination other than current directory")
    print("`$ python autoMove.py [origin] [destination] [filetypes (this is a .txt file)]`\n")
    print("If you need to exclude certain files or directories")
    print("`$ python autoMove.py [origin] [destination] [filetypes] [exclude (also a .txt file)]`\n")
    print("OR\n")
    print("For copying from an origin to current directory destination")
    print("`$ python autoMove.py [origin] [filetypes (this is a .txt file)]`\n")
    print("If you need to exclude certain files or directories")
    print("`$ python autoMove.py [origin] [filetypes] [exclude (also a .txt file)]`\n")
    print("Format the filetypes.txt file as follows with file extensions!:")
    print(".txt\n.png\n.jpg\n.mov\n.shp\n")
    print("Format the exclude.txt file as follows with files and directories!")
    print("DIRECTORIES\nScripts\nFILES\nhelper.txt\n")
    print("OR\n")
    print("FILES\nhelper.txt\n")
    print("**IMPORTANT NOTE**\nDO NOT LEAVE ANY EMPTY LINES OR TRAILING WHITE SPACE IN THE .txt FILES")

# validPath function
# params: string, path to be tested
# returns: boolean, determining whether or not path exists
def validPath(testPath):
    if exists(testPath):
        return True
    return False

# fourArgExclude function
# params: strings of arguments three and four when the script is used with four arguments instead of three or five
# returns: boolean, determining whether or not the four argument execution by user contains an exclude.txt (true) or if it contains a user defined copy destination (false)
def fourArgExclude(argThree, argFour):
    if isfile(argThree) and isfile(argFour):
        return True
    elif isdir(argThree) and isfile(argFour):
        return False
    else:
        usage()
        print("Please ensure that the last two arguments are:\n1. txt file containing formats and txt file containing files and files/directories to be excluded\n2. directory to copy destination and txt file containing formats\n")
        exit(1)

# parseExclude function
# params: string, path to .txt file containing directories or files or both that should be excluded
# returns: dictionary of lists containing strings, indicating what should be ignored of what type
def parseExclude(exclude):
    try:
        with open(exclude, "r") as ft:
            exclude = [line.strip() for line in ft.readlines() if line != ""]
            excludeDir = {"directories":[], "files":[]}
            if exclude[0] == "DIRECTORIES":
                flag = True
                for i in range(1, len(exclude)):
                    if exclude[i] == "FILES":
                        flag = False
                    else:
                        if flag:
                            excludeDir['directories'].append(exclude[i])
                        else:
                            excludeDir['files'].append(exclude[i])
            elif exclude[0] == "FILES":
                flag = True
                for i in range(1, len(exclude)):
                    if exclude[i] == "DIRECTORIES":
                        flag = False
                    else:
                        if flag:
                            excludeDir['files'].append(exclude[i])
                        else:
                            excludeDir['directories'].append(exclude[i])
            else:
                usage()
                print("Please ensure that the first line indicates the type of things you would like to ignore with the following arguments.\nSee the above example.\n")
                exit(1)
            return excludeDir
    except:
        usage()
        print("Failed to open and extract exclude types from: %s\nPlease ensure the document is a text file and is correctly formatted as indicated by the above example.\n" % (exclude))

# parseFile function
# params: filetypes, path to .txt file containing desired file types to be copied
# returns: list of file extensions to be copied
# Can error out and exit if invalid
def parseFile(filetypes):
    try:
        with open(filetypes, "r") as ft:
            return [line.strip() for line in ft.readlines()]
    except:
        usage()
        print("Failed to open and extract format types from: %s\nPlease ensure the document is a text file and is correctly formatted as indicated by the above example.\n" % (filetypes))

# coreCopyUtil function
# params: formats, the list of strings that are file extensions, returned by above `parseFile` function
#         origin and destination, strings, that are valid paths
# returns: Void function
# Generates an analysis, as well as does the 'heavy lifting' in that it copies everything from origin to destination that matches the extensions in the provided formats argument
def coreCopyUtil(formats, origin, destination, exclude):
    jsonWrite = destination + "/pathtoID.json"
    jsonCount = 0
    jsonDict = {}
    analysisWrite = destination + "/analysis.txt"
    makedirs(dirname(analysisWrite), exist_ok=True)
    makedirs(dirname(jsonWrite), exist_ok=True)
    analysis = open(analysisWrite, "w")
    json = open(jsonWrite, "w")
    analysis.write("Operation performed at " + str(datetime.now()) + "\n")
    analysis.write("Analysis of copy operation performed from %s to %s\n" % (origin, destination))
    analysis.write("Analysis performed on the following filetypes\n")
    for filetypes in formats:
        analysis.write(filetypes + "\n")
    analysis.write("File paths that failed to copy:\n")
    recordSuccess = 0
    recordFailure = 0
    originLen = len(origin)
    # firstLevel = listdir(origin)
    # print(firstLevel)
    for (dirpath, dirnames, filenames) in walk(origin):
        if not any(exc in dirpath[originLen:] for exc in exclude['directories']):
            for file in filenames:
                if not any(exc in file for exc in exclude['files']):
                    extension = '.'+'.'.join(file.split(".")[1:])
                    if extension in formats:
                        toCopy = dirpath+"/"+file
                        writePath = destination + dirpath[originLen:] + "/" + file

                        hashPath = "/" + dirpath[originLen:] + "/" + file
                        jsonDict[hashPath] = {}
                        jsonDict[hashPath]['id'] = hashID = md5(hashPath.encode()).hexdigest()                        
                        jsonCount += 1

                        makedirs(dirname(writePath), exist_ok=True)
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
    analysis.write("Success ratio: %f\n" % ratio)
    analysis.close()
    jsonDict['count'] = jsonCount
    json.write(dumps(jsonDict))
    json.close()

# main Function
# params: None
# returns: Void function
# Times the length of operation, and ensures correct usage. Primarily organizes the arguments for the copy utility function.
def main():
    start = default_timer()
    if len(argv) < 3 :
        usage()
        exit(1)
    elif len(argv) > 5:
        usage()
        exit(1)
    else:
        if len(argv) == 5:
            origin, destination, filetypes, exclude = argv[1].strip(), argv[2].strip(), argv[3].strip(), parseExclude(argv[4].strip())
        elif len(argv) == 4:
            if fourArgExclude(argv[2].strip(), argv[3].strip()):
                origin, destination, filetypes, exclude = argv[1].strip(), getcwd(), argv[2].strip(), parseExclude(argv[3].strip())
            else:
                origin, destination, filetypes, exclude = argv[1].strip(), argv[2].strip(), argv[3].strip(), {"directories":[], "files":[]}
        else:
            origin, destination, filetypes, exclude = argv[1].strip(), getcwd(), argv[2].strip(), {"directories":[], "files":[]}
        if origin[-1] != "/":
            origin = origin + "/"
        if destination[-1] != "/":
            destination = destination + "/"
        if validPath(origin) and validPath(destination) and validPath(filetypes) and origin != destination:
            formats = parseFile(filetypes)
            print(origin)
            print(destination)
            print(formats)
            print(exclude)
            coreCopyUtil(formats, origin, destination, exclude)
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
