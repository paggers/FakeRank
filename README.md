
# FakeRank  


March 17, 2017  
Hrishi Dharam, Eilam Levitov


### Abstract:  
    We began this project with a general goal to rank the ’fakeness’ of news articles. During construction the goal has shifted slightly, but the concept is still similar. Given a search value, our program will return results corresponding to the ’center of mass’ of each Voronoi region, or colloquially the most important result for a given group.


### Introduction:   
    In today’s world there is a massive influx of ’hard to distinguish’ data. The project’s objective is to use Google’s search engine to return the most prominent articles with respect to distinct ’groups’ of articles. Here, instead of finding the most relevant and reputable articles, we construct a graph using the retrieved data and try to find communities within the graph that correspond to similar articles. By finding the centers of these communities, we can generate a list of articles that will summarize different topics related to the query.


### Algorithm Overview:  
1. Enter Search Value  
2. Uses google to retrieve results  
3. Parse text for each result  
4. Generate a graph where edge weights correspond to the similarities (tf-idf) of the documents  
5. Adjust edge weights and apply threshold on similarities in order to transform to adjacency matrix  
6. Normalize the adjacency matrix to be applicable to PageRank Algorithm  
7. Select parameters by simulations and apply the PageRank-ClusteringA [1]  
8. Output the articles corresponding to the centers  




## To read the full report go to [finding-key-articles.pdf](https://github.com/paggers/FakeRank/blob/master/finding-key-articles.pdf)

