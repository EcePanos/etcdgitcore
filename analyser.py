import configparser
from os import listdir


config = configparser.ConfigParser()
config.read('config.ini')
workdir = config['WORKING_ENVIRONMENT']['WORKDIR']


def compare(file1, file2):
    with open(workdir + "/" + file1, 'r') as t1, open(workdir + "/" + file2, 'r') as t2:
        fileone = t1.readlines()
        filetwo = t2.readlines()

    with open(workdir + "/" + 'update.csv', 'w') as outFile:
        for line in filetwo:
            if line not in fileone:
                outFile.write(line)
    print("Check update.csv in workdir for updated entries")

def list():
    print("Contents of workdir:")
    print(listdir(workdir))
