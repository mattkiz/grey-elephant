from gensim.models import Word2Vec
from googlesearch import search
from nltk import word_tokenize
from nltk.corpus import stopwords
import urllib.request
from bs4 import BeautifulSoup
import pickle
import facebook
import random


suggestions = 3
categories = pickle.load(open("eBay_categories.pkl","rb"))
model = pickle.load(open("model.pkl", "rb"))
training = pickle.load(open("training.pkl", "rb"))
nn = pickle.load(open("neuralnetwork.pkl","rb"))
subcategoryIDs = pickle.load(open("subcategoryIDs.pkl","rb"))
sub_categories = {}

s = set(stopwords.words("english"))

keys_array = []
#form the probability chart
for key in training.keys():
    sub_categories[key] = 0
    keys_array.append(key)

def generate_IDs(token):
    graph = facebook.GraphAPI(access_token=token, version=3.1)
    stop_words = set(stopwords.words('english'))
    likes = graph.get_connections(id='me', connection_name='likes') #send invitation to friend
    for liked_page in likes['data']:
        individual_sub_categories = {}
        for key in training.keys():
            individual_sub_categories[key] = 0
            keys_array.append(key)

        words = []
        title = liked_page['name']
        query = title
        print("Query: " + query)
        response = search(query, tld="com", num=1, start=0, stop=1, pause=0)
        result = next(response)
        try:
            print(result)
            uContent = urllib.request.urlopen(result)
            html = uContent.read()
            soup = BeautifulSoup(html, "html.parser")
            paragraphs = soup.findAll("p")
            for paragraph in paragraphs:
                sentence = word_tokenize(paragraph.text)
                filtered_sentence = [w for w in sentence if w not in s]
                for w in filtered_sentence:
                    try:
                        individual_sub_categories[keys_array[nn.predict([model.wv[w]])[0]]]+=1
                    except:
                        pass
            uContent.close()
        except:
            pass


        total_score = 0
        for i in [individual_sub_categories[x] for x in individual_sub_categories.keys()]: total_score += i
        if total_score==0:
            continue
        else:
            for x in individual_sub_categories.keys(): sub_categories[x] += individual_sub_categories[x] / total_score
            teaser = [x for x in individual_sub_categories.keys() if individual_sub_categories[x] != 0]
            teaser = random.choice(teaser)
            teaser = random.choice(subcategoryIDs[teaser])
            print(random.choice(get_category(teaser))['title'])
            #print(sub_categories)
    abs_total_score = 0;
    for x in sub_categories.keys(): abs_total_score += sub_categories[x]
    if abs_total_score == 0 : return None
    output = []
    for i in range(suggestions):
        threshold = random.uniform(0,1) * abs_total_score
        current_score = 0
        for x in sub_categories.keys():
            current_score += sub_categories[x]
            if current_score >= threshold:
                output.append(subcategoryIDs[x])
                break
    return output


