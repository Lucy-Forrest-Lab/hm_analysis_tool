# hm_analysis_tool #

## Introduction ##
A set of python scripts to analyze homology models computed with MODELLER

**get\_molpdf\.py** \- Extracts the MODELLER MOLPDF score from a set of PDB files and print it to a text file\. For usage type: `get_molpdf.py -h`\
**check\_molpdf\_conv\.py** \- From the file generated by get\_molpdf\.py generates plots of score per model (sorted by model number and by score) and of the running RMSD of the score\. For usage type: `check_molpdf_conv.py -h`\
**extract\_str\.py** \- Copy all the PDB files with a MOLPDF score less than a threshold or a percentage of the lowest MOLPDF scored structures\. For usage type:`extract_str.py -h`\
**compute\_proqm\.py** \-Compute PROQM score for the template and a group of models\. For usage type:`compute_proqm.py -h`

## Installation ##
Clone the repo and install it.\
`git clone https://github.com/Lucy-Forrest-Lab/hm_analysis_tool.git`\
`pip install -e .`

## Example ##
*  **Extract MOLPDF score of the models\.** Search for the MOLPDF score printed in each PDB in the directory `model2/` and starting with the rootname `glyt1.B` and it will write the result to the `mdls_molpdf.out` file in the working directory.

   `get_molpdf -pdbdir model2/ -rootname glyt1.B -o mdls_molpdf.out`

*  **Plot convergence plot of MOLPDF score\.** Read the list of MOLPDF scores in the `mdls_molpdf.out` file and it will plot the list of MOLPDF score, the ordered MOLPDF score and the RMS value of MOLPDF score (with the default 200 models window)\. The three plots will be printed in `mdls_convergence.pdf` file and the window RMS of the MOLPDF score will be printed in the `mdls_conv.out` file.

   `check_molpdf_conv -scorefile mdls_molpdf.out -outrms mdls_conv.out -ofig mdls_convergence.pdf`

*  **Select a group of models based on their MOLPDF score\.** Read the MOLPDF score from the `mdls_molpdf.out` file and copy all the structures with a score below 2400 to the `analysis` folder.

   `extract_str -scorefile mdls_molpdf.out -threshold 2400 -outdir analysis`

*  **Compute the PROQM score for the template and the selected models\.** The name of the template PDB file (located in `model2` folder) will be inferred from the `model2/glyt1_on_4xp4_noloop.pir` alignment file\. The command has to be run in the folder where the model PDB files are located.

   `compute_proqm -tmpldir model2/ -alignment model2/glyt1_on_4xp4_noloop.pir`

## Future features ##
*  Analyze a subgroup of structures by:
	- ProQ/ProQM scores - Done, need add functionality to plot ProQM score per residue of the target and template together
	- Molprobilty quality check
	- PROCHECK quality check

