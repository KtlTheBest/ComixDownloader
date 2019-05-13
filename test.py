# -*- coding: utf-8 -*

class someClass:
	def __init__(self):
		self.some_val = 5

	def copy_val(self, other_class):
		self.some_val = other_class

	def __str__(self):
		return "The value is " + str(self.some_val)

if __name__ == "__main__":
	cl = someClass()
	cl.some_val = 6
	he = someClass()
	he.copy_val(cl)
	print(he)
