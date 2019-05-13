# -*- coding: utf-8 -*

import requests
from urlparse import urlparse
import pickle
import os

import config
from error import UnknownUrlType

def getHostFromUrl(url):
    return urlparse(url).netloc.split(".")[0]

class Comic:
    def __init__(self, url, baseConfig):
        self.url = url
        
        self.urlType = self.getUrlType()
        if self.urlType == "unknown":
			raise UnknownUrlType
			
        #host = getHostFromUrl(self.url)        
            
        self.comicHelper = config.ComicHelper()
		self.baseConfig = baseConfig
        
        self.text = self.getPageCode()        
        self.name = self.getComicName()
        self.pages = self.getPageCount()
        self.downloadFolder = home + os.sep + self.name
        self.chapterUrls = []
        self.createFolderIfMissing()
    
    def getPageCode(self):
        return requests.get(self.url).text
    
    def getComicName(self):
        name_pat = re.compile(self.mangaNamePatRE)
        return name_pat.search(self.text).group(1)

    def getPageCount(self):
        pageOptionPat = re.compile(self.optionPatRE)
        return len(pageOptionPat.findall(self.text))

	def getZerosInFilename(self):
	    cnt = 0
	    tmp = self.pages
	    while tmp != 0:
	        tmp /= 10
	        cnt += 1
	    return cnt - 1

	def getFilenameList(self):
		lst = []
		target = 10
		zeros = self.getZerosInFilename()
		for i in xrange(1, self.pages + 1):
			if i == target:
				target *= 10
				zeros -= 1
			lst.append(baseConfig.downloadFolder + \
						os.sep + \
						self.name + \
						os.sep + \
						"0" * zeros + str(i) + ".jpg")
		return lst

	def downloadPage(self, url, page_num):
		# TO-DO: TEST

		try:
			pageText = requests.get(url).text
			imageUrl = re.compile(self.imageUrlPatRE).search(pageText)
			imageDataPool = requests.get(imageUrl)
			filename = config.BaseConfig.downloadFolder + \
						os.sep + \
						self.name + \
						os.sep + \
						page_num

			with open(filename, "wb") as f:
				for chunk in imageDataPool.iter_content(size=256):
					f.write(chunk)
		except:
			print("[x] Check your connection to internet!")

    def downloadPages(self):
        self.baseConfig.downloadCount += 1
        for i in xrange(1, self.pages + 1):
            try:        
                print('[==>] Downloading %d out of %d' % (i, self.pages))
                # write code that gets image url
					# <--
				# Yeah, do it :)
                self.downloadPage(imageUrl, i+1)
            except Exception, e:                
                print('[x] There is a mistake in a URL')
                return

	def getUrlType(self):
		url = self.url
		if url == re.compile(self.mainUrlPatRE).match(url).group(0):
			return "main"
		elif url == re.compile(self.chapterUrlPatRE).match(url).group(0):
			return "chapter"
		elif url == re.compile(self.pageUrlPatRE).match(url).group(0):
			return "page"
		else:
			return "unknown"

    def createCBZ(self, url):
        self.downloadPages(url)
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
    
    def downloadChapter(self, url):
        if comicType == "folder":
            self.downloadPages(url)
        else:
            self.createCBZ(url)

	def getChaptersList(self):
		main_page = requests.get(self.url).text
		with self.chapterPatRE.finditer(main_page) as matches:
			toPrepend = ""
			if self.chapterPrependUrl == 1:
				toPrepend = self.url
			for item in matches:
				self.chapterUrls.append(toPrepend + item.group(1))
	
	def printChaptersAndChooseWhichToDownload(self):
		self.getChaptersList()
		for num, item in enumerate(self.ChapterUrl):
			print(str(num + 1) + item)
	
	def download(self):
		if self.urlType == "main":
			self.printChaptersAndChooseWhichToDownload()
		if self.urlType == "chapter":
			self.downloadChapter()
		if self.urlType == "page":
			self.downloadPage(self.url)

