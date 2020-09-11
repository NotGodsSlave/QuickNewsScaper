import requests
import os
from article import Article
from bs4 import BeautifulSoup as bs

class TheGuardianScraper:
	def __init__(self):
		self.website = "TheGuardian"
		self.base_url = "https://www.theguardian.com/"

	def scrape_news(self):
		url = self.base_url+'/international'
		page = requests.get(url)
		soup = bs(page.content, 'html.parser')
		headings = soup.find_all('a', class_="js-headline-text")
		stories = []
		for item in headings:
			if item != None:
				link = self.make_url(item['href'])
				"""
				Excluding live coverage, audio and photo galleries links
				"""
				if (not "/live/" in link) and (not "/gallery/" in link) and (not "/audio/" in link):  
					print(link)
					story = self.scrape_article(link)
					stories.append(story)

		return stories

	def scrape_article(self, url):
		try:
			artcl = requests.get(url)
		except:
			return Article(self.website, "","",True,"Couldn't access the url {0}, please check if it is correct".format(url))
		try:
			soup = bs(artcl.content, 'html.parser')
			title = ""
			text = []
			
			if soup.find(class_="content__headline") != None:		
				title = soup.find(class_="content__headline").text
				body = soup.find(class_="content__article-body")
				text = [p.text for p in body.find_all("p")]
			elif soup.find(class_="article-body-commercial-selector") != None:
				title = soup.find('h1').text
				body = soup.find(class_="article-body-commercial-selector")
				text = [p.text for p in body.find_all("p")]

			#print(title)
			article_text = ""
			for line in text:
				article_text += line
				if len(line) > 1:
					article_text += "\n"
			#print(article_text)
			return Article(self.website, article_text, title, False, "")
		except: 
			return Article(self.website, "","",True,"Couldn't scrape the article {0}".format(url))

	def make_url(self, url):
		if "http" in url:
			return url
		return self.base_url+url