from types import NoneType
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
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
from datastore_self_defined import datastore_push
from datastore_self_defined import datastore_push
import dateutil.parser as dparser

def scrape_website_boa(url, b_name): 

    #lsts to store data
    bank_names = []
    urls = []
    article_titles = []
    article_bodies = []
    article_publish_dates = []
    article_publish_year = []

    #keep track of article count
    count_articles = 0
    es_art_cnt = 0

    # Retrieve the main page HTML
    main_page = requests.get(url)
    soup = BeautifulSoup(main_page.content, 'html.parser')

    #get all links to all articles on page
    links = soup.find_all("a",attrs={'class':'prlist-path'})
    
    #get the 'a' tag that has the title
    # title_tag = soup.find_all("a",{'class':'prlist-path'})
    # title =[]
    #get the title out of the tags
    #print(type(title_tag[1].find('p')))
    # for each in title_tag:
    #      print("--------")
    #      print(type(each.find('p')))
    #      if type(each.find('p')) is not NoneType:
    #         print(each.find('p').text)

    #Enumerate to each article on page
    article_clean = ""
    newsroom_article_addon = "https://newsroom.bankofamerica.com"
    for ind,link in enumerate(links):
        href = link['href']
        try:
            if not href.startswith('https'):
                href = newsroom_article_addon+href
                #print("-----")
                connected_page = requests.get(href)
                connected_soup = BeautifulSoup(connected_page.content, 'html.parser')

                #check if article is es and go to next iteration if so
                span_for_lang = connected_soup.find("span",attrs={'class':'lang-es'})
                if span_for_lang is not None:
                    es_art_cnt=es_art_cnt+1
                    continue
                    
                #get the div that has dates
                dates_div = connected_soup.find("div",attrs={'class':'pub-date'})
                date = dates_div.text.strip()
                
                #get the div with the article text
                article_full = connected_soup.find("div",{'class':'cmp-text'})
                #decompose/remove tags and content
                for sup in article_full.find_all("sup"):
                    sup.decompose()
                for sec_header in article_full.find_all("span",{'class':'media-contact-header'}):
                    sec_header.decompose()
                for footnote in article_full.find_all("span",{'class':'footnote-body'}):
                    footnote.decompose()
                #replace below tags with just the content
                replacelist = ["abbr","a","b","p","h2","span","li","ul","br"]
                for tag_html in replacelist:
                    for tag_store in article_full.find_all(tag_html):
                        tag_store.replaceWithChildren()
                
                article_clean = article_full.text.strip()
                
                count_articles = count_articles+1

                #store each article data
                bank_names.append(b_name)
                urls.append(href)
                article_titles.append("")#no title
                article_bodies.append(preprocess(article_text=article_clean))
                article_publish_dates.append(date)
                article_publish_year.append(dparser.parse(date,fuzzy=True).strftime("%Y"))
                   
        except:
            continue
    df = pd.DataFrame({
        'bank_name': bank_names,
        'url': urls,
        'article_title': article_titles,
        'article_body': article_bodies,
        'article_publish_date': article_publish_dates,
        'article_publish_year': article_publish_year
    })
    return df,count_articles,es_art_cnt

print("in bofa scraper")
url_list = [
    #Environment
    "https://newsroom.bankofamerica.com/content/newsroom/press-releases.html?page=1&year=all&category=press-release-categories/environment&categTitle=Environment",
    "https://newsroom.bankofamerica.com/content/newsroom/press-releases.html?page=2&year=all&category=press-release-categories/environment&categTitle=Environment",
    #Work and Employee Benefits
    "https://newsroom.bankofamerica.com/content/newsroom/press-releases.html?page=1&year=all&category=press-release-categories/great-place-to-work-and-employee-benefits&categTitle=Great%20Place%20to%20Work%20and%20Employee%20Benefits",
    #Racial and Economic Opportunity
    "https://newsroom.bankofamerica.com/content/newsroom/press-releases.html?page=1&year=all&category=press-release-categories/racial-equality-and-economic-opportunity&categTitle=Racial%20Equality%20and%20Economic%20Opportunity",
    "https://newsroom.bankofamerica.com/content/newsroom/press-releases.html?page=2&category=press-release-categories/racial-equality-and-economic-opportunity&year=all&categTitle=Racial%20Equality%20and%20Economic%20Opportunity",
    "https://newsroom.bankofamerica.com/content/newsroom/press-releases.html?page=3&category=press-release-categories/racial-equality-and-economic-opportunity&year=all&categTitle=Racial%20Equality%20and%20Economic%20Opportunity",
    "https://newsroom.bankofamerica.com/content/newsroom/press-releases.html?page=4&category=press-release-categories/racial-equality-and-economic-opportunity&year=all&categTitle=Racial%20Equality%20and%20Economic%20Opportunity",
    "https://newsroom.bankofamerica.com/content/newsroom/press-releases.html?page=5&category=press-release-categories/racial-equality-and-economic-opportunity&year=all&categTitle=Racial%20Equality%20and%20Economic%20Opportunity",
    "https://newsroom.bankofamerica.com/content/newsroom/press-releases.html?page=6&category=press-release-categories/racial-equality-and-economic-opportunity&year=all&categTitle=Racial%20Equality%20and%20Economic%20Opportunity",
    #Small Business
    "https://newsroom.bankofamerica.com/content/newsroom/press-releases.html?page=1&year=all&category=press-release-categories/small-business-commercial-banking&categTitle=Small%20Business,%20Business%20and%20Commercial%20Banking",
    "https://newsroom.bankofamerica.com/content/newsroom/press-releases.html?page=2&year=all&category=press-release-categories/small-business-commercial-banking&categTitle=Small%20Business,%20Business%20and%20Commercial%20Banking",
    "https://newsroom.bankofamerica.com/content/newsroom/press-releases.html?page=3&year=all&category=press-release-categories/small-business-commercial-banking&categTitle=Small%20Business,%20Business%20and%20Commercial%20Banking",
    #Sponsorships and Philantropy
    "https://newsroom.bankofamerica.com/content/newsroom/press-releases.html?page=1&year=all&category=press-release-categories/sponsorships-and-philanthropy&categTitle=Sponsorships%20and%20Philanthropy",
    "https://newsroom.bankofamerica.com/content/newsroom/press-releases.html?page=2&year=all&category=press-release-categories/sponsorships-and-philanthropy&categTitle=Sponsorships%20and%20Philanthropy",
    "https://newsroom.bankofamerica.com/content/newsroom/press-releases.html?page=3&year=all&category=press-release-categories/sponsorships-and-philanthropy&categTitle=Sponsorships%20and%20Philanthropy",
    "https://newsroom.bankofamerica.com/content/newsroom/press-releases.html?page=4&year=all&category=press-release-categories/sponsorships-and-philanthropy&categTitle=Sponsorships%20and%20Philanthropy",
    "https://newsroom.bankofamerica.com/content/newsroom/press-releases.html?page=5&year=all&category=press-release-categories/sponsorships-and-philanthropy&categTitle=Sponsorships%20and%20Philanthropy",
    #Sustainable Finance
    "https://newsroom.bankofamerica.com/content/newsroom/press-releases.html?page=1&year=all&category=press-release-categories/sustainable-finance&categTitle=Sustainable%20Finance",
    "https://newsroom.bankofamerica.com/content/newsroom/press-releases.html?page=2&year=all&category=press-release-categories/sustainable-finance&categTitle=Sustainable%20Finance"
]


b_name = 'Bank of America'  # Replace with your desired value
count_total_articles = 0
es_arts = 0
frames = []
for url in url_list:
    data_frame,count_articles,es_art_cnt = scrape_website_boa(url, b_name)
    count_total_articles = count_total_articles + count_articles
    es_arts=es_arts+es_art_cnt
    frames.append(data_frame)

#stores all data from boa
final_dataframe_boa = pd.concat(frames)
datastore_push(final_dataframe_boa,kind_passed='Article')
save_csv = input("Save in boa_scraped_data.csv? (y/n):")
if save_csv == 'y':
    final_dataframe_boa.to_csv('boa_scraped_data.csv',index=False)