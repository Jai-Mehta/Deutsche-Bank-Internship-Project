import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import os
import sys
from google.cloud import datastore


current = os.path.dirname(os.path.realpath(__file__))

parent = os.path.dirname(current)
 
sys.path.append(parent)
from wordsim import preprocess
from datastore_self_defined import datastore_push


home_url = 'https://www.jpmorganchase.com'

def get_all_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = []
    year = " "

    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.startswith('/news-stories/'):
            links.append(home_url + href)

    return links

# Example usage
url = 'https://www.jpmorganchase.com/news-stories/news'
all_links = get_all_links(url)
all_links = all_links[5:]
res = [all_links[i] for i in range(len(all_links)) if i % 2 != 0]
# for link in res:
    # print(link)
    
def scrape_article(url,year):
    # print(url)
    
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    article_body = soup.find('div', class_='article__body__text')

    body = article_body.get_text()

    article_title = soup.find('h1', class_='article__body__head')

    title = article_title.get_text()

    date_pattern = r"([A-Za-z]+) (\d{1,2}), (\d{4})"

    dates = re.findall(date_pattern, body)
    yr=year
    pub_date= None
    if(len(dates)!=0):
      pub_date=dates[0]
    if(len(dates)==0) :
      article_date = soup.find('div', class_='article__body__abstract--date article__body__text--small')
      if(article_date):
        # date_pat = r"([A-Za-z]+) (\d{1,2}), (\d{4})"
        article_d = article_date.get_text()
        dates = re.findall(date_pattern, article_d)  
        if(len(dates)!=0):
          pub_date=dates[0]

    if(pub_date is not None):
      yr= int(pub_date[2])   
      pub_date = ''.join(pub_date)
      #pub_date = str(pub_date)

    body = preprocess(body)

    if(url=='https://www.jpmorganchase.com/news-stories/celebrating-juneteenth'):
        yr='2020'

    yr=str(yr)
    return body,title,pub_date,yr


# Example usage
bank_name = "JPMorgan Chase & Co"
data = []
prev = "2023"
for url in res:
    body,title, date, year = scrape_article(url,prev)
    prev = year
    data.append({
    'bank_name': bank_name,
        'url': url,
        'article_title': title,
        'article_body': body,
        'article_publish_date': date,
        'article_publish_year' : year
    })

df = pd.DataFrame(data)


df.to_csv('jpmorganchase.csv', encoding='utf-8', index=False)

check_pushed = datastore_push(df,"Articles")

print(check_pushed)


