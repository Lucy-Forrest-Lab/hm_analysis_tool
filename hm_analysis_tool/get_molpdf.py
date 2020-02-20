#!/usr/bin/env python
import sys
import argparse
import glob
import pandas as pd
import numpy as np

def get_parser(args):
    '''Define inputs by the user from the command line'''
    ########## Input/output and options from user ###
    parser = argparse.ArgumentParser(description = 'Script to get all MODELLER molpdf scores from a list of pdb files in a given directory')
    parser.add_argument("-pdbdir", help="directory of the input pdb file(s)", required=True)
    parser.add_argument("-rootname", help="specify rootname of the pdb files (i.e. gly1.B)", dest="rootnm", required=True)
    parser.add_argument("-o", dest="scorefile", help="output score file", default="molpdf.txt")
    parser.add_argument("-pattern", help="pattern in pdb file to search for score, (default='MODELLER OBJECTIVE FUNCTION')", default='MODELLER OBJECTIVE FUNCTION')
    parser.add_argument("-col", help="column of MOLPDF score value in matched line of pdb (default=5)", default='5')
    return parser.parse_args(args)

######### Functions ###############
def lines_match(string, fp):
    '''make a list of matched lines in a file'''
    return [line for line in fp if string in line]

def getscore(listfiles,pattern,col):
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

def check_file_existance(ofile):
    '''check if the file file already exists'''
    try:
        f = open(ofile)
        f.close()
        print('the ' + str(ofile) + ' already exists, exiting...')
        sys.exit()
    except FileNotFoundError:
        print('the ' + str(ofile) + ' will be created')    

def get_listoffiles(directory,name):
    '''Get list of files and check if there are files in that directory'''
    listdir = glob.glob(directory + '/' + str(name) +'*.pdb')
    if len(listdir) == 0:
        print('Cannot find files in starting with ' + str(name) + ' in the ' + str(directory) + ' directory')
        sys.exit()
    return listdir

def main():
    '''Main entry point'''
    args = get_parser(sys.argv[1:])
    ########### Variables ###############
    pdbdir = str(args.pdbdir)
    rootnm = str(args.rootnm)
    # Output files/directories
    scorefile = str(args.scorefile)
    # Global variables
    scorepatt = str(args.pattern)
    colscore = int(args.col)
    #####################################

    #check if the output file already exists
    check_file_existance(scorefile) 

    # Find all *.pdb files in the pdbdir
    pdblist = get_listoffiles(pdbdir,rootnm)

    #print scores sorted by name with format
    np.savetxt(scorefile, getscore(pdblist,scorepatt,colscore).values, fmt='%s')

if __name__ == '__main__':
    main()
