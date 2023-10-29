import bs4 as bs
import urllib.request
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
    
nltk.download('punkt')
nltk.download('stopwords')
import numpy as np
from sklearn.manifold import TSNE
import string
import re
import spacy
#python -m spacy download en
nlp = spacy.load('en_core_web_sm')
from spacy.tokens import Doc
import plotly
import plotly.graph_objs as go
from gensim.models import Word2Vec

def getdata(textSource=True):
    """if textSource true gets data from wiki else gets data from ./Articles/article1.txt located in same directory as code"""
    if textSource:
        #TEST DATA FROM WIKI
        # send the url request to open and read the website
        scrapped_data = urllib.request.urlopen('https://en.wikipedia.org/wiki/Machine_learning')
        # read the article with beautiful soup lxml parser
        article = scrapped_data.read()
        parsed_article = bs.BeautifulSoup(article,'lxml')
        # parse only the paragraph tag inside the website HTML
        paragraphs = parsed_article.find_all('p')
        # get the string of the website from the paragraph tag
        article_text = ""
        for p in paragraphs:
            article_text += p.text
    else:
        #DATA FROM ARTICLES
        with open('article.txt', 'r',encoding='utf8') as file:
            article_text = file.read()
    return article_text


#TEXT PREPROCESSING
def preprocess(article_text):
    """Takes in a plain text string and removes unneccessary characters, removes stopwords, lemmatizes and return a plain string of words in processed_text_PLAIN
    Return Empty if article_text is empty"""
    #remove useless characters like numbers etc
    article_text = article_text.replace('\n', '')
    if len(article_text) == 0:
        print('Error: Article is empty!')
        return ""
    processed_article = article_text.lower()
    processed_article = re.sub(r'\s+', ' ', processed_article)
    processed_article = re.sub(r'[!"#$%&\'()*+,-./:;<=>\"?@[\]^_`{|}~”“’0-9â€“]','', processed_article)
    # Tokenize 
    all_sentences = sent_tokenize(processed_article)
    all_words = [word_tokenize(sent) for sent in all_sentences]
    # Removing Stop Words
    if len(all_words)==0:
        print("all words empty")
        return ""
    stops = set(stopwords.words('english'))
    for i in range(len(all_words)):
        all_words[i] = [w for w in all_words[i] if w not in stops]
    # Lemmatizing
    all_words = ' '.join(all_words[0])
    doc = nlp(all_words)
    # Create list of tokens from given string
    tokens = []
    for token in doc:
        tokens.append(token)
    
    processed_text_list = []
    for token in doc:
        # print(token.pos_, token.lemma_)
        processed_text_list.append(token.lemma_)
    processed_text = []
    processed_text.append(processed_text_list)
    processed_text_PLAIN = ' '.join(processed_text[0])
    if len(processed_text_PLAIN) == 0:
        print('Error: Article is garbage, and is empty after preprocessing!')
        return ""
    return processed_text_PLAIN


def modelwork(processed_text_PLAIN, VECTOR_SIZE = 150, MIN_COUNT = 6, WINDOW = 3, SG = 1):
    """Pass the plain processed text  after using preprocess(..) and specify model parameters. Then use topn_similar_words for word similarity. Other methods are also available in word2vec, so look at that documentation if needed. Returns trained model and training loss"""
    list_of_words = []
    list_of_words.append(processed_text_PLAIN.split())
    #MODEL WORK
    word2vec = Word2Vec(list_of_words, min_count=MIN_COUNT,vector_size=VECTOR_SIZE, window=WINDOW,sg=SG,compute_loss=True)
    training_loss = word2vec.get_latest_training_loss()

    return word2vec, training_loss

def topn_similar_words(model, word, topn=10, confidence_limit=0):
    """get list of top n words and their confidences as a list of tuples. if sentiment_limit is set, returns topn words or less that are higher confidence than confidence_limit.
    Range of limit is 0-1. May return empty if there are no words above the confidence_limit. Returns empty list of word is not in vocabulary"""
    try:
        words_similar = model.wv.most_similar(word,topn=topn)
        for pair in words_similar:
            if pair[1]<confidence_limit:
                words_similar.remove(pair)
        return words_similar
    except KeyError:
        print("KeyError: '",word,"' not in vocabulary")
        return []

#PLOTLY
def reduce_dimensions(model):
    num_components = 2  # number of dimensions to keep after compression

    # extract vocabulary from model and vectors in order to associate them in the graph
    vectors = np.asarray(model.wv.vectors)
    labels = np.asarray(model.wv.index_to_key)  

    # apply TSNE 
    tsne = TSNE(n_components=num_components, random_state=0)
    vectors = tsne.fit_transform(vectors)

    x_vals = [v[0] for v in vectors]
    y_vals = [v[1] for v in vectors]
    return x_vals, y_vals, labels


def plot_embeddings(model):
    """Returns TSNE fig and shows figure automatically in browser. Helpful for understanding model success"""
    x_vals, y_vals, labels = reduce_dimensions(model)
    fig = go.Figure()
    trace = go.Scatter(x=x_vals, y=y_vals, mode='markers', text=labels)
    fig.add_trace(trace)
    fig.update_layout(title="Word2Vec - Visualizing using TSNE")
    plotly.offline.plot(fig)
    #fig.show()
    return fig

def find_occurence_in_article(article,word_list):
    """returns true if any word in list is in article else false"""
    has_occurrences = any(string in article for string in word_list)
    return has_occurrences
#hyperparameter tuning with raytune is possible if needed 
