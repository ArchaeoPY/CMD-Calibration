# -*- coding: utf-8 -*-
"""
IH  
"""

from distutils.core import setup
import py2exe, sys, os

sys.argv.append('py2exe')

setup(
    options = {'py2exe': {'bundle_files': 3, "includes" : ["sip","numpy"]}},
    windows = [{'script': "GUI.py"}],         
    zipfile = r"lib\sharedlib",
)