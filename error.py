# -*- coding: utf-8 -*

class Error(Exception):
	pass

class UnknownUrlType(Error):
	"""
	Raised when getUrlType can't define the type of comics URL
	"""
	pass

class UnknownComicSource(Error):
	"""
	Raised when program can't find the comic source in it's support
	folder
	"""
	pass

class IncorrectUrlType(Error):
	"""
	Raised when the expected type of url doesn't match the method
	invariant
	"""
	pass
