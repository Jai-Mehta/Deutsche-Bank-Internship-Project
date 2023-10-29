from datastore_self_defined import datastore_get
from text_analysis import generate_push_response_df
from plotly_graph_analysis.keyword_analysis_by_bank_histogram import histogram_keyword_analysis
from plotly_graph_analysis.time_series import time_series_analysis
import pickle
from datastore_self_defined import datastore_response_push


'''RUN SETUP.PY ONLY ONCE'''
#Delete Table "Articles" before run
#Run scrapers, each scraper should push data to datastore "Article"
scrape_ = input("Scrape BOA, DB, Fidelity, JPMC and PNC and push all data to Articles table? (y/n):")
if scrape_ == 'y':
    import Scrapers.bofa_scraper as bofa_scraper
    print("BOA scraped")
    import Scrapers.db_scraper as db_scraper
    print("DB scraped")
    import Scrapers.fidelity_scraper as fidelity_scraper
    print("Fidelity scraped")
    import Scrapers.pnc_scraper as pnc_scraper
    print("PNC scraped")
    import Scrapers.jpmc_scraper as jpmc_scraper
    print("JPMC scraped")
    
gen_responses_pickle_ = input("Generate and push responses to Response table FROM PICKLE? (Warning: Say 'n' to the next question) (y/n):")
if gen_responses_pickle_ == 'y':
    with open('./plotly_graph/entity_sentiment.pkl', 'rb') as fp:
            df = pickle.load(fp)
    datastore_response_push(df)



#Generate nlp entity sentiment responses for all articles and push into datastore "Response"
gen_responses_ = input("Generate and push responses to Response table? (Warning: This incurs large charges on NLP) (y/n):")
if gen_responses_ == 'y':
    #get datastore "Article"
    df = datastore_get(kind_passed='New_Article')
    generate_push_response_df(df)

#Run data use for all graphs and pushed to datastore
get_graph_data_ = input("Run and push graph df data for all graphs? (y/n):")
if get_graph_data_ == 'y':
    histogram_keyword_analysis()
    time_series_analysis()
    # ADD REST OF GRAPH DATA GENERATION HERE


