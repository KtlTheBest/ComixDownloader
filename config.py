# -*- coding: utf-8 -*

import pickle
from os import sep
from error import UnknownComicSource

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Content-Type": "application/x-www-form-urlencoded"
}

class BaseConfig:
	def __init__(self, *args, **kwargs):
		self.downloadFolder = "Comics"
		self.downloadType = "folder"
		self.configFolder = "support"
		self.configName = "config.pickle"
		
		self.filename = self.configFolder + sep + self.configName
		
		if self.doesHaveConfigFile() == False:
			self.createConfig()
		else:
			with open(self.filename) as f:
				config_dict = pickle.load(f)
			self.__dict__.update(config_dict)
				
	def doesHaveConfigFile(self):
		try:
			open(self.filename)
			return True
		except IOError:
			return False
	
	def saveConfig(self):
		configFile = open(self.filename, "wb")
		pickle.dump(self.__dict__, configFile)
		configFile.close()

	def createConfig(self):
		try:
			os.rm(self.filename)
		except:
			pass
		self.saveConfig()

class ComicHelper:
	def __init__(self):
		"""
		This class contains all the necessary REs that might be used
		when downloading the comics
		"""
		
		# Note: this is just a prototype, how the __init__
		# should look like
		self.mangaUrlPatRE = r'' 
		self.imageUrlPatRE = r''
		self.imageUrlPageReplacePatRE = r''
		self.mangaNamePatRE = r''
		self.optionPatRE = r''
		self.chapterPatRE = r''
		self.chapterGroupNum = 0
		self.chapterPrependUrl = 0
		pass
	
	def loadFromFile(self, filename):
		"""
		This method accepts the filename as it's argument
		and calls pickle.load() on it.
		It should do some error handling
		"""
		try:
			configFile = open("filename")
			self = pickle.load(configFile)
			configFile.close()
		except:
			raise UnknownComicSource
	
	def pickleToFile(self):
		"""
		This method is used to create pickle files.
		It is not intended to be called inside main.py or
		comic_class.py
		"""
		pass
