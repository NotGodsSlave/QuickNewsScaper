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


	def make_filename(self, extension="txt"):
		return "./articles/{0}-{1}.{2}".format(self.website,self.title.replace(" ","-").replace('/','-'),extension)

	def make_dict(self):
		return {"website": self.website,
				"title": self.title,
				"text": self.text
		}

	def print_to_file(self):
		if self.iserror:
			print(self.error_message)
		else:
			try:
				if not os.path.isdir("./articles"):
					os.mkdir("./articles")
				resfile = open(self.make_filename(), 'w')
				print(self.title+"\n\n", file = resfile)
				print(self.text, file = resfile)
			except OSError:
				print ("Couldn't create a file")

	def make_json(self, filename=None):
		if not self.iserror:
			jsn = json.dumps({"website": self.website, "title": self.title, "text": self.text}, ensure_ascii=False)
			if filename != None:
				with open(filename, 'w') as file:
					json.dump({"website": self.website, "title": self.title, "text": self.text}, file)
			return jsn