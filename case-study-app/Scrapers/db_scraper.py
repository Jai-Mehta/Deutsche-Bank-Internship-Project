import json
import re
import html
import pandas as pd
import requests
# from google.cloud import datastore
import os
import sys
sys.path.append('D:/Git Uploads/team-9-case-study/case-study-app')       
import wordsim
import datastore_self_defined


def convert_html_entities(text):
    converted_text = html.unescape(text)
    return converted_text
def remove_tags(text):
    pattern = r'<([^>]*)>'
    result = re.sub(pattern, '', text)
    return result
def scrape_db(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
    bank = "Deutsche Bank"
    count = 0
    bank_name = []
    url = []
    article_title = []
    article_body = []
    article_publish_date = []
    article_publish_year = []


    for ele in data["contentlets"]:
        try:
            if (ele["hostName"]) and (ele["headline"]) and (ele["richText"]) and (ele["publishDate"]):

                bank_name.append(bank)
                # print(bank_name)
                url.append(ele["hostName"])
                # print(ele["hostName"])
                article_title.append(ele["headline"])
                # print(ele["headline"])
                article_body.append(wordsim.preprocess(convert_html_entities(remove_tags(ele["richText"]))))
                # print(memoryview(convert_html_entities(remove_tags(ele["richText"])).encode('utf-8')).nbytes)
                # print(convert_html_entities(remove_tags(ele["richText"])))
                article_publish_date.append(ele["publishDate"])
                # print(ele["publishDate"])
                # print(count)
                article_publish_year.append(ele["publishDate"].split(" ")[0][:4])
                # break
                
        except:
            # print("**********************************************************************")
            # count+=1
            # print(count)
            # print("**********************************************************************")
            continue
        # finally:
            # count+=1

    df = pd.DataFrame({
    'bank_name' : bank_name, 
    'url' : url, 
    'article_title' : article_title, 
    'article_body' : article_body, 
    'article_publish_date' : article_publish_date,
    'article_publish_year' : article_publish_year
    })

    # print(df)
    # Pushing the data to datastore
    check_pushed = datastore_self_defined.datastore_push(df,"Article")
    # print(check_pushed)


    return df
url = "https://www.db.com/api/content/limit/2000/offset/0/render/false/type/json/query/%20+((categories:adHocRelease%20categories:event1%20categories:mediaRelease%20categories:news%20categories:research)%20&&%20(categories:africa%20categories:americas1%20categories:asiapacific%20categories:europeexGermany%20categories:germany%20categories:middleEast%20categories:art%20categories:assetManagement%20categories:awards%20categories:capitalMarkets%20categories:careers%20categories:company1%20categories:corporateCitizenship%20categories:corporateProducts%20categories:cryptocurrencies%20categories:culture%20categories:digitalBankingServices%20categories:digitalisation%20categories:diversity%20categories:education%20categories:employeeEngagement%20categories:entrepreneurship%20categories:financialResults%20categories:history%20categories:investmentBanking%20categories:managementLeadership%20categories:personnelAnnouncements%20categories:privateProducts%20categories:research3%20categories:sports%20categories:strategy%20categories:sustainability%20categories:wealth))%20%20+C03News.publishDate:%5B20150101000000%20to%2020231231235959%5D%20+conhost:8e29bc28-e0f6-40f1-930a-6258631a0985%20+languageId:1%20+deleted:false%20/orderby/C03News.publishDate%20desc"
df = scrape_db(url)