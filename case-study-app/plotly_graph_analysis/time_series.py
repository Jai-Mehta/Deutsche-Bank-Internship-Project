# need method to input a keyword and get te score and aggregate sentiment of keyword and top n similar words 
# call preprocess -> modelwork use returned model to get top n similar words (method for topn words in wordsim.py)
# method will need to call get_nlp_data for the response on the processed data (use get_nlp_data in text_analysis.py)
# search for topn words in response and keyword and get sentiment (method for sentiment for top words in textanalysis.py)
# calculate 0-100 score and store (may be local method depending on use)
# display score

import plotly
import pickle
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, callback
import pandas as pd
import os
import sys
import random
# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))
# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)
# adding the parent directory to
# the sys.path.
sys.path.append(parent)
from datastore_self_defined import *
from wordsim import modelwork, topn_similar_words, plot_embeddings
from text_analysis import get_nlp_data, get_sentiment_score




def time_series_analysis():
    """"Returns figure for use in the display"""

    # Output df to use :
    # | bank name | keyword | aggregate_score |
    #
    # figure :
    # x-axis = bank name, y-axis = score
    # color of bar = keyword

    #use the combined texts for taring word2vec model. relative link from path of main.py
    
    # with open('/Users/diyaaggarwal/team-9-case-study/case-study-app/entity_sentiment.pkl', 'rb') as fp:
    #     dataframe = pickle.load(fp)
    dataframe = datastore_response_get()
    # dataframe = pd.read_csv('../Scrapers/boa_scraped_data.csv')
    combined_bank_articles = ' '.join(dataframe["article_body"])
    
    
    model, training_error = modelwork(processed_text_PLAIN=combined_bank_articles,VECTOR_SIZE=1000,MIN_COUNT=3,WINDOW=15,SG=1)
    
    #Use these keywords
    keyword_list = ["emission", "environment", "resource", "climate", "diversity", "innovation","community", "social", "shareholder",  "governance", "management", "workforce"]

    #dict using keyword as key and list of similar words as values
    word_to_search = {}
    print("searching.....")
    #fill dict
    for word in keyword_list: 
        word_confidence = topn_similar_words(model=model,topn=10,confidence_limit=0,word=word)
        #print("------------",word,"--------------")
        #print([tup[0] for tup in word_confidence])
        if len(word_confidence) != 0:
            word_to_search[word] = [tup[0] for tup in word_confidence]

    #get response and sentiment score of words
    # FOR each bank with an article text (row in df)
    # GET response of NLP
    # FOR each keyword
    # GET sentiment, magnitude for keyword and similar words in each article for each bank
    # CALCULATE the score for each keyword in each article for each bank

    # will be a dict of dicts of struct - { "bank": {"keyword":[sum of score,number of additions],..},..}
    banks_keywords_scores = {}
    
    for index,nlp_response,bank_name,url,article_title,article_body,article_publish_date,article_publish_year in dataframe.itertuples(index=False):
        if banks_keywords_scores.get(article_publish_year) == None:
            banks_keywords_scores[article_publish_year] = {}
        #if dict does not have that bank,create key
        if banks_keywords_scores[article_publish_year].get(bank_name) == None:
            banks_keywords_scores[article_publish_year][bank_name] = {}
            
        for word, similars in word_to_search.items():
            #get sentiment for word and all similars
            # similars.append(word)
            combined_list_of_words = []
            combined_list_of_words.append(word)
            combined_list_of_words.extend(similars)
            word_mag_sco = get_sentiment_score(response=nlp_response,wordlist=combined_list_of_words)
            # word_mag_sco = [(" ", random.randint(0,1), random.randint(0,1)), (" ", random.randint(0,1), random.randint(0,1)), (" ", random.randint(0,1), random.randint(0,1))]
            #calculate final score by sentiment mag*score if there are scores to calculate for particular article
            if len(word_mag_sco) != 0:
                word_score_per_word = sum([( y * z ) for x, y, z in word_mag_sco])
                #if bank does not have a specific keyword data, initialize to [0,0] where first number is the sum of the scores and second is the number of times scores is added for use in avg
                
                if banks_keywords_scores[article_publish_year][bank_name].get(word) == None:
                    banks_keywords_scores[article_publish_year][bank_name][word] = [0,0]
                banks_keywords_scores[article_publish_year][bank_name][word] = [banks_keywords_scores[article_publish_year][bank_name][word][0] + word_score_per_word, banks_keywords_scores[article_publish_year][bank_name][word][1] + 1]
    
    with open('nlp_scores.pkl', 'wb') as fp:
        pickle.dump(banks_keywords_scores, fp)
        print('dictionary saved successfully to file')
        
    # Empty lists to store the data
    banks = []
    keywords = []
    scores = []
    years = []

    # Iterate over the outer dictionary
    for year, o_dict in banks_keywords_scores.items():
        for bank, keywords_dict in o_dict.items():
            # Iterate over the inner dictionary
            for keyword, value in keywords_dict.items():
                # Append the values to the lists
                years.append(year)
                banks.append(bank)
                keyword_display = keyword.capitalize()
                if keyword_display == "Climate":
                    keyword_display = "Climate Change"
                if keyword_display == "Resource":
                    keyword_display = "Resource Use"
                
                keywords.append(keyword_display)
                scores.append(value[0]/value[1])

    df = pd.DataFrame({
        'Year': years,
        'Bank Name': banks,
        'Keyword': keywords,
        'Score': scores
    })
    
    
    # {'Year':{'Bank Name':{'Keyword': 'Score'}}}

    with open('time_series_data.pkl', 'wb') as fp:
        pickle.dump(df, fp)
        print('dictionary saved successfully to file')
        
    # return df
    return datastore_diya_time_series_push(df)



# with open('case-study-app/entity_sentiment.pkl', 'rb') as fp:
#         df = pickle.load(fp)
# print(df)

    
def return_time_series(Keyword):
    df = datastore_diya_time_series_get()
    # with open('/Users/diyaaggarwal/team-9-case-study/case-study-app/plotly_graph/time_series_data.pkl', 'rb') as fp:
    #     df = pickle.load(fp)
    # word_df = df.sort_values('Keyword')

    #dropdown = dcc.Dropdown(["Emission", "Environment", "Resource Use", "Climate Change", "Diversity", "Innovation","Community", "Social", "Shareholder",  "Governance", "Management", "Workforce"], "Emision", clearable=False)
    words = ["Emission", "Environment", "Resource Use", "Climate Change", "Diversity", "Innovation","Community", "Social", "Shareholder",  "Governance", "Management", "Workforce"]
    
    
    # for word in words:
    #     word_df = df[df["Keyword"] == word]
    #     # emmission_df = df[df["Keyword"] == "Environment"]
    #     year_df = word_df.sort_values('Year')
    #     fig = px.line(year_df, x="Year", y="Score", color="Bank Name",markers=True,title="Time Series for "+word,)
    #     plotly.offline.plot(fig)
    year_df = df[df["Year"] >= '2014']
    word_df = year_df[year_df["Keyword"] == Keyword]
    # emmission_df = df[df["Keyword"] == "Environment"]
    year_df = word_df.sort_values('Year')
    fig = px.line(year_df, x="Year", y="Score", color="Bank Name",markers=True,title="Time Series for "+Keyword,)
    # plotly.offline.plot(fig)
        
    
    return fig
    

#time_series_analysis()
# plot = return_time_series('Management')
# plot.show()