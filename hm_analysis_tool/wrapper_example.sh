python get_molpdf.py -pdbdir ../../test-case/glyt1 -rootname glyt1.B9 -o ../../test-case/analysis/molpdf-score.txt
  
python check_molpdf_conv.py -scorefile ../../test-case/analysis/molpdf-score.txt -outrms ../../test-case/analysis/rmsd-molpdf-score.txt -outsort ../../test-case/analysis/sorted-molpdf-score.txt -ofig ../../test-case/analysis/score-conv.pdf
