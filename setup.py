import os
from setuptools import setup

requirementPath = './requirements.txt'
if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        dependencies = f.read().splitlines()


setup(name='hm_analysis_tool',
      packages=['hm_analysis_tool'],
      install_requires = dependencies,
      entry_points={
          'console_scripts': [
              'get_molpdf = hm_analysis_tool.get_molpdf:main',
              'check_molpdf_conv = hm_analysis_tool.check_molpdf_conv:main',
              'extract_str = hm_analysis_tool.extract_str:main',
              'compute_proqm = hm_analysis_tool.compute_proqm:main'
          ]
      },
      )
