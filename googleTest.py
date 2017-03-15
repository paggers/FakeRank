import re
import sys
import urlparse
import random
import string
import numpy as np
import urllib,urllib2
import json
from bs4 import BeautifulSoup
from google import search
from sklearn.feature_extraction.text import TfidfVectorizer

# 1) Insert keywords
userInput = []
Input = raw_input('Search: ')

# 2) Look keywords on google, return n=20 pages
print "Retrieving pages..."
pages = []
for url in search(Input, stop=10):
	pages.append(url)
# 3) Generate similarity vectors using SimRank
print "Generating similarity vectors..."
sim = np.zeros(shape=(10,10))
API_URL="http://www.scurtu.it/apis/documentSimilarity"
def callApi(url,inputObject):
	params = urllib.urlencode(inputDict)    
  	f = urllib2.urlopen(url, params)
  	response= f.read()
  	responseObject=json.loads(response)  
  	return responseObject
inputDict={}

# # 4) Create a normalized fully contected graph
#     try:
#         # open, read, and parse the text using beautiful soup
#         page = myopener.open(url)
#         text = page.read()
#         page.close()
#         soup = BeautifulSoup(text, "html")

#         # find all hyperlinks using beautiful soup
#         for tag in soup.findAll('a', href=True):
#             # concatenate the base url with the path from the hyperlink
#             tmp = urlparse.urljoin(url, tag['href'])
#             # we want to stay in the berkeley EECS domain (more relevant later)...
#             if domain(tmp).endswith('berkeley.edu') and 'eecs' in tmp:
#                 url_list.append(tmp)
#         if len(url_list) == 0:
#             return [url_start]
#         return url_list
#     except:
#         return [url_start]
vect = TfidfVectorizer(min_df=1)
from django.utils.encoding import smart_str, smart_unicode
class MyOpener(urllib.FancyURLopener):
   version = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15'
myopener = MyOpener()
textList = []
for i in xrange(len(pages)):
	page = myopener.open(pages[i])	
	text = page.read()
	text = text.decode('unicode_escape').encode('ascii','ignore')
	text = "".join(text)
	page.close()
	soupI = BeautifulSoup(text, 'lxml')
	textI = soupI.get_text()
	textList.append(textI)
tfidf = vect.fit_transform(textList)
transition_matrix = (tfidf * tfidf.T).A
row_sums = transition_matrix.sum(axis=1)
transition_matrix = transition_matrix / row_sums[:, np.newaxis]
print transition_matrix




# while (True):
# 	Input = input('Enter ' + count + ' keyword (q to stop): ')
# 	if Input == 'q':
# 		break
# 	userInput.append(Input)


# inputDict['doc1']='Text of the first document'
# inputDict['doc2']='Text of the second document'
# finalResponse = callApi(API_URL,inputDict)



# from lxml import html
# import requests

# page = requests.get('http://econpy.pythonanywhere.com/ex/001.html')
# tree = html.fromstring(page.content)



# import re
# import sys
# import urllib
# import urlparse
# import random
# from bs4 import BeautifulSoup
# class MyOpener(urllib.FancyURLopener):
#    version = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15'

# def domain(url):
#     """
#     Parse a url to give you the domain.
#     """
#     # urlparse breaks down the url passed it, and you split the hostname up 
#     # ex: hostname="www.google.com" becomes ['www', 'google', 'com']
#     hostname = urlparse.urlparse(url).hostname.split(".")
#     hostname = ".".join(len(hostname[-2]) < 4 and hostname[-3:] or hostname[-2:])
#     return hostname
    
# def parse_links(url, url_start):
#     """
#     Return all the URLs on a page and return the start URL if there is an error or no URLS.
#     """
#     url_list = []
#     myopener = MyOpener()
#     try:
#         # open, read, and parse the text using beautiful soup
#         page = myopener.open(url)
#         text = page.read()
#         page.close()
#         soup = BeautifulSoup(text, "html")

#         # find all hyperlinks using beautiful soup
#         for tag in soup.findAll('a', href=True):
#             # concatenate the base url with the path from the hyperlink
#             tmp = urlparse.urljoin(url, tag['href'])
#             # we want to stay in the berkeley EECS domain (more relevant later)...
#             if domain(tmp).endswith('berkeley.edu') and 'eecs' in tmp:
#                 url_list.append(tmp)
#         if len(url_list) == 0:
#             return [url_start]
#         return url_list
#     except:
#         return [url_start]