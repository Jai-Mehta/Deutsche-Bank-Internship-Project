# input

# {
#   "document": {
#     "content": "This is a success. We have no success to show for.",
#     "language": "en",
#     "type": "PLAIN_TEXT"
#   },
#   "encodingType": "UTF8",
#   "features": {
#     "classificationModelOptions": {
#       "v2Model": {
#         "contentCategoriesVersion": "V2"
#       }
#     },
#     "extractEntities": true,
#     "extractEntitySentiment": true,
#     "classifyText": false,
#     "extractSyntax": false
#   }
# }

# output

# {
#   "sentences": [],
#   "tokens": [],
#   "entities": [
#     {
#       "name": "success",
#       "type": "OTHER",
#       "metadata": {},
#       "salience": 0.92553633,
#       "mentions": [
#         {
#           "text": {
#             "content": "success",
#             "beginOffset": 10
#           },
#           "type": "COMMON",
#           "sentiment": {
#             "magnitude": 0.6,
#             "score": 0.6
#           }
#         }
#       ],
#       "sentiment": {
#         "magnitude": 1.4,
#         "score": 0.7
#       }
#     },
#     {
#       "name": "success",
#       "type": "OTHER",
#       "metadata": {},
#       "salience": 0.07446366,
#       "mentions": [
#         {
#           "text": {
#             "content": "success",
#             "beginOffset": 30
#           },
#           "type": "COMMON",
#           "sentiment": {
#             "magnitude": 0.2,
#             "score": -0.2
#           }
#         }
#       ],
#       "sentiment": {
#         "magnitude": 0.2,
#         "score": -0.2
#       }
#     }
#   ],
#   "documentSentiment": {
#     "magnitude": 0,
#     "score": 0
#   },
#   "language": "en",
#   "categories": [],
#   "moderationCategories": []
# }
import pandas as pd
import pickle
from datastore_self_defined import datastore_response_push, datastore_get
from google.cloud import language_v1
import os
import json

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/diyaaggarwal/team-9-case-study/case-study-app/key.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"


def get_nlp_data(text_content, extract_entities=False, extract_entity_sentiment=False, classify_text=False, extract_syntax=False, moderate_text=False, extract_document_sentiment=False):
    """Pass text_content as plain text and enable the features you wish to use, Returns response in JSON format
    """
    client = language_v1.LanguageServiceClient()

    # Available types: PLAIN_TEXT, HTML
    type = language_v1.Document.Type.PLAIN_TEXT

    # Optional. If not specified, the language is automatically detected.
    # For list of supported languages:
    # https://cloud.google.com/natural-language/docs/languages
    language = "en"
    document = {"content": text_content, "type": type, "language": language}

    content_categories_version = (
        language_v1.ClassificationModelOptions.V2Model.ContentCategoriesVersion.V2
    )
    response = client.annotate_text(       
        request={
            "document": document,
            "encoding_type":"UTF8",
            "features": {           
                "classification_model_options": {
                "v2_model": {
                    "content_categories_version": content_categories_version
                }
                },
                "extract_entities": extract_entities,             
                "extract_entity_sentiment": extract_entity_sentiment,
                "classify_text": classify_text,
                "extract_syntax": extract_syntax,
                "moderate_text": moderate_text,
                "extract_document_sentiment": extract_document_sentiment
            }
        }
    )
    return response

def get_sentiment_score(response,wordlist):
    """Pass in the nlp response and list of words that you want the sentiments of. Returns list of tuples of words found and their sentiments.
    
    Tuple -> name of ent, magnitude of sentiment, score of sentiment
    """
    aggregate_score = []
    for ent in response['entities']:
        check = any(name in ent['name'].split() for name in wordlist)
        if check:
            if bool(ent['sentiment']['magnitude']) and bool(ent['sentiment']['score']):
                #print(ent.name, " -> found! Sentiment score: ",ent.sentiment.score," | Sentiment Magnitude: ", ent.sentiment.magnitude)
                # do calculations
                aggregate_score.append((ent['name'],ent['sentiment']['magnitude'],ent['sentiment']['score']))         
    return aggregate_score

def generate_push_response_df(dataframe):
    '''Pushes responses data to datastore from table "Article"'''
    count = 0
    index = []
    nlp_response = []
    bank_name_list = []
    url_list =[]
    article_title_list = []
    article_body_list = []
    article_publish_date_list = []
    article_publish_year_list = []
    for bank_name,url,article_title,article_body,article_publish_date,article_publish_year in dataframe.itertuples(index=False):
        index.append(count)
        nlp_response.append(get_nlp_data(text_content=article_body,extract_entity_sentiment=True))
        bank_name_list.append(bank_name)
        url_list.append(url)
        article_title_list.append(article_title)
        article_body_list.append(article_body)
        article_publish_date_list.append(article_publish_date)
        article_publish_year_list.append(article_publish_year)
        count = count + 1

    responses_df = pd.DataFrame({
        'index': index,
        'nlp_response': nlp_response,
        'bank_name': bank_name_list,
        'url': url_list,
        'article_title': article_title_list,
        'article_body': article_body_list,
        'article_publish_date': article_publish_date_list,
        'article_publish_year': article_publish_year_list
    })

    with open('entity_sentiment.pkl', 'wb') as fp:
        pickle.dump(responses_df, fp)
        print('dataframe of responses saved successfully to file')
    
    return datastore_response_push(responses_df)
    




