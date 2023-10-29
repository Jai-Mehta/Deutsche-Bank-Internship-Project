# need method to input a keyword and get te score and aggregate sentiment of keyword and top n similar words 
# call preprocess -> modelwork use returned model to get top n similar words (method for topn words in wordsim.py)
# method will need to call get_nlp_data for the response on the processed data (use get_nlp_data in text_analysis.py)
# search for topn words in response and keyword and get sentiment (method for sentiment for top words in textanalysis.py)
# calculate 0-100 score and store (may be local method depending on use)
# display score

import plotly
import pickle
import plotly.express as px
import pandas as pd
import os
import sys
# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))
# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)
# adding the parent directory to
# the sys.path.
sys.path.append(parent)
from datastore_self_defined import datastore_response_get,datastore_rishav_histogram_push, datastore_rishav_histogram_get
from wordsim import modelwork, topn_similar_words
from text_analysis import get_sentiment_score


# rough function to test different params. Training error might not be correct due to word2vec issues, so rely on needs for correct training
def training_model(combined_bank_articles):
    hyperparams = [[300,3,3,1],
                   [250,6,6,0],
                   [400,6,6,0],
                   [400,6,6,1],
                   [500,2,4,0],
                   [500,2,4,1],
                   [500,3,3,0],
                   [300,4,4,0],
                   [200,6,6,0]]
    for params in hyperparams:
        model, training_error = modelwork(processed_text_PLAIN=combined_bank_articles,VECTOR_SIZE=params[0],MIN_COUNT=params[1],WINDOW=params[2],SG=params[3])
        print(params," : TRAINING ERROR :",training_error)


def histogram_keyword_analysis():
    print("Starting analysis.....")
    """"Calculates df for display for figure for use in the display"""
    #use the combined texts for trainig word2vec model. relative link from path of main.py
    dataframe = datastore_response_get()
    print("Got data....")
    print(dataframe.head())

    # with open('entity_sentiment.pkl', 'rb') as fp:
    #     dataframe = pickle.load(fp)

    #print(dataframe.head())

    combined_bank_articles = ' '.join(dataframe["article_body"])
    
    model, training_error = modelwork(processed_text_PLAIN=combined_bank_articles,VECTOR_SIZE=1000,MIN_COUNT=3,WINDOW=15,SG=1)
    #plot_embeddings(model=model)
    
    #Use these keywords
    keyword_list = ["emission", "environment", "resource", "climate", "diversity", "innovation","community", "social", "shareholder",  "governance", "management", "workforce"]

    #dict using keyword as key and list of similar words as values
    word_to_search = {}
    print("searching.....")
    for word in keyword_list: 
        word_confidence = topn_similar_words(model=model,topn=10,confidence_limit=0,word=word)
        if len(word_confidence) != 0:
            word_to_search[word] = [tup[0] for tup in word_confidence]
            print(word," -- ",word_to_search[word])

    # will be a dict of dicts of struct - { "bank": {"keyword":[sum of score,number of additions],..},..}
    banks_keywords_scores = {}
    for index,nlp_response,bank_name,url,article_title,article_body,article_publish_date,article_publish_year in dataframe.itertuples(index=False):        #if dict does not have that bank,create key
        if banks_keywords_scores.get(bank_name) == None:
            banks_keywords_scores[bank_name] = {}  
        for word, similars in word_to_search.items():
            #get sentiment for word and all similars
            combined_list_of_words = []
            combined_list_of_words.append(word)
            combined_list_of_words.extend(similars)
            print("Searching each wordlist - ",combined_list_of_words,"for bank - ", bank_name)
            word_mag_sco = get_sentiment_score(response=nlp_response,wordlist=combined_list_of_words)
            #calculate final score by sentiment mag*score if there are scores to calculate for particular article
            if len(word_mag_sco) != 0:
                word_score_per_word = sum([( y * z ) for x, y, z in word_mag_sco])
                if banks_keywords_scores[bank_name].get(word) == None:
                    banks_keywords_scores[bank_name][word] = [0,0]
                banks_keywords_scores[bank_name][word] = [banks_keywords_scores[bank_name][word][0] + word_score_per_word , banks_keywords_scores[bank_name][word][1] + 1]
    
    # with open('nlpscore_dict.pkl', 'wb') as fp:
    #     pickle.dump(banks_keywords_scores, fp)
    #     print('dictionary saved successfully to file')
    
    # Empty lists to store the data
    banks = []
    keywords = []
    scores = []

    print(banks_keywords_scores)
    
    # Iterate over the outer dictionary
    for bank, keywords_dict in banks_keywords_scores.items():
        # Iterate over the inner dictionary
        for keyword, value in keywords_dict.items():
            # Append the values to the lists
            banks.append(bank)
            keyword_display = keyword.capitalize()
            if keyword_display == "Climate":
                keyword_display = "Climate Change"
            if keyword_display == "Resource":
                keyword_display = "Resource Use"
            keywords.append(keyword_display)
            scores.append(value[0]/value[1])

    # Create a DataFrame from the lists
    df_score = pd.DataFrame({'Bank Name': banks, 'Keyword': keywords, 'Score': scores})
    # Display the DataFrame
    print(df_score.head(15))
    with open('df_score.pkl', 'wb') as fp:
        pickle.dump(df_score, fp)
        print('dataframe saved successfully to file')

    return datastore_rishav_histogram_push(df_score)
