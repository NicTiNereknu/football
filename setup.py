# -*- coding: utf-8 -*-

# A simple setup script to create an executable using Tkinter. This also
# demonstrates the method for creating a Windows executable that does not have
# an associated console.
#
# SimpleTkApp.py is a very simple type of Tkinter application
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the application

import sys
import os
from cx_Freeze import setup, Executable

base = None
if sys.platform == 'win32':
	base = 'Win32GUI'

includeFiles = ['BorderTypeCombination.csv', 'FieldPointsType.csv', 'FieldPointsTypeCombination.csv',
				'mySave.pkl', 'arrow-up-double-2.gif', 'arrow-down-double-2.gif']

build_exe_options = {
	'include_files': includeFiles
	}

executables = [
	Executable(targetName='football.exe',
			script='main.py',
			base=base,
			icon='icon.ico')
]

os.environ['TCL_LIBRARY'] = r'tcl86t.dll'
os.environ['TK_LIBRARY'] = r'tk86t.dll'


setup(name='simple_Tkinter',
	  version='0.1',
	  description='Sample cx_Freeze Tkinter script',
	  options = {'build_exe': build_exe_options},
	  executables=executables
	  )
