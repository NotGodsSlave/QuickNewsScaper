import requests
import os
import json
from bs4 import BeautifulSoup as bs

class Article:
	def __init__(self, website: str, text: str, title: str, iserror, error_message):
		self.website = website
		self.text = text
		self.title = title
		self.iserror = iserror
		self.error_message = error_message

	def print_to_file(self):
		if self.iserror:
			print(self.error_message)
		else:
			try:
				if not os.path.isdir("./articles"):
					os.mkdir("./articles")
				resfile = open("./articles/{0}-{1}.txt".format(self.website,self.title.replace(" ","-")), 'w')
				print(self.title+"\n\n", file = resfile)
				print(self.text, file = resfile)
			except OSError:
				print ("Couldn't create a file")

	def make_json(self):
		if not self.iserror:
			file = json.dumps({"website": self.website, "title": self.title, "text": self.text})