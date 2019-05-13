# -*- coding: utf-8 -*

import os
from shutil import rmtree

def createFolderIfMissing(name):
	if os.access(name) == True:
		return
	os.mkdir(comicFolderName)

def removeFolderIfExists(name):
	if os.access(name) == False:
		return
	rmtree(name)
