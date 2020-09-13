from article import Article
from TheGuardianScraper import TheGuardianScraper
from BBCScraper import BBCScraper
import json
import sys

websites = []

if len(sys.argv) == 1:
	websites = ["BBC", "TheGuardian"]

elif sys.argv[1] == "help":
	print("Run this script to scrape articles from the available websites. Currently TheGuardian and BBC are available.\nIf you want to scrape only some of these websites, specify them as a command line argument.\nBy default articles are outputed as json files, if you want to output them in command line, please use \"cmdoutput\" argument")

elif sys.argv[1] == "cmdoutput":
	websites = ["BBC", "TheGuardian", "cmdoutput"]

else:
	websites = sys.argv[1:]

args = []
for item in websites:
	args.append(item.lower())

bbcscraper = BBCScraper()
guardianscraper = TheGuardianScraper()
jsons = []
bbcstories = []
guardianstories = []
if args:
	if "bbc" in args:
		bbcstories = bbcscraper.scrape_news()
	if "theguardian" in args:
		guardianstories = guardianscraper.scrape_news()

if not "cmdoutput" in args:
	for item in bbcstories:
		jsons.append(item.make_json(item.make_filename("json")))
	for item in guardianstories:
		jsons.append(item.make_json(item.make_filename("json")))
else:
	articles = []
	for item in bbcstories:
		articles.append(item)
	for item in guardianstories:
		articles.append(item)
	json_list = json.dumps([item.make_dict() for item in articles], ensure_ascii=False).encode('utf-8')

print(json_list.decode())
#print(jsons)
#print("Scraped {0} articles".format(len(jsons)))