#!/usr/bin/env python
import sys
import argparse
import glob
import pandas as pd
import numpy as np

# Read inputs from prompt
parser = argparse.ArgumentParser(description = 'Script to get all MODELLER molpdf scores from a list of pdb files in a given directory')
parser.add_argument("-pdbdir", help="directory of the input pdb file(s)")
parser.add_argument("-rootname", help="specify rootname of the pdb files (i.e. gly1.B)", dest="rootnm")
parser.add_argument("-o", dest="scorefile", help="output score file")
parser.add_argument("-pattern", help="pattern in pdb file to search for score, (default='MODELLER OBJECTIVE FUNCTION')",
        default='MODELLER OBJECTIVE FUNCTION')
parser.add_argument("-col", help="column of MOLPDF score value in matched line of pdb (default=5)", default=5)
args = parser.parse_args()

# Assign prompted inputs to variables
pdbdir = str(args.pdbdir)
pattern = str(args.pattern)
scorefile = str(args.scorefile)
rootnm = str(args.rootnm)
colscore = args.col

# Find all *.pdb files in the pdbdir
pdblist = glob.glob(pdbdir + '/' + rootnm +'*.pdb')

#check if there are pdbs to analyze in the input folder
if len(pdblist) == 0:
    print('the are not pdb files in starting with ' + rootnm + ' in the ' + pdbdir + ' directory')

#check if the output file exists
try:
    f = open(scorefile)
    f.close()
    print('the ' + str(scorefile) + ' already exists, exiting...')
    sys.exit()
except FileNotFoundError:
    print('the ' + str(scorefile) + ' will be created')


def lines_match(string, fp):
    '''make a list of matched lines in a file'''
    return [line for line in fp if string in line]

def getscore(listfiles, col):
    '''From a set of files extract a dataframe with the file name and col of lines matching a pattern in that file'''
    column1 = []
    column2 = []
    for ifile in listfiles:
        try:
            with open(ifile,'r') as f:
                for line in lines_match(pattern, f):
                    column1.append(ifile)
                    column2.append(line.strip().split()[col])
        except IndexError:
                print('input column of pdb file score line is not correct')
    col1col2 = pd.DataFrame(list(zip(column1,column2)), columns=['col1','col2'])
    return col1col2.sort_values(by=['col1'])

#print scores sorted by name with format
np.savetxt(scorefile, getscore(pdblist,colscore).values, fmt='%s')
