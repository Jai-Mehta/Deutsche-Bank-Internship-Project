import requests
from bs4 import BeautifulSoup
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
from wordsim import preprocess
from datastore_self_defined import datastore_push


def text_from_html(html):
    response = requests.get(html)
    soup = BeautifulSoup(response.content, 'html.parser')

    title = soup.find("title").text
    date = soup.find("div", {"class": "story-live-date"}).contents[0][14:]
    year = date[-4:]
    text = soup.find("div", {"class": "dev-story-desc"}).get_text()
    
    return title, text, date, year


def get_all(page):
  url = "https://newsroom.fidelity.com/pressreleases?page=" + str(page)
  response = requests.get(url)
  soup = BeautifulSoup(response.content, 'html.parser')
  links = soup.find_all("a", {"class": "story-detail-bglayer"})
  links = [l["href"] for l in links]
  return links


data = []

for i in range(1, 20):
  page_list = get_all(i)
  for article in page_list:
    title, text, date, year = text_from_html(article)
    processed = preprocess(text)
    data.append({
      "bank_name": "Fidelity",
      "url": article,
      "article_title": title,
      "article_body": processed,
      "article_publish_date": date,
      "article_publish_year": year,
    })

df = pd.DataFrame(data)
# print(df)

df.to_csv('fidelity_scraped_data.csv', index=False)
datastore_push(df, kind_passed='Article')
