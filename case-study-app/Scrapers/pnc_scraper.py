import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys
import os
 
# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))
 
# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)
 
# adding the parent directory to
# the sys.path.
sys.path.append(parent)
from wordsim import preprocess
import datastore_self_defined


# Function to scrape the newsroom page and extract the desired information
def scrape_newsroom_page(url):
    # Send a GET request to the newsroom page
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all divisions with class="wd_item"
    wd_items = soup.find_all('div', class_='wd_item_wrapper')
    
    # Create empty lists to store the extracted information
    bank_names = []
    urls = []
    article_titles = []
    article_bodies = []
    article_publish_dates = []
    article_publish_year = []
    
    # Iterate over each wd_item division
    for item in wd_items:
        bank_names.append("PNC Financial Services")
        article_bodies.append('')
        # Extract article title and URL from wd_title division
        wd_title = item.find('div', class_='wd_title')
        title_url = wd_title.find('a')
        title_text = title_url.text.strip()
        article_titles.append(title_text)
        article_url = title_url['href']
        urls.append(article_url)
        # Extract article publish date from wd_date division
        wd_date = item.find('div', class_='wd_date')
        article_publish_dates.append(wd_date.text.strip())
        article_publish_year.append(wd_date.text.strip()[-4:])
        
    # Create a DataFrame from the extracted information
    df = pd.DataFrame({
        'bank_name': bank_names,
        'url': urls,
        'article_title': article_titles,
        'article_body': article_bodies,
        'article_publish_date': article_publish_dates,
        'article_publish_year': article_publish_year
    })
    
    for link in urls:
        try: 
            article_response = requests.get(link)
            article_soup = BeautifulSoup(article_response.text, 'html.parser')
            article_body = article_soup.find('div', class_='wd_body wd_news_body')
            paragraphs = article_body.find_all('p')
            body = " ".join([p.get_text() for p in paragraphs])
            processed_body = preprocess(body)
            row_num = df[df['url'] == link].index[0]
            df.at[row_num, 'article_body']= processed_body
        except: 
            print("This link is broken.") 
    return df



dataframe1 = scrape_newsroom_page('https://pnc.mediaroom.com/index.php?s=3473&l=100&o=0')
dataframe2 = scrape_newsroom_page('https://pnc.mediaroom.com/index.php?s=3473&l=100&o=100')
dataframe3 = scrape_newsroom_page('https://pnc.mediaroom.com/index.php?s=3473&l=100&o=200')
dataframe4 = scrape_newsroom_page('https://pnc.mediaroom.com/index.php?s=3473&l=100&o=300')
dataframe5 = scrape_newsroom_page('https://pnc.mediaroom.com/index.php?s=3473&l=100&o=400')
dataframe6 = scrape_newsroom_page('https://pnc.mediaroom.com/index.php?s=3473&l=100&o=500')
    
frames = [dataframe1, dataframe2, dataframe3, dataframe4, dataframe5, dataframe6]
dataframe = pd.concat(frames)
dataframe.to_csv('pnc_scraped_data.csv',index=False)
# print(dataframe)

check = datastore_self_defined.datastore_push(dataframe, "Article")
print(check)