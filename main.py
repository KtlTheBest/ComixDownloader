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

home = ""
comicType = ""
downloadCount = 0

comicsIniFilePath = "support" + os.sep + "Comics.ini"
linksIniFilePath  = "support" + os.sep + "links.ini"

parser = ConfigParser.RawConfigParser(allow_no_value=True)

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Content-Type": "application/x-www-form-urlencoded"
}

class Comic:
    def __init__(self, url):
        self.url = url
        self.text = self.getPageCode()        
        self.name = self.getComicName()
        self.pages = self.getPageCount()
        self.mangaUrlPatRE = ""        
        self.imageUrlPatRE = ""
        self.mangaNamePatRE = ""
        self.optionPatRE = ""
        self.downloadFolder = home + os.sep + self.name
    
    def getPageCode(self):
        return requests.get(self.url + '1', headers=headers).text
    
    def getComicName(self):
        name_pat = re.compile(self.mangaNamePatRE)
        return name_pat.search(self.text).group(1)

    def getPageCount(self):
        pageOptionPat = re.compile(self.optionPatRE)
        return len(pageOptionPat.findall(self.text))

    def updateRegex(self, host):
        self.mangaUrlPatRE = parser.get(host, "mangaUrlPat")        
        self.imageUrlPatRE = parser.get(host, "imageUrlPat")
        self.mangaNamePatRE = parser.get(host, "mangaNamePat")
        self.optionPatRE = parser.get(host, "optionPat")

    def downloadPages(self):
        global downloadCount
        createDir(home)
        deleteDir(self.downloadFolder)
        createDir(self.downloadFolder)
        
        imageUrlPat = re.compile(self.imageUrlPatRE)
        numLen = getNumLen(self.pages) - 1
        target = 10    
        for i in xrange(1, self.pages + 1):
            if i == target:
                target *= 10
                numLen -= 1
            filename = 'Comics' + os.sep + self.name + os.sep + "0" * numLen + str(i) + '.jpg'
            try:        
                print('[==>] Downloading %d out of %d' % (i, self.pages))
                comicPage = requests.get(self.url + str(i), headers=headers).text
                #print(comicPage)                                
                imageUrl = imageUrlPat.search(comicPage).group(1)
                imageUrl = cleanUrl(imageUrl) + str(i) + '.jpg'
#                print("[D] " + imageUrl)                          
                imagePage = requests.get(imageUrl, headers=headers, stream=True)
                comicPageFile = open(filename, "wb")            
                for chunk in imagePage.iter_content(chunk_size=256):
                    if chunk:
                        comicPageFile.write(chunk)
                comicPageFile.close()
            except Exception, e:                
                print('[x] There is a mistake in a URL')
                return
        print("[o] Done!")
        downloadCount += 1

    def createCBZ(self):
        self.downloadPages()
        cbz = zipfile.ZipFile(self.downloadFolder + ".cbz", mode="w")        
        numLen = getNumLen(self.pages) - 1
        target = 10
        for i in xrange(1, self.pages + 1):
            if i == target:
                target *= 10
                numLen -= 1            
            try:
                cbz.write(self.downloadFolder + os.sep + "0" * numLen + str(i) + ".jpg")
            except:
                return
        cbz.close()
        rmtree(home + os.sep + self.name, ignore_errors=True)
    
    def download(self):
        if comicType == "folder":
            newComic.downloadPages()
        else:
            newComic.createCBZ()

def createDir(name):
    try:
        os.mkdir(name)
    except:
        pass

def deleteDir(name):
    rmtree(name, ignore_errors=True)

def getHostFromUrl(url):
    return urlparse(url).netloc.split(":")[0]

def readConfig(conf):
    global parser
    sample_config = conf.read()
    conf.close()
    parser.readfp(io.BytesIO(sample_config))

def init():
    
    global home
    global downloadCount
    global comicType 
    
    print("\tComics downloader by marik")
    print("\tP.S. To get help, enter :h")    
    print

    try:
        ini = open(comicsIniFilePath)
    except:
        try:
            os.mkdir("support")
        except:
            pass
        ini = open(comicsIniFilePath, "w")
        ini.write("[base]\n")        
        ini.write("type=folder\n")
        ini.write("count=0\n")
        ini.write("home=Comics")
        ini.close()
        ini = open(comicsIniFilePath)
    
    readConfig(ini)
    ini.close()
    
    home = parser.get('base', 'home')
#    print("[D] home={}".format(home))
    comicType = parser.get('base', 'type')
#    print("[D] type={}".format(comicType))    
    downloadCount = int(parser.get('base', 'count'))
#    print("[D] count={}".format(downloadCount))
    ini = open(linksIniFilePath)    
    readConfig(ini)
    
def updateConfig():    
    configFile = open(comicsIniFilePath, "w")
    configFile.write("[base]\n")
    configFile.write("type={}\n".format(comicType))
    configFile.write("count={}\n".format(str(downloadCount)))
    configFile.write("home={}\n".format(home))
    configFile.close()

def user_input():
    global comicType
    if comicType == "folder":
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

def getNumLen(x):
    cnt = 0
    while x != 0:
        x /= 10
        cnt += 1
    return cnt    
    
def resolveInput(buff):
    global comicType
    try:        
        command = re.compile(r'^:(.+?)$').match(buff).group(1)
        if command == 'fld':
            comicType = "folder"
        elif command == 'cbz':
            comicType = "cbz"
        else:
            print("[x] Unknown command!")
    except:
        buff = buff.replace(' ', '')
        if buff == "":
            return
        comicUrl = cleanUrl(buff)

        host = getHostFromUrl(comicUrl)
        
        if not comicUrl:
            return
        if "gallery" in comicUrl:
            tmp = comicUrl.split("allery")
            comicUrl = tmp[0] + tmp[1]
        newComic = Comic(comicUrl)
        newComic.updateRegex(host)
        newComic.download()        
        del(newComic)
    
def main():
    init()
    while True:
        buff = user_input()
        if re.compile(r'^:x').match(buff):
            updateConfig()            
            return
        elif re.compile(r'^:h\w*?$').match(buff):
            printHelp()
        else:
            resolveInput(buff)
        
if __name__ == "__main__":
    main()