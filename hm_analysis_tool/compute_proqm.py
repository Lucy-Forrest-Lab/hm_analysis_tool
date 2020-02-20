#!/usr/bin/env python
import argparse
import sys, os
import shutil
import subprocess
import glob
import re

def get_parser(args):
    '''Define inputs by the user from the command line'''
    ########## Input/output and options from user ###
    parser = argparse.ArgumentParser(description = 'Compute the PROQM score for a list of PDB files. For running this script you need to have up and running ProQ2/QM master script, EMBOSS (needle command) and Rosetta (version 3.5 and up). You also need to indicate the location of a local copy of uniprot and Rosetta database. The PDB of the models needs to be in the working directory and have the same rootname that the one of the alignment pir file')
    parser.add_argument("-tmpldir", help="directory of the template models file(s) to analyze", required=True)
    parser.add_argument("-alignment_pir", help="full path to the alignment modeller PIR file between target and template, template name and rootname of models will be read from the alignment file", required=True)
    parser.add_argument("-full_seq_mdl", help="full-length sequence of the model in fasta format (file has to be in the working directory)", dest="fasta_mdl" )
    parser.add_argument("-full_seq_template", help="full-length sequence of the model in fasta format (file has to be in the working directory)", dest="fasta_template")
    parser.add_argument("-rosetta_score_app", help="Rosetta score application (default: /data/TMB-CSB/apps/CentOS7-LabLinux/rosetta/3.9/main/source/bin/score.static.linuxgccrelease)", default="/data/TMB-CSB/apps/CentOS7-LabLinux/rosetta/3.9/main/source/bin/score.static.linuxgccrelease")
    parser.add_argument("-proqm_script", help="ProQ master script bin folder (default: /home/leonealvarezva/software/ProQ_scripts/bin/)", default="/home/leonealvarezva/software/ProQ_scripts/bin/")
    parser.add_argument("-rosetta_db", help="Rosetta database folder (default: /data/TMB-CSB/apps/CentOS7-LabLinux/rosetta/3.9/main/database/)", default="/data/TMB-CSB/apps/CentOS7-LabLinux/rosetta/3.9/main/database/")
    return parser.parse_args(args)
    #modeller inst? write pir to fasta?

######### Functions ###############
def check_file_existance(ofile):
    '''check if the file file already exists'''
    try:
        f = open(ofile)
        f.close()
        print('the ' + str(ofile) + ' already exists, will be deleted')
        os.remove(ofile)
    except FileNotFoundError:
        print('the ' + str(ofile) + ' will be created')

def rootnm_from_pir(string, fp):
    '''get matched lines in a file'''
    for line in open(fp):
        if string in line:
            return line.split(":")[1]

def find_not_matches(string1,string2,string3,string4,string5, fp):
    '''get not matched lines in a file'''
    for line in fp:
        if string1 not in line and string2 not in line and string3 not in line and string4 not in line and string5 not in line:
            yield line

def print_clean_pdb(pdbin):
    '''print a clean pdb without the patched terminal atoms'''
    pdbout=str(pdbin) + 'cl'
    check_file_existance(pdbout)
    with open(pdbin, 'r') as fp:
        for line in find_not_matches(' CAY ',' CY ',' OY ', ' NT ', ' CAT ', fp):
            with open(pdbout, 'a') as noterpdb:
                noterpdb.write(line)
    return pdbout

def num_res(fp):
    '''Get the number of residues from the profile span file'''
    with open(fp) as open_file:
        file_lines=open_file.readlines()
        return file_lines[1].strip().split()[1]

def get_listoffiles(directory,name):
    '''Get list of files and check if there are files in that directory'''
    listdir = glob.glob(directory + '/' + str(name) + '*.pdb')
    if len(listdir) == 0:
        print('Cannot find files in starting with ' + str(name) + ' in the ' + str(directory) + ' directory')
        sys.exit()
    return listdir

def get_profile(proqmdir,fpdb,fullseq):
    '''Compute the PROQM profile'''
    try:
        f = open(fullseq)
        f.close()
        print('\n\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\nIMPORTANT: the full-sequence and the sequence from the pdb file MUST be 100% identical,\nexcept for the missing regions (it cannot contain mutations, i.e. variants to improve\ncrystallization or stabilize a conformation. If the pdb file has a mutation, change\nthe full-sequence accordingly before generating the ProQM profile\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n')

        print('Creating a ProQM profile for ' + str(fullseq) + '. This can take some time...')
        proqm_allext = subprocess.Popen(["perl", str(proqmdir) + '/run_all_external.pl', '-fasta', str(fullseq), '-membrane', '1'], stdout=sys.stdout)
        proqm_allext.communicate()
        print('Copy the profile features for the ' + str(fullseq) + ' to the sequence in the ' + str(fpdb) + ' PDB file')
        proqm_copy = subprocess.Popen(["perl", str(proqmdir) + '/copy_features_from_master.pl', str(fpdb), str(fullseq)], stdout=sys.stdout)
        proqm_copy.communicate()
    except FileNotFoundError:
        print('Creating a ProQM profile for the sequence in the PDB file ' + str(fpdb) + '. This can take some time...')
        proqm_allext = subprocess.Popen(["perl", str(proqmdir) + '/run_all_external.pl', '-pdb', str(fpdb), '-membrane', '1'], stdout=sys.stdout)
        proqm_allext.communicate()

def compute_proqm(scoreapp,rosettadb,basename,pdb,nres):
    '''Use Rosetta score application to compute ProqQM score for a pdb file'''
    subprocess.call([str(scoreapp),
                    '-database', str(rosettadb),
                    '-in:file:fullatom',
                    '-ProQ:basename', str(basename),
                    '-in:file:s', str(pdb),
                    '-ignore_unrecognized_res',
                    '-Ntermini', 'ALL',
                    '-Ctermini', 'ALL',
                    '-out:file:scorefile', 'ProQM.sc',
                    '-score:weights', 'ProQM',
                    '-ProQ:membrane',
                    '-read_only_ATOM_entries', 'true',
                    '-ProQ:normalize', str(nres),
                    '-ProQ:output_local_prediction'])
def main():
    '''Main entry point'''
    args = get_parser(sys.argv[1:])
    ########### Variables ###############
    # Output files/directories
    tmpldir = str(args.tmpldir)
    proqm_script = str(args.proqm_script)
    alignment_pir = str(args.alignment_pir)
    if args.fasta_template != None:
        fasta_template = str(args.fasta_template)
    else:
        fasta_template = ""
    if args.fasta_mdl != None:
        fasta_mdl = str(args.fasta_mdl)
    else:
        fasta_mdl = ""
    rosetta_score_app=str(args.rosetta_score_app)
    rosetta_db=str(args.rosetta_db)
    ####################################################

    outdir = os.getcwd()

    #get proqm profile for the template
    template_name=rootnm_from_pir("structure",alignment_pir)
    tempstr = str(template_name) + '.pdb'
    shutil.copy(tmpldir + '/' + str(template_name) + '.pdb',outdir)
    get_profile(proqm_script,tempstr,fasta_template)

    #get proqm profile for the model
    mdls_rootnm=rootnm_from_pir("sequence",alignment_pir)
    mdls_pdblist = get_listoffiles(outdir,mdls_rootnm)
    one_mdl=mdls_pdblist[0]
    get_profile(proqm_script,one_mdl,fasta_mdl)

    #compute proqm score for the template
    ntemp=num_res(str(tempstr)+'.span')
    compute_proqm(rosetta_score_app,rosetta_db,tempstr,tempstr,ntemp)

    #iterate computation of proqm score for all models
    nmdl=num_res(str(one_mdl)+'.span')
    [print_clean_pdb(mod_i) for mod_i in mdls_pdblist]
    [compute_proqm(rosetta_score_app,rosetta_db,one_mdl,str(mod_i) + 'cl',nmdl) for mod_i in mdls_pdblist]

   
#compare the profiles with the alignment


if __name__ == '__main__':
    main()
