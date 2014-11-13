# -*- coding: utf-8 -*-

import sys, string, os


# Local variables...

script = 'pyuic4 -o'
uiFile = ' main_window.ui'
pyFile = ' gui_code2.py'

script = script + pyFile + uiFile

print script

os.system(script)

