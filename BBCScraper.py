import requests
import os
from article import Article
from bs4 import BeautifulSoup as bs

class BBCScraper:
	def __init__(self):
		self.website = "BBC"
		self.base_url = "https://www.bbc.com"

	def scrape_news(self):
		url = self.base_url+"/news"
		page = requests.get(url)
		soup = bs(page.content, 'html.parser')
		headings = soup.find_all('a', class_="gs-c-promo-heading")
		stories = []
		for item in headings:
			link = self.make_url(item['href'])
			"""
			Some of the entries on BBC are either not news or video/audio/live coverage and therefore do not interest us
			"""
			if (not "/live/" in link) and (not "/play/" in link) and (not "/earth/" in link) and (not "/travel/" in link) and (not "/video/" in link) and (not "/programmes/" in link):  
				print(link)
				story = self.scrape_article(link)
				stories.append(story)
		return stories

	def scrape_article(self, url):
		try:
			artcl = requests.get(url)
			if "/av/" in artcl.url:
				return Article(self.website, "","",True,"Video entry, did not scrape the article {0}".format(url))
		except:
			return Article(self.website, "","",True,"Couldn't access the url {0}, please check if it is correct".format(url))
		try:
			soup = bs(artcl.content, 'html.parser')
			title = ""
			text = []
			if soup.find(class_="story-body__h1") != None:			
				title = soup.find(class_="story-body__h1").text
				body = soup.find(property="articleBody")
				text = [p.text for p in body.find_all("p")]
			elif soup.find(id="main-heading") != None:
				title = soup.find(id="main-heading").text
				body = soup.find("article")
				text = [p.text for p in body.find_all(attrs={"data-component": "text-block"})]
			elif soup.find(class_="qa-story-headline") != None:
				title = soup.find(class_="qa-story-headline").text
				body = soup.find(class_="qa-story-body")
				text = [p.text for p in body.find_all("p")]
			else:
				title = soup.find(class_="article-headline__text").text
				#print(title)
				body = soup.find(class_="article__body-content")
				if body.find(class_="article__intro"):
					intro = body.find(class_="article__intro").text
					text.append(intro)
				first_letter = ""
				if body.find(class_="drop-capped"):
					first_letter = body.find(class_="drop-capped").text
				text_cards = body.find_all(class_="body-text-card__text")
				for card in text_cards:
					paragraphs = card.find_all("p")
					for p in paragraphs:
						if first_letter != "":
							text.append(first_letter+p.text)
							first_letter = ""
						else:
							text.append(p.text)

			#print(title)
			article_text = ""
			for line in text:
				article_text += line
				article_text += "\n"
			#print(article_text)
			return Article(self.website, article_text, title, False, "")
		except: 
			return Article(self.website, "","",True,"Couldn't scrape the article {0}".format(url))

	def make_url(self, url):
		if "http" in url:
			return url
		return self.base_url+url