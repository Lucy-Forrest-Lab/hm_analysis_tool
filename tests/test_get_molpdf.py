from hm_analysis_tool import get_molpdf
import pytest
import os
import pandas as pd

#clean analysis folder
if os.path.exists('test-case/analysis/test-scorefile.txt'):
    os.remove('test-case/analysis/test-scorefile.txt')

def test_parser_required():
    '''Test if parser reads correctly required options'''
    args = get_molpdf.get_parser(['-pdbdir', 'test-case/glyt1', '-rootname', 'glyt1.B9'])
    assert args.pdbdir == 'test-case/glyt1'
    assert args.rootnm == 'glyt1.B9'

def test_parser_default():
    '''Test if parser reads correctly default options if not indicated'''
    args = get_molpdf.get_parser(['-pdbdir', 'test-case/glyt1', '-rootname', 'glyt1.B9'])
    assert args.pattern == 'MODELLER OBJECTIVE FUNCTION'
    assert args.scorefile == 'molpdf.txt'
    assert args.col == '5'

def test_parser_default_specified():
    '''Test if parser reads correctly default options if indicated'''
    args = get_molpdf.get_parser(['-pdbdir', 'test-case/glyt1', '-rootname', 'glyt1.B9', '-o', 'scorefile.txt', '-col', '10'])
    assert args.pattern == 'MODELLER OBJECTIVE FUNCTION'
    assert args.scorefile == 'scorefile.txt'
    assert args.col == '10'

@pytest.mark.parametrize('listfiles,pattern,col', [(['test-case/glyt1/glyt1.B99990001.pdb'], 'MODELLER OBJECTIVE',5)])

def test_get_one_score(listfiles,pattern,col):
    '''Test if getscore routine gets the correct score'''
    match = get_molpdf.getscore(listfiles,pattern,col)
    check = pd.DataFrame({'col1':['test-case/glyt1/glyt1.B99990001.pdb'],
                      'col2':['2386.0759']})
    assert match.equals(check) 

@pytest.mark.parametrize('listfiles,pattern,col', [(['test-case/glyt1/glyt1.B99990001.pdb', 'test-case/glyt1/glyt1.B99990002.pdb'], 'MODELLER OBJECTIVE',5)])
def test_get_list_score(listfiles,pattern,col):
    '''Test if getscore routine gets the correct score'''
    match = get_molpdf.getscore(listfiles,pattern,col)
    check = pd.DataFrame({'col1':['test-case/glyt1/glyt1.B99990001.pdb','test-case/glyt1/glyt1.B99990002.pdb'],
                      'col2':['2386.0759','2607.5806']})
    assert match.equals(check)


