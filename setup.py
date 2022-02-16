#!/usr/bin/env python3

from setuptools import setup, find_packages

import re
VERSIONFILE="customQObjects/_version.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))
    

setup(name='CustomPyQtObjects',
      version=verstr,
      description='A repo of convenience classes for PyQt/PySide objects.',
      author='Keziah Milligan',
      packages = find_packages(),
      install_requires = ["QtPy"]
     )