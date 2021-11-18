import requests
from bs4 import BeautifulSoup 
import numpy
import pandas
import networkx
from pyvis.network import Network

print('Please give the starting node URL and the how many degrees of adjacency you want to vizualize:')
currentURL = input('URL:')
adj_factor = input('Degrees:')

links = [] #initialize empty lists for our loop
titles = [] 
saucepages = []
for i in range(int(adj_factor)):
  if i == 0: 
    sauce = requests.get(currentURL).text #get the text source from the currently assigned URL
    soup = BeautifulSoup(sauce, 'lxml') #parse the html using lxml and assign it to a BeautifulSoup object
    main = soup.find('div', class_='mw-parser-output') #scrape the main wikipedia page contents
    pg1_arts = main.p.find_all('a') #find the "articles" ('a'), ie, links,in the first paragraph ('p')

    for i in range(len(pg1_arts)): #loop through the list of articles we made earlier
      if 'wiki' in pg1_arts[i]['href']: #look at the URLs of the outgoing links ('href'), appending them only IF they're going to new wikipedia pages
        links.append(pg1_arts[i]['href']) 
        titles.append(pg1_arts[i]['title'])
      #this approach differentiates between links to footnotes/sources e.g. [1]
      #We've now made a list filled with the links, and another with the titles of all the linked pages in the first paragraph. 
    saucepages = [currentURL.split('/')[4]]*len(pg1_arts) #Our "source" for all outgoing pages is just this currentURL page, so fill the source column with it.

  else: #Expanding the network to further neighbours requires going through the links acquired in the first loop.
    #I will try to find a way to omit alot of this redundant code, but it works for now. 
    for i in range(len(links)): 
      currentURL = 'https://en.wikipedia.org' + links[i]
      sauce = requests.get(currentURL).text 
      soup = BeautifulSoup(sauce, 'lxml') 
      main = soup.find('div', class_='mw-parser-output') 
      pg1_arts = main.p.find_all('a') 

      for i in range(len(pg1_arts)): 
        if 'wiki' in pg1_arts[i]['href']: 
          links.append(pg1_arts[i]['href']) 
          titles.append(pg1_arts[i]['title'])
      saucepages = saucepages + ([currentURL.split('/')[4]]*len(pg1_arts))
      
#We want to make a list of nodes in our network and other information, which includes titles and links.
zipnodes = list(zip(titles,links)) #zip them up into a list of lists.
nodelist = pandas.DataFrame(zipnodes, columns = ['Title','Link'], index=[numpy.arange(len(zipnodes))]) #turn it into a dataframe.

#An edgelist contains the "source" and "target" nodes, indicating a relationship (an edge). 
zipedges = list(zip(saucepages,titles)) 
edgelist = pandas.DataFrame(zipedges, columns = ['Source','Target'], index=numpy.arange(len(zipedges))) 

graphy = networkx.Graph() #initialize an empty networkx graph object (the actual data structure, vs. the vizualization object below)
graphy = networkx.from_pandas_edgelist(edgelist, source='Source',target='Target') #give it our edge data
vizzed = Network(height='px', width='75%', bgcolor='#222222', font_color='white') #set vizualization parameters of a pyviz.network object 
vizzed.from_nx(graphy) #give it our network data
vizzed.show_buttons(filter_=['physics'])
vizzed.show('wikigraph.html') #vizualize it in html! 

#Now, how do we show hyperlink w/ hover over?

