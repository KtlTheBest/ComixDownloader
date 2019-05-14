# -*- coding: utf-8 -*

import requests
from urlparse import urlparse
import pickle
import os

import config
from error import UnknownUrlType, IncorrectUrlType
from system import removeFolderIfExists

def getHostFromUrl(url):
	return urlparse(url).netloc.split(".")[0]

class Comic:
	def __init__(self, url, baseConfig):
		self.url = url
		
		self.urlType = self.getUrlType()
		if self.urlType == "unknown":
			raise UnknownUrlType
			
		host = getHostFromUrl(self.url)        
			
		self.comicHelper = config.ComicHelper(host)
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
		name_pat = re.compile(self.comicHelper.mangaNamePatRE)
		return name_pat.search(self.text).group(1)
	
	def getPageCount(self):
		pageOptionPat = re.compile(self.comicHelper.optionPatRE)
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
	
	def getImageUrls(self):
		if self.urlType != "chapter":
			raise IncorrectUrlType
	
		url = self.url
		imageUrls = [url]
	
		imageUrlRE = re.compile(self.comicHelper.imageUrlPageReplacePatRE)
		for i in xrange(2, self.pages + 1):
			imageUrls.append(
				imageUrlRE.sub(imageUrlPageReplacePlaceholder % i, url)
				)
	
		return imageUrls
	
	def downloadPage(self, url, page_num):
		# TO-DO: TEST
	
		try:
			pageText = requests.get(url).text
			imageUrl = re.compile(self.comicHelper.imageUrlPatRE).search(pageText)
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
		imageUrls = self.getImageUrls()
		for i, url in enumerate(imageUrls):
			try:        
				print('[==>] Downloading %d out of %d' % (i+1, self.pages))
				self.downloadPage(url, i+1)
			except:                
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
		filenameList = self.getFilenameList()
		for name in filenameList:
			try:
				cbz.write(name)
			except:
				return
		cbz.close()
		removeFolderIfExists(self.baseConfig + os.sep + self.name)
	
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

	def downloadChapters(self, listOfChapters):
		for url in listOfChapters:
			self.downloadChapter(url)
	
	def printChaptersAndChooseWhichToDownload(self):
		self.getChaptersList()
		for num, item in enumerate(self.ChapterUrls):
			print(str(num + 1) + item)

		buff = input("Download all (Y) or chapter number: ").rstrip()
		if buff.lower()[0] == "y" or buff.lower() == "yes":
			urlsOfChaptersToDownload = self.ChapterUrls
		else:
			buff = int(buff) # User input here. Should serialize more
			urlsOfChaptersToDownload = [self.ChapterUrls[buff - 1]]

		self.downloadChapters(urlsOfChaptersToDownload)
	
	def download(self):
		if self.urlType == "main":
			self.printChaptersAndChooseWhichToDownload()
		if self.urlType == "chapter":
			self.downloadChapter(self.url)
		if self.urlType == "page":
			self.downloadPage(self.url)

