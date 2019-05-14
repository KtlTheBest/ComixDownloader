# -*- coding: utf-8 -*-
import requests
import re
import os
import sys
import ConfigParser
import io
import zipfile
from urlparse import urlparse
from shutil import rmtree
import pickle

from comic_class import Comic
from error import UnknownUrlType
import config

baseConfig = config.BaseConfig()

def createDir(name):
    try:
        os.mkdir(name)
    except:
    	print("[x] Couldn't create folder " + name)
        pass

def deleteDir(name):
    rmtree(name, ignore_errors=True)

def getHostFromUrl(url):
    return urlparse(url).netloc.split(".")[0]

def readConfig(conf):
    global parser
    sample_config = conf.read()
    conf.close()
    parser.readfp(io.BytesIO(sample_config))

def init():
    print("\tComics downloader by marik")
    print("\tP.S. To get help, enter ':h'")    
    print
    
def updateConfig():
	baseConfig.saveConfig()

def user_input():
    if baseConfig.downloadType == "folder":
        tp = "fld"
    else:
        tp = "cbz"
    buffer = raw_input(tp + "> ")
    return buffer

def printHelp():
    print("\tHello and welcome to comic downloader :)")
    print
    print("To download a comic, just copy-paste the url of the comic")
    print("There are also some settings that can be ticked")
    print("\tTo exit enter ':x' like in vim")
    print
    print("\tTo choose the downloaded file type, enter :type=[folder,cbz]")
    print("\tThe default is [folder]")

def cleanUrl(url):
    cleanUrlPat = re.compile(r'(http[s]?://)?([a-z0-9./]+)')
    url = "https://" + str(cleanUrlPat.search(url).group(2)) 
    try:    
        page = requests.get(url)
        return url
    except:
        print("[x] Typo in a url")    

def parseOptionCommandOrPrintUnknown(buff):	
	if buff[0] != ":":
		return False
	
	command = buff[1:]
	if command == 'fld':
		baseConfig.downloadType = "folder"
	elif command == 'cbz':
		baseConfig.downloadType = "cbz"
	else:
		print("[x] Unknown command!")    
	return True
    
def resolveInput(buff):
	if parseOptionCommandOrPrintUnknown(buff) == True:
		return
	buff = buff.replace(' ', '')
	if buff == "":
		return
	comicUrl = cleanUrl(buff)
	try:
		newComic = Comic(comicUrl, baseConfig)
		newComic.download()
	except UnknownUrlType:
		print("[x] Unknown manga source!")
    
def main():
	init()
	while True:
		try:
			buff = user_input()
		except KeyboardInterrupt:
			updateConfig()
			return
			
		if re.compile(r'^:x').match(buff):
			updateConfig()            
			return
		elif re.compile(r'^:h\w*?$').match(buff):
			printHelp()
		else:
			resolveInput(buff)
        
if __name__ == "__main__":
    main()
