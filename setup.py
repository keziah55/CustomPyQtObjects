#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(name='CustomPyQtObjects',
      version='0.1',
      description='A repo of convenience classes for PyQt objects.',
      author='Keziah Milligan',
      packages = find_packages(),
      install_requires = ["PyQt5"]
     )