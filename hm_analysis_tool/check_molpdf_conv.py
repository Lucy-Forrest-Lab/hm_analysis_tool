#!/usr/bin/env python
import argparse
import numpy as np
from matplotlib import pyplot as plt

parser = argparse.ArgumentParser(description = 'Script that plots MOLPDF scores to evaluate convergence')
parser.add_argument("-scorefile", help="score input file (i.e format pdbfile score")
parser.add_argument("-outrms" , help="name of output score RMSD")
parser.add_argument("-outsort", help="name of output sorted score")
parser.add_argument("-ofig", help="name of the output pdf figure")
parser.add_argument("-win", help="windows size for computing score RMSD (default: 200)", default=200)
parser.add_argument("-scorecol", help="column index in score file (default: 1)", default=1)
args = parser.parse_args()

scorefile = str(args.scorefile)
rmsscorefile= str(args.outrms)
sortcorefile= str(args.outsort)
figscoreconv= str(args.ofig)
win = args.win
score_col = args.scorecol

### need to add a check if the number of scored models in scorefile is at least more than win*5

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

scorelist = col2list(scorefile,score_col)
sortscorelist=-np.sort(-scorelist)
scorerms = winrms(sortscorelist,win)

#plot results into file
fig = plt.figure(figsize=(6,10))
axis1 = fig.add_subplot(311)
axis1.plot(scorelist)
axis1.set_ylabel('MOLPDF score (a.u)')
axis1.set_xlabel('# of models')
axis2 = fig.add_subplot(312)
axis2.plot(sortscorelist)
axis2.set_ylabel('MOLPDF score (a.u.)')
axis2.set_xlabel('# of models')
axis3 = fig.add_subplot(313)
axis3.plot(scorerms)
axis3.set_ylabel('RMSD of MOLPDF score (a.u)')
axis3.set_xlabel('# of windows of (' + str(win) + ' models/window)')
fig.savefig(figscoreconv)

#transpose to make it readable and print with format
transp_rms = scorerms.T
with open(rmsscorefile, 'w+') as datafile_id:
    np.savetxt(datafile_id, transp_rms, fmt=['%1.4f'])

transp_sscore = sortscorelist.T
with open(sortcorefile, 'w+') as datafile_id:
    np.savetxt(datafile_id, transp_sscore, fmt=['%1.4f'])

