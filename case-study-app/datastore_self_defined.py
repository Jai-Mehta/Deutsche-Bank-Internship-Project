from google.cloud import datastore
import os
import pandas as pd
import json
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"

def datastore_push(df, kind_passed):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"
    datastore_client = datastore.Client()
    # The kind for the new entity. This is so all 'Sentences' can be queried.
    # kind = "Article"
    kind = "New_Article"
    # Create a key to store into datastore
    key = datastore_client.key(kind)
    for ind in range(len(df)):
        entity = datastore.Entity(key, exclude_from_indexes=("bank_name","url","article_title","article_body","article_publish_date","article_publish_year"))
        entity["bank_name"] = df.iloc[ind]["bank_name"] 
        entity["url"] = df.iloc[ind]["url"] 
        entity["article_title"] = df.iloc[ind]["article_title"] 
        entity["article_body"] = df.iloc[ind]["article_body"] 
        entity["article_publish_date"] = df.iloc[ind]["article_publish_date"]
        entity["article_publish_year"] = df.iloc[ind]["article_publish_year"]
        datastore_client.put(entity)
        print(ind)
    print("All the data from " + df.iloc[ind]["bank_name"] + " has been pushed to datastore!")
    return "All the data from " + df.iloc[ind]["bank_name"] + " has been pushed to datastore!"

def datastore_get(kind_passed):
    """
    This GET request will return all the texts and sentiments that have been POSTed previously.
    """
    # Create a Cloud Datastore client.
    kind_passed = "New_Article"
    datastore_client = datastore.Client()

    # Get the datastore 'kind' which are 'Sentences'
    # query = datastore_client.query(kind="Article")
    query = datastore_client.query(kind=kind_passed)
    text_entities = list(query.fetch())

    bank_name = []
    url = []
    article_title = []
    article_body = []
    article_publish_date = []
    article_publish_year = []

    for ele in text_entities:
        bank_name.append(ele["bank_name"])
        url.append(ele["url"])
        article_title.append(ele["article_title"])
        article_body.append(ele["article_body"])
        article_publish_date.append(ele["article_publish_date"])
        article_publish_year.append(ele["article_publish_year"])

    df = pd.DataFrame({
        'bank_name' : bank_name, 
        'url' : url, 
        'article_title' : article_title, 
        'article_body' : article_body, 
        'article_publish_date' : article_publish_date,
        'article_publish_year' : article_publish_year
        })

    return df

def datastore_response_push(df):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"
    datastore_client = datastore.Client()
    # The kind for the new entity. This is so all 'Sentences' can be queried.
    # kind = "Article"
    kind = 'Response'
    # Create a key to store into datastore
    key = datastore_client.key(kind)
    for ind in range(len(df)):
        entity = datastore.Entity(key, exclude_from_indexes=("index", "nlp_response","bank_name","url","article_title","article_body","article_publish_date","article_publish_year"))
        entity["index"] = str(df.iloc[ind]["index"] )
        nlp_response = df.iloc[ind]["nlp_response"]
        nlp_response_json = nlp_response.__class__.to_json(nlp_response)
        entity["nlp_response"] = json.dumps(nlp_response_json)
        entity["bank_name"] = df.iloc[ind]["bank_name"] 
        entity["url"] = df.iloc[ind]["url"] 
        entity["article_title"] = df.iloc[ind]["article_title"] 
        entity["article_body"] = df.iloc[ind]["article_body"] 
        entity["article_publish_date"] = df.iloc[ind]["article_publish_date"]
        entity["article_publish_year"] = df.iloc[ind]["article_publish_year"]
        datastore_client.put(entity)
    print("All the nlp response data has been pushed to datastore!")
    return "All the nlp response data has been pushed to datastore!"


def datastore_response_get():
    """
    This GET request will return all the texts and sentiments that have been POSTed previously for "Response" table
    """
    # Create a Cloud Datastore client.
    datastore_client = datastore.Client()

    # Get the datastore 'kind' which are 'Sentences'
    # query = datastore_client.query(kind="Article")
    query = datastore_client.query(kind='Response')
    text_entities = list(query.fetch())

    index = []
    nlp_response = []
    bank_name = []
    url = []
    article_title = []
    article_body = []
    article_publish_date = []
    article_publish_year = []

    for ele in text_entities:
        index.append(ele["index"])
        nlp_response.append(json.loads(json.loads(ele["nlp_response"])))
        bank_name.append(ele["bank_name"])
        url.append(ele["url"])
        article_title.append(ele["article_title"])
        article_body.append(ele["article_body"])
        article_publish_date.append(ele["article_publish_date"])
        article_publish_year.append(ele["article_publish_year"])

    df = pd.DataFrame({
        'index' : index, 
        'nlp_response' : nlp_response,
        'bank_name' : bank_name, 
        'url' : url, 
        'article_title' : article_title, 
        'article_body' : article_body, 
        'article_publish_date' : article_publish_date,
        'article_publish_year' : article_publish_year
    })

    return df

def datastore_rishav_histogram_push(df):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"
    datastore_client = datastore.Client()
    # The kind for the new entity. This is so all 'Sentences' can be queried.
    # kind = "Article"
    kind = 'Histogram'
    # Create a key to store into datastore
    key = datastore_client.key(kind)
    for ind in range(len(df)):
        entity = datastore.Entity(key, exclude_from_indexes=("Bank Name", "Keyword","Score"))
        entity["Bank Name"] = df.iloc[ind]["Bank Name"] 
        entity["Keyword"] = df.iloc[ind]["Keyword"] 
        entity["Score"] = df.iloc[ind]["Score"] 
        datastore_client.put(entity)
    print("All the histogram data has been pushed to datastore!")
    return "All the histogram data has been pushed to datastore!"


def datastore_rishav_histogram_get():
    """
    This GET request will return all the texts and sentiments that have been POSTed previously for rishav's histogram.
    """
    # Create a Cloud Datastore client.
    datastore_client = datastore.Client()
    kind_passed = 'Histogram'
    # Get the datastore 'kind' which are 'Sentences'
    # query = datastore_client.query(kind="Article")
    query = datastore_client.query(kind=kind_passed)
    text_entities = list(query.fetch())

    bank_name = []
    keyword = []
    score = []

    for ele in text_entities:
        bank_name.append(ele["Bank Name"])
        keyword.append(ele["Keyword"])
        score.append(ele["Score"])

    df = pd.DataFrame({
        'Bank Name' : bank_name, 
        'Keyword' : keyword,
        'Score': score
    })

    return df



def datastore_diya_time_series_push(df):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"
    datastore_client = datastore.Client()
    # The kind for the new entity. This is so all 'Sentences' can be queried.
    # kind = "Article"
    kind = 'TimeSeries'
    # Create a key to store into datastore
    key = datastore_client.key(kind)
    for ind in range(len(df)):
        entity = datastore.Entity(key, exclude_from_indexes=("Year", "Bank Name", "Keyword","Score"))
        entity["Year"] = df.iloc[ind]["Year"] 
        entity["Bank Name"] = df.iloc[ind]["Bank Name"] 
        entity["Keyword"] = df.iloc[ind]["Keyword"] 
        entity["Score"] = df.iloc[ind]["Score"] 
        datastore_client.put(entity)
    print("All the time series data has been pushed to datastore!")
    return "All the time series data has been pushed to datastore!"


def datastore_diya_time_series_get():
    """
    This GET request will return all the texts and sentiments that have been POSTed previously for rishav's histogram.
    """
    # Create a Cloud Datastore client.
    datastore_client = datastore.Client()
    kind_passed = 'TimeSeries'
    # Get the datastore 'kind' which are 'Sentences'
    # query = datastore_client.query(kind="Article")
    query = datastore_client.query(kind=kind_passed)
    text_entities = list(query.fetch())
    
    year = []
    bank_name = []
    keyword = []
    score = []

    for ele in text_entities:
        year.append(ele["Year"])
        bank_name.append(ele["Bank Name"])
        keyword.append(ele["Keyword"])
        score.append(ele["Score"])

    df = pd.DataFrame({
        'Year': year,
        'Bank Name' : bank_name, 
        'Keyword' : keyword,
        'Score': score
    })

    return df



def datastore_jack_pie_chart_push(df):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"
    datastore_client = datastore.Client()
    
    kind = 'PieChart'
    key = datastore_client.key(kind)

    for ind in range(len(df)):
        entity = datastore.Entity(key, exclude_from_indexes=("bank", "environmental","social", "governance"))
        entity["bank"] = df.iloc[ind]["bank"] 
        entity["environmental"] = df.iloc[ind]["environmental"] 
        entity["social"] = df.iloc[ind]["social"]
        entity["governance"] = df.iloc[ind]["governance"] 
        datastore_client.put(entity)

    print("All the histogram data has been pushed to datastore!")
    return "All the histogram data has been pushed to datastore!"



def datastore_jack_pie_chart_get():
    datastore_client = datastore.Client()
    kind_passed = 'PieChart'

    query = datastore_client.query(kind=kind_passed)
    text_entities = list(query.fetch())

    banks = []
    environmental = []
    social = []
    governance = []

    for ele in text_entities:
        banks.append(ele["bank"])
        environmental.append(ele["environmental"])
        social.append(ele["social"])
        governance.append(ele["governance"])

    df = pd.DataFrame({
        'bank': banks,
        'environmental': environmental,
        'social': social,
        'governance': governance
    })

    return df


def datastore_jai_radial_push(df, bank_names, words, kind_passed = "Data_Radial_Gauge_Chart"):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"
    datastore_client = datastore.Client()
    # The kind for the new entity. This is so all 'Sentences' can be queried.
    # kind = "Article"
    kind = kind_passed
    # Create a key to store into datastore
    key = datastore_client.key(kind)
    for bank in bank_names:
        entity = datastore.Entity(key, exclude_from_indexes=('Environment', 'Emissions', 'Resource Use', 'Innovation', 'Social', 'Human Rights', 'Product Responsibility', 'Workforce', 'Community', 'Governance', 'Management', 'Shareholders', 'CSR Strategy', 'Racial Justice', 'Disability', 'LGBT+ Inclusion', 'Vulnerable Communities Worker Safety', 'Refugees', 'Inequality', 'Human Trafficking', 'Access In Work Poverty', 'Conflict Minerals', 'Forced Labor', 'Migration Child Labor', 'Education', 'Human Rights', 'Freedom of Assembly', 'Skills', 'Alcohol Abuse', 'Just Transition', 'Healthcare', 'Access to Justice', 'Drug Pricing', 'Gambling', 'Labor Relations', 'AI / Automation', 'Future of Work', 'Health', 'Addiction', 'Fake News', 'Anti microbial Resistance', 'Mental Health', 'Food Safety', 'Disinformation', 'Pandemics', 'Burnout', 'Sugar', 'Food Substance Misuse', 'Workplace health Nutrition Hunger', 'Living Wage Digital Inclusion', 'Financial Inclusion', 'Working Conditions', 'Gender Equality', 'Diversity', 'Waste', 'Climate Change', 'Biodiversity', 'Water', 'Resource Use', 'Recycling', 'Ecotoxicity', 'Ocean Plastic', 'Food Waste', 'Circular Economy', 'Rare Earths', 'Pollution', 'Extraction Desertification', 'Water Scarcity Air Quality', 'Soil', 'Drinkable Water', 'Soil Acidification', 'Crop Yields', 'Pesticides', 'Regenerative Agriculture', 'Fertilizers', 'Clean Energy', 'Bee Fertility', 'Net Zero', 'Climate Adaptation', 'Floods', 'Carbon Emissions', 'Conservation', 'Animal Welfare', 'Mass Extinction', 'Ecosystem Collapse', 'Over fishing', 'Deforestation', 'Sea Level Rises', 'Ocean Acidification', 'Topsoil Loss', 'Discrimination', 'Conduct', 'Board', 'Remuneration', 'Data', 'Tax', 'Homophobia', 'Money Laundering', 'Corruption', 'Transparency', 'Sexism', 'Workplace Conduct', 'Financial Crime', 'Racism', 'Inappropriate Behavior', 'Bullying', 'Anti trust Mis selling', 'Harassment', 'Transphobia', 'Rate Fixing', 'Oversight', 'Bribery', 'Fraud', 'Composition', 'Criminal Misconduct', 'Data Misuse', 'Capacity and Competency', 'Privacy', 'Corporate Tax', 'Data Stewardship', 'Tax Avoidance', 'Bonuses Dividends', 'Share Buybacks', 'CEO Pay'))
        entity["bank_name"] = bank
        for word in words:
            entity[word] = str(df.loc[bank][word])
        # print(entity)
        datastore_client.put(entity)
    print("Radial Gauge Chart scores have been pushed to Datastore with the kind as Data_Radial_Gauge_Chart!")




def datastore_vedangi_map_push(df):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"
    datastore_client = datastore.Client()
    
    kind = 'Maps'
    key = datastore_client.key(kind)

    for ind in range(len(df)):
        entity = datastore.Entity(key, exclude_from_indexes=("code","Score","bank_name"))
        entity["code"] = df.iloc[ind]["code"] 
        entity["Score"] = df.iloc[ind]["Score"]
        entity["bank_name"] = df.iloc[ind]["bank_name"] 
        datastore_client.put(entity)

    print("All the Maps data has been pushed to datastore!")
    return "All the Maps data has been pushed to datastore!"
 

def datastore_vedangi_map_get():
    datastore_client = datastore.Client()
    kind_passed = 'Maps'

    query = datastore_client.query(kind=kind_passed)
    text_entities = list(query.fetch())

    bank_name = []
    code = []
    Score = []

    for ele in text_entities:
        code.append(ele["code"])
        Score.append(ele["Score"])
        bank_name.append(ele["bank_name"])

    df = pd.DataFrame({
        'code': code,
        'Score': Score,
        'bank_name': bank_name
    })

    return df

def datastore_jai_radial_get(input_passed,kind_passed="Data_Radial_Gauge_Chart"):
    """
    This GET request will return all the texts and sentiments that have been POSTed previously.
    """
    # Create a Cloud Datastore client.
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"
    kind_passed = "Data_Radial_Gauge_Chart"
    datastore_client = datastore.Client()
    query = datastore_client.query(kind=kind_passed)
    text_entities = list(query.fetch())
    scores = {}
    for ele in text_entities:
        scores[ele["bank_name"]] = float(ele[input_passed])
    return scores