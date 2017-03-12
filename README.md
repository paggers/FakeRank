#FakeRank: 
Fake news exposed


March 2nd, 2017
Hrishi Dharam, Eilam Levitov




Abstract
The current state of communication, specifically media and social network, provides an inherent vulnerability to a rapidly growing problem colloquially known as “fake news”. This vulnerability preys on the accessibility of trending articles which consist of few to none credible sources or actual fact checking, to the point of malicious fabrication of facts. In this project we construct a system which uses the PageRank algorithm to establish a measure of fakeness for a given article. 


Introduction 
        In order to generate a measure of fakeness, we construct a fully connected markov chain where the transition probabilities correspond to the similarity between articles. After quantizing the similarity and normalizing, we can use the PageRank algorithm in order to rank the similarity between all articles. Our model is constructed under the assumption that a keyword search will generate reputable related articles, and a fake news article to be more dissimilar to these then the reputable articles are to each other.  Thus, we expect that if the article is indeed fake it will rank relatively low.


Algorithm Overview:
1. Extract keywords from article in question and take the top fixed n recommended articles from a search of the keywords
2. Generate a vector representation of the n+1 articles (the specific representation is not finalized, one representation could be a bag-of-words where the corpus is the union of all the articles)
3. Generate a complete graph with n+1 nodes where each node is an article with the corresponding vector representation. The edges of the graph will be a measure of similarity between articles. Again, the method by which to determine similarity is not finalized but we could for example, use cosine similarity. 
4. Normalize the edges. Specifically, since we want a markov chain, divide each edge weight by the highest “node weight” where the node weight is the sum of the edge weights connected to a node. Add self-loops to each node such that the node weight is equal to 1 and is a distribution. 
5. Now that we have a markov chain that represents the similarity between articles PageRank will give us a ranking of the articles that are most similar to other articles. If the article in question is sufficiently low on this list, we can classify it as fake news.