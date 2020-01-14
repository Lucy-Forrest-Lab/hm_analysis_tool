#!/usr/bin/env python
import math
import argparse
import sys, os
import pandas as pd
import shutil

def get_parser(args):
    '''Define inputs by the user from the command line'''
    ########## Input/output and options from user ###
    parser = argparse.ArgumentParser(description = 'Script to extract pdb files that have a MOLPDF score below a given threshold OR a percentage of the lowest MOPDF scored structures')
    parser.add_argument("-scorefile", help="input score file, format PDB_NAME MOLPDF_SCORE")
    parser.add_argument("-outdir", help="folder to write extracted pdb files")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-percent', dest="perc", help="percentage of lowest MOLPDF score to extract")
    group.add_argument('-threshold', dest="thres", help="MOLPDF score threshold of the models to extract")
    return parser.parse_args(args)

######### Functions ###############

def get_underthres(ifile,threshold):
    '''Get the list of pdbs below a given threshold'''
    df_from_file = pd.read_csv(ifile, delimiter= '\s+', names = ["pdbname", "molpdf"])
    filter_df = df_from_file[df_from_file.molpdf < threshold]
    filter_list = filter_df['pdbname'].values.tolist()
    return filter_list

def get_best_perc(ifile,perc):
    '''Get the lowest score X % structures'''
    df_from_file = pd.read_csv(ifile, delimiter= '\s+', names = ["pdbname", "molpdf"])
    df_from_file.sort_values("molpdf", axis = 0, ascending = True, inplace = True, na_position ='last')
    tot_mdls = df_from_file.shape[0]
    num_mdls = math.ceil(tot_mdls * (perc / 100))
    xtx = df_from_file.head(num_mdls)
    xtx_score = xtx.tail(1)['molpdf'].values.tolist()
    list_pdb = xtx['pdbname'].values.tolist()
    return (xtx_score, list_pdb)

def create_outdir(odir,files):
    '''Create out directory and copy files to it'''
    path = str(os.getcwd()) + '/' + odir

    try:
        os.mkdir(path)
    except OSError:
        print ("The directory %s already exists and it will not be overwritten. Exiting..." % path)
        sys.exit()
    else:
        print ("The %s directory will be created and pdbs will be copied" % path)
        for f in files:
            shutil.copy(f,path)

def print_log_thr(odir,threshold,tot):
    '''Print a log file with the threshold info'''
    logfile = str(os.getcwd()) + '/' + odir + '/log.txt'
    flog = open(logfile,"w") 
    flog.write("PDB structures below %s MOLPDF score: %d mdls" % (threshold, tot)) 
    flog.close()

def print_log_perc(odir,perc,score,tot):
    '''Print a log file with the threshold info'''
    logfile = str(os.getcwd()) + '/' + odir + '/log.txt'
    flog = open(logfile,"w")
    flog.write("%s percent of PDB structure with lowest MOLPDF score: %d mdls, highest score is %.4f" % (perc,tot,score))
    flog.close()

def main():
    args = get_parser(sys.argv[1:])
    '''Main entry point'''
    ########### Variables ###############
    scorefile = str(args.scorefile)
    # Output files/directories
    outdir = str(args.outdir)

    ## Define analysis by perc of mdls or under threshold
    if args.perc != None:
        perc=int(args.perc)
        xtx_score, list_pdb = (get_best_perc(scorefile,perc))
        create_outdir(outdir,list_pdb)
        num_mdls = len(list_pdb)
        print_log_perc(outdir,perc,xtx_score[0],num_mdls)

    if args.thres != None:
        thres = int(args.thres)
        list_pdb = (get_underthres(scorefile,thres))
        create_outdir(outdir,list_pdb)
        num_mdls = len(list_pdb)
        print_log_thr(outdir,thres,num_mdls)
   
if __name__ == '__main__':
    main()
