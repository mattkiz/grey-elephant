import facebook
from googlesearch import search
from urllib.request import urlopen
from bs4 import BeautifulSoup
from nltk import word_tokenize, pos_tag
from nltk.corpus import stopwords
import subprocess
from gensim import corpora, models, similarities

user_id = ""
token = 'EAAZAqVsGAF3MBACzaZCknkiS2GAjEgerKOvZAWZBa3ZBdLuyrJ9XwTVSVvF3K2PqCJAqnd7V1fhZB2LwHMKsxFA7mGSXEB578XHopNZBUwbZCnhDc4r0I2FHZC0DqlJzaMPTKvteJAF2PemWwoACD64K73c3fBJSGF6T5ouvqlZCUdMfZAfCorQzZCnBgfG3TnFBAvaLAC9lkZAId0wZDZD'
graph = facebook.GraphAPI(access_token=token, version=3.1)
stop_words = set(stopwords.words('english'))
likes = graph.get_connections(id='me', connection_name='likes')
for liked_page in likes['data']:
    words = []
    title = liked_page['name']
    query = title
    print(query + ":-")
    for site in search(query, tld="co.in", num=1, stop=1, pause=1):
        try:
            print(site)
            uClient = urlopen(site)
            site_html = uClient.read()
            uClient.close()
            page_soup = BeautifulSoup(site_html, "html.parser")
            desc_container = page_soup.findAll("p")
            for c in desc_container:
                print(c.text)
        except:
            pass
'''
            for paragraph in desc_container:
                tokenized_paragraph = word_tokenize(paragraph.text)
                pos_tag_pair = pos_tag(tokenized_paragraph)
                words += [w[0] for w in pos_tag_pair if w[1]=='NN' or w[1]=='NNS' or w[1]=='NNP' or w[1]=='NNPS']

       
    words_frequency = [[x, words.count(x)] for x in set(words)]
    sorted(words_frequency, key=lambda x: x[1], reverse=True)

    buzz_words = [x[0] for x in words_frequency[:15]]
    print(buzz_words)
'''