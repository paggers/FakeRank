from __future__ import division
import numpy as np
from matplotlib import pyplot as plt
import math
from bs4 import BeautifulSoup
from google import search
from sklearn.feature_extraction.text import TfidfVectorizer
import urlparse
import urllib,urllib2
import json
# import NetworkX
import time
import util

def gSearch(str):
    start = time.time()
    # 1) Look keywords on google, stop = number of pages
    print "Retrieving pages..."
    pages = []
    for url in search(str, stop=50):
        print url
        pages.append(url)
    print "Pages retrieved"
    end = time.time()
    print(end - start)
    return pages

def simMatrix(pages):
    # 2) Generate similarity vectors using SimRank
    start = time.time()
    print "Generating similarity vectors..."
    vect = TfidfVectorizer(min_df=1)
    class MyOpener(urllib.FancyURLopener):
       version = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15'
    myopener = MyOpener()
    textList = []
    for i in xrange(len(pages)):
        try:
            page = myopener.open(pages[i])  
            text = page.read()
            # text = text.decode('unicode_escape').encode('ascii','ignore')
            # text = "".join(text)
            myopener.close()
            page.close()        # Doulbe check
            soupI = BeautifulSoup(text, 'lxml')
            textI = soupI.get_text()
            textList.append(textI)
        except:
            print str(i) + "th parse was unsuccessful :("
    # 3) Create similarity matrix 
    tfidf = vect.fit_transform(textList)
    transition_matrix = (tfidf * tfidf.T).A
    transition_matrix = filterNaN(transition_matrix)
    transition_matrix = adjacent(transition_matrix)
    transition_matrix = noZeros(transition_matrix)
    # row_sums = transition_matrix.sum(axis=1)
    # mtx = transition_matrix / row_sums[:, np.newaxis]   # normalizing
    end = time.time()
    print "Similarity Matrix computed"
    print(end - start)
    return transition_matrix

def filterNaN(mtx):
    badindex = []
    for i in range(len(mtx)):
        if True in np.isnan(mtx[i]):
            badindex.append(i)
    for b in sorted(badindex,reverse=True):
        mtx = np.delete(mtx,(b), axis=0)
        mtx = np.delete(mtx,(b), axis=1)
    return mtx

def noZeros(mtx):
    badindex = []
    for i in range(len(mtx)):
        if sum(mtx[i]) == 0:
            badindex.append(i)
    for b in sorted(badindex,reverse=True):
        mtx = np.delete(mtx,(b), axis=0)
        mtx = np.delete(mtx,(b), axis=1)
    return mtx

def adjacent(mtx):
    threshold = 0.1
    for i in range(len(mtx)):
        for j in range(len(mtx)):
            if i == j:
                mtx[i][j] = 0
            elif mtx[i][j] < threshold:
                mtx[i][j] = 0
            else:
                mtx[i][j] = 1
    return mtx
