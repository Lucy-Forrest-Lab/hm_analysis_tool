from setuptools import setup

setup(name='hm_analysis_tool',
      packages=['hm_analysis_tool'],
      entry_points={
          'console_scripts': [
              'get_molpdf = hm_analysis_tool.get_molpdf:main',
              'check_molpdf_conv = hm_analysis_tool.check_molpdf_conv:main',
              'extract_str = hm_analysis_tool.extract_str:main',
              'compute_proqm = hm_analysis_tool.compute_proqm:main' 
          ]
      },
      )

