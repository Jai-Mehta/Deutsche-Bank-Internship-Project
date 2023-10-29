import spacy
from spacy import displacy

NER = spacy.load("en_core_web_sm")

import plotly
import pickle
import plotly.express as px
import pandas as pd
import os
import sys
import pycountry

current = os.path.dirname(os.path.realpath(__file__))

parent = os.path.dirname(current)

sys.path.append(parent)
from datastore_self_defined import datastore_get, datastore_vedangi_map_push, datastore_vedangi_map_get


def get_all_banks_data():
	print("getting the data.....")
	df = datastore_get("New_Article")
	print("Got data....")
	df_banks=df[['bank_name','article_body']]
	df_db=df_banks['article_body'].loc[df_banks['bank_name'] == 'Deutsche Bank']
	df_jpmc=df_banks['article_body'].loc[df_banks['bank_name'] == 'JPMorgan Chase & Co']
	df_boa=df_banks['article_body'].loc[df_banks['bank_name'] == 'Bank of America']
	df_pnc=df_banks['article_body'].loc[df_banks['bank_name'] == 'PNC Financial Services']
	df_fidelity=df_banks['article_body'].loc[df_banks['bank_name'] == 'Fidelity']

	return df_db,df_jpmc,df_boa,df_pnc,df_fidelity


def country_codes():
	print("contry codes manipulation...")
	country_list_ame = ['Bahrain','Egypt','Israel','Nigeria','Qatar','Saudi Arabia','Saudi Arabia DSSA','South Africa','Turkey','United Arab Emirates','uae']
	country_list_americas=['Brazil','Canada','Mexico','USA','United States','us']
	country_list_asia_pacific=['Asia Pacific','Australia','China','China - Hong Kong','India','Indonesia','Japan','Kazakhstan','Malaysia','Pakistan','Philippines','Singapore','South Korea','Sri Lanka','Taiwan','Thailand','Taiwan, Province of China','Korea, Republic of','Turkmenistan','Vietnam','Viet Nam']
	country_list_europe=['Austria','Belgium','Bulgaria','Croatia','Czech Republic','Czechia','France','Germany','Greece','Hungary','Ireland','Italy','Jersey','Luxembourg','Netherlands','Poland','Portugal','Romania','Russia','Russian Federation','Serbia','Spain','Sweden','Switzerland','Ukraine','United Kingdom','uk']

	countries = {}

	for country in pycountry.countries:
	    countries[country.name] = country.alpha_3

	ame_codes = [countries.get(country, 'Unknown code') for country in country_list_ame]
	americas_codes = [countries.get(country, 'Unknown code') for country in country_list_americas]
	europe_codes = [countries.get(country, 'Unknown code') for country in country_list_europe]
	asia_pacific_codes = [countries.get(country, 'Unknown code') for country in country_list_asia_pacific]

	country_list_ame = [x.lower() for x in country_list_ame]
	country_list_americas = [x.lower() for x in country_list_americas]
	country_list_asia_pacific = [x.lower() for x in country_list_asia_pacific]
	country_list_europe = [x.lower() for x in country_list_europe]

	return ame_codes, americas_codes, europe_codes, asia_pacific_codes, country_list_ame,country_list_americas ,country_list_asia_pacific ,country_list_europe

def get_ner(df,bankname,fin_df,country_list_ame,country_list_americas ,country_list_asia_pacific ,country_list_europe):
	print("Ner for "+bankname)
	gpe_list_ame = []
	gpe_list_americas = []
	gpe_list_asia_pacific = []
	gpe_list_europe = []
	for row in df:
		rel_entity= NER(str(row))		
		for word in rel_entity.ents:
			if(word.label_ == 'GPE'):
				if word.text in country_list_ame:
					gpe_list_ame.append(word)
				if word.text in country_list_americas:
					gpe_list_americas.append(word)
				if word.text in country_list_asia_pacific:
					gpe_list_asia_pacific.append(word)
				if word.text in country_list_europe:
					gpe_list_europe.append(word)


	allcountries=gpe_list_ame+gpe_list_americas+gpe_list_asia_pacific+gpe_list_europe
	total =  len(gpe_list_ame)+ len(gpe_list_americas)+ len(gpe_list_asia_pacific)+len(gpe_list_europe)
	print(total)
	fin_df.loc[len(fin_df.index)] = [bankname, len(gpe_list_ame)*100//total, len(gpe_list_americas)*100//total, len(gpe_list_asia_pacific)*100//total,len(gpe_list_europe)*100//total,allcountries]

	return fin_df

def create_df_for_maps(db_map_list, ame_score,americas_score,apac_score,eur_score,ame_codes, americas_codes, europe_codes, asia_pacific_codes, bank_name):
	for a in ame_codes:
		db_map_list.append((a,str(ame_score),bank_name))

	for a in americas_codes:
		db_map_list.append((a,str(americas_score),bank_name))

	for a in europe_codes:
		db_map_list.append((a,str(eur_score),bank_name))

	for a in asia_pacific_codes:
		db_map_list.append((a,str(apac_score),bank_name))

	return db_map_list


df_db,df_jpmc,df_boa,df_pnc,df_fidelity = get_all_banks_data()

ame_codes, americas_codes, europe_codes, asia_pacific_codes, country_list_ame,country_list_americas ,country_list_asia_pacific ,country_list_europe = country_codes()

df_map= pd.DataFrame(columns =['bank_name','ame','americas','asia_pacific','europe','allcountries'])


df_map = get_ner(df_db,'Deutsche Bank', df_map,country_list_ame,country_list_americas ,country_list_asia_pacific ,country_list_europe)
df_map = get_ner(df_jpmc,'JPMorgan Chase & Co', df_map,country_list_ame,country_list_americas ,country_list_asia_pacific ,country_list_europe)
df_map = get_ner(df_boa,'Bank of America',df_map,country_list_ame,country_list_americas ,country_list_asia_pacific ,country_list_europe)
df_map = get_ner(df_pnc,'PNC Financial Services',df_map,country_list_ame,country_list_americas ,country_list_asia_pacific ,country_list_europe)
df_map = get_ner(df_fidelity,'Fidelity',df_map,country_list_ame,country_list_americas ,country_list_asia_pacific ,country_list_europe)

l=[]

db_map= create_df_for_maps(l,int(df_map['ame'].loc[df_map['bank_name'] == 'Deutsche Bank']),int(df_map['americas'].loc[df_map['bank_name'] == 'Deutsche Bank']),
                           int(df_map['asia_pacific'].loc[df_map['bank_name'] == 'Deutsche Bank']),int(df_map['europe'].loc[df_map['bank_name'] == 'Deutsche Bank']),
                           ame_codes, americas_codes, europe_codes, asia_pacific_codes,'Deutsche Bank')
jpmc_map= create_df_for_maps(db_map,int(df_map['ame'].loc[df_map['bank_name'] == 'JPMorgan Chase & Co']),int(df_map['americas'].loc[df_map['bank_name'] == 'JPMorgan Chase & Co']),
                           int(df_map['asia_pacific'].loc[df_map['bank_name'] == 'JPMorgan Chase & Co']),int(df_map['europe'].loc[df_map['bank_name'] == 'JPMorgan Chase & Co']),
                           ame_codes, americas_codes, europe_codes, asia_pacific_codes,'JPMorgan Chase & Co')
pnc_map= create_df_for_maps(jpmc_map,int(df_map['ame'].loc[df_map['bank_name'] == 'PNC Financial Services']),int(df_map['americas'].loc[df_map['bank_name'] == 'PNC Financial Services']),
                           int(df_map['asia_pacific'].loc[df_map['bank_name'] == 'PNC Financial Services']),int(df_map['europe'].loc[df_map['bank_name'] == 'PNC Financial Services']),
                           ame_codes, americas_codes, europe_codes, asia_pacific_codes,'PNC Financial Services')
fidelity_map= create_df_for_maps(pnc_map,int(df_map['ame'].loc[df_map['bank_name'] == 'Fidelity']),int(df_map['americas'].loc[df_map['bank_name'] == 'Fidelity']),
                           int(df_map['asia_pacific'].loc[df_map['bank_name'] == 'Fidelity']),int(df_map['europe'].loc[df_map['bank_name'] == 'Fidelity'])
                           ,ame_codes, americas_codes, europe_codes, asia_pacific_codes,'Fidelity')
boa_map=  create_df_for_maps(fidelity_map,int(df_map['ame'].loc[df_map['bank_name'] == 'Bank of America']),int(df_map['americas'].loc[df_map['bank_name'] == 'Bank of America']),
                           int(df_map['asia_pacific'].loc[df_map['bank_name'] == 'Bank of America']),int(df_map['europe'].loc[df_map['bank_name'] == 'Bank of America']),
                           ame_codes, americas_codes, europe_codes, asia_pacific_codes,'Bank of America')

print(boa_map)
all_banks_map= pd.DataFrame(boa_map, columns =['code', 'Score','bank_name'])

print(all_banks_map)

# check_pushed = datastore_vedangi_map_push(all_banks_map)

