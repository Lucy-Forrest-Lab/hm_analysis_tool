#!/usr/bin/env python
import argparse
import numpy as np
import sys
from matplotlib import pyplot as plt

def get_parser(args):
    parser = argparse.ArgumentParser(description = 'Script that plots MOLPDF scores to evaluate convergence. WARNING: all outputs will be rewritten!')
    parser.add_argument("-scorefile", help="score input file (i.e format pdbfile score")
    parser.add_argument("-outrms" , help="name of output score RMSD")
    parser.add_argument("-ofig", help="name of the output pdf figure")
    parser.add_argument("-win", help="windows size for computing score RMSD (default: 200)", default='200')
    parser.add_argument("-scorecol", help="column index in score file (default: 1)", default='1')
    return parser.parse_args(args)

######### Functions ###############

def col2list(datfile, col):
    '''Extract the column #col of datfile and write it as a list'''
    collist = []
    with open(datfile,'r') as f:
        for line in f:
            data = line.strip().split()
            #before appending into the list, check if there are empy lines
            try:
                collist.append(line.strip().split()[col])
            except IndexError:
                print('empty line')
    collist = np.array(collist).astype(np.float)
    return collist

def winrms(a, window_size):
    '''Computes windows rms of a list of values'''
    a2 = np.power(a,2)
    window = np.ones(window_size)/float(window_size)
    return np.sqrt(np.convolve(a2, window, 'valid'))

def check_numdls(ilist,win):
    '''check if the number of scored models in scorefile is at least more than win*5'''
    nummdls=(len(ilist))
    if nummdls < win*5:
        print('The total number of models, ' + str(nummdls) + ', is too little compared with the RMSD windows size,' + str(win) + '.')
        print('Please, increase the number of models to analyze, or decrease the windows size.')
        print('Exiting now...')
        sys.exit()    

def plot_opt(ilist,slist,scorerms,ofig,win):
    fig = plt.figure(figsize=(6,10))
    axis1 = fig.add_subplot(311)
    axis1.plot(ilist)
    axis1.set_ylabel('MOLPDF score (a.u)')
    axis1.set_xlabel('# of models')
    axis2 = fig.add_subplot(312)
    axis2.plot(slist)
    axis2.set_ylabel('MOLPDF score (a.u.)')
    axis2.set_xlabel('# of models')
    axis3 = fig.add_subplot(313)
    axis3.plot(scorerms)
    axis3.set_ylabel('RMSD of MOLPDF score (a.u)')
    axis3.set_xlabel('# of windows of (' + str(win) + ' models/window)')
    fig.savefig(ofig)

def main():
    '''Main entry point'''
    args = get_parser(sys.argv[1:])
    ########### Variables ###############
    # Input files/directories
    scorefile = str(args.scorefile)
    # Output files/directories
    rmsscorefile= str(args.outrms)
    figscoreconv= str(args.ofig)
    # Global variables
    win = int(args.win)
    score_col = int(args.scorecol)
    ####################################

    scorelist = col2list(scorefile,score_col)
    sortscorelist=-np.sort(-scorelist)
    scorerms = winrms(sortscorelist,win)

    ### check if the number of scored models in scorefile is at least more than win*5
    check_numdls(scorelist,win)
        
    #plot results into file
    plot_opt(scorelist,sortscorelist,scorerms,figscoreconv,win)

    #transpose to make it readable and print with format
    transp_rms = scorerms.T
    with open(rmsscorefile, 'w+') as datafile_id:
        np.savetxt(datafile_id, transp_rms, fmt=['%1.4f'])

if __name__ == '__main__':
    main()
