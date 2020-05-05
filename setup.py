from distutils.core import setup


setup(name='jupyter_utils',
      version='0.1',
      packages=['jupyter_utils'],
      scripts=['bin/kernel-create'],
      url='https://github.com/eth-cscs/jupyter-utils',
      license='LICENSE.txt',
      description='Utilities for working jupyterlab at CSCS',
      long_description=open('README.md').read(),
      install_requires=[],
      )
