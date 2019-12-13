from hm_analysis_tool import check_molpdf_conv
import pytest

def test_parser_not_default():
    '''Test if parser reads if all not default options are passed'''
    args = check_molpdf_conv.get_parser(['-scorefile', 'test-case/analysis/molpdf-score.txt', '-outrms', 'test-case/analysis/rmsd-molpdf-score.txt', '-ofig', 'test-case/analysis/score-conv.pdf'])
    assert args.scorefile == 'test-case/analysis/molpdf-score.txt'
    assert args.outrms == 'test-case/analysis/rmsd-molpdf-score.txt'
    assert args.ofig == 'test-case/analysis/score-conv.pdf'

def test_parser_allopt():
    '''Test if parser reads if all not default options are passed'''
    args = check_molpdf_conv.get_parser(['-scorefile', 'test-case/analysis/molpdf-score.txt', '-outrms', 'test-case/analysis/rmsd-molpdf-score.txt', '-ofig', 'test-case/analysis/score-conv.pdf', '-win', '200', '-scorecol', '1'])
    assert args.scorefile == 'test-case/analysis/molpdf-score.txt'
    assert args.outrms == 'test-case/analysis/rmsd-molpdf-score.txt'
    assert args.ofig == 'test-case/analysis/score-conv.pdf'
    assert args.win == '200'
    assert args.scorecol == '1'
