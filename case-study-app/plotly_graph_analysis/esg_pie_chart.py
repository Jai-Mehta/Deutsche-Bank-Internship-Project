import plotly
import pickle
import plotly.express as px
import pandas as pd
import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from datastore_self_defined import datastore_response_get, datastore_jack_pie_chart_push, datastore_jack_pie_chart_get
from wordsim import modelwork, topn_similar_words
from text_analysis import get_sentiment_score



def pie_chart_analysis():
    df = datastore_response_get()
    print("Got data....")
    print(df.head())


    combined_bank_articles = ' '.join(df["article_body"])
    

    model, training_error = modelwork(processed_text_PLAIN=combined_bank_articles,VECTOR_SIZE=1000,MIN_COUNT=3,WINDOW=15,SG=1)
    
    keyword_list = ["emission", "environment", "resource", "climate", "diversity", "innovation","community", "social", "shareholder",  "governance", "management", "workforce"]

    environmental_set = set(["emission", "environment", "resource", "climate"])
    social_set = set(["diversity", "innovation","community", "social"])
    governance_set = set(["shareholder",  "governance", "management", "workforce"])


    word_to_search = {}
    print("searching.....")
    for i in range(len(keyword_list)): 
        if i <= 3:
            add_to = environmental_set
        elif i <= 8:
            add_to = social_set
        else:
            add_to = governance_set
        word = keyword_list[i]
        word_confidence = topn_similar_words(model=model,topn=10,confidence_limit=0,word=word)
        if len(word_confidence) != 0:
            for tup in word_confidence:
                add_to.add(tup[0])
            word_to_search[word] = [tup[0] for tup in word_confidence]
            print(word," -- ",word_to_search[word])
    
    e_list = list(environmental_set)
    s_list = list(social_set)
    g_list = list(governance_set)

    bank_esg = {}
    for index,nlp_response,bank_name,url,article_title,article_body,article_publish_date,article_publish_year in df.itertuples(index=False):
        if bank_name not in bank_esg:
            bank_esg[bank_name] = [0, 0, 0]
        
        e_sent = get_sentiment_score(response=nlp_response,wordlist=e_list)
        if len(e_sent) > 0:
            bank_esg[bank_name][0] += sum([(y * z) for x, y, z in e_sent])

        s_sent = get_sentiment_score(response=nlp_response,wordlist=s_list)
        if len(s_sent) > 0:
            bank_esg[bank_name][1] += sum([(y * z) for x, y, z in s_sent])
        
        g_sent = get_sentiment_score(response=nlp_response,wordlist=g_list)
        if len(g_sent) > 0:
            bank_esg[bank_name][2] += sum([(y * z) for x, y, z in g_sent])


    banks = []
    environmental = []
    social = []
    governance = []
    for bank, scores in bank_esg.items():
        banks.append(bank)
        environmental.append(scores[0])
        social.append(scores[1])
        governance.append(scores[2])

    pie_df = pd.DataFrame({
        'bank': banks,
        'environmental': environmental,
        'social': social,
        'governance': governance
    })
    
    print(pie_df)
    return datastore_jack_pie_chart_push(pie_df)

def display_pie_chart(bank):
    df = datastore_jack_pie_chart_get()
    vals = df.loc[df['bank'] == bank].iloc[0]
    
    fig = px.pie(
        values=list(vals)[1:],
        names=['Environmental', 'Social', 'Governance'],
        title=bank,
    )

    return fig



# pie_chart_analysis()
# display_pie_chart("Deutsche Bank")


