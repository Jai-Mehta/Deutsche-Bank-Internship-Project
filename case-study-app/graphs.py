import plotly.express as px
import pandas as pd
from datastore_self_defined import *
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from urllib.request import urlopen
import json
with urlopen('https://gist.githubusercontent.com/hrbrmstr/91ea5cc9474286c72838/raw/59421ff9b268ff0929b051ddafafbeb94a4c1910/continents.json') as response:
    continents = json.load(response)


'''File contain only plots get methods'''

def display_histogram():
    """Displays Rishav's histogram graph"""
    df_score = datastore_rishav_histogram_get()    
    fig = px.histogram(
        df_score,
        x="Bank Name",
        y="Score",
        color="Keyword",
        labels={'Bank Name':'Bank Name','Score':'Score','Keyword':'Common Keywords'},
        title="Score for Keyword per Bank"
    )
    return fig

def display_icicle():
    '''Icicle graph of all keywords used under E,S and G'''
    df = pd.DataFrame({
         'child':['Environment','Social','Governance',
                  'Climate Change','Emmission', 'Resource Use', 'Fuel', 'Minerals', 'Pandemics', 'Pollution', 'Extraction Desertification', 'Air Quality', 'Drinkable Water',
                  'LGBTQ+','Equality', 'Diversity', 'Innovation', 'Community', 'Human Rights', 'Refugees', 'Racism', 'Gender Equality', 'Mental Health',
                  'Management','Payment', 'Shareholder', 'Workforce', 'Shares', 'Corruption', 'Tax', 'Laundering', 'Fraud', 'Rate Fixing'],
         'parent':['Keywords','Keywords','Keywords',
                   'Environment','Environment', 'Environment','Environment', 'Environment','Environment', 'Environment','Environment', 'Environment','Environment',
                   'Social','Social', 'Social','Social', 'Social','Social', 'Social','Social', 'Social','Social',
                   'Governance','Governance', 'Governance','Governance', 'Governance','Governance', 'Governance','Governance', 'Governance','Governance'],
         'values':[1,1,1,
                   1,1,1,1,1,1,1,1,1,1,
                   1,1,1,1,1,1,1,1,1,1,
                   1,1,1,1,1,1,1,1,1,1]
    })
    fig = px.icicle(
         df,
         names='child',
         parents='parent',
         values='values',
         title="Commonly Used Keywords for ESG"
    )
    fig.update_traces(root_color="lightgrey")
    return fig


def create_radial_gauge_chart(key, val, scores):
    fig = go.Figure(go.Indicator(
    domain = {'x': [0, 1], 'y': [0, 1]},
    value = val,
    mode = "gauge+number+delta",
    title = {'text': key},
    delta = {'reference': scores["Deutsche Bank"]},
    gauge = {'axis': {'range': [0, 5]},
            'bar': {'color': "#0047ab"},
            'steps' : [{'range': [0, 1.5], 'color': "#E97451"},{'range': [1.5, 3], 'color': "#FFFF8F"},{'range': [3, 5], 'color': "#50C878"}]}
            ))
    return fig


def plot_radial_gauge(input_passed):
    scores = datastore_jai_radial_get(input_passed,kind_passed="Data_Radial_Gauge_Chart")
    fig = make_subplots(rows=1, cols=5,
                        specs=[[{"type": "indicator"}, {"type": "indicator"},{"type": "indicator"},{"type": "indicator"}, {"type": "indicator"}]])
    row = 1
    col = 1
    gauge_chart = create_radial_gauge_chart('Deutsche Bank', scores['Deutsche Bank'], scores)
    # fig.add_trace(gauge_chart.data, row=row, col=col)
    for trace in gauge_chart.data:
            fig.add_trace(trace, row=row, col=col)
    col+=1
    for key,value in scores.items():
        if key=='Deutsche Bank':
            continue
        gauge_chart = create_radial_gauge_chart(key, value, scores)
        for trace in gauge_chart.data:
            fig.add_trace(trace, row=row, col=col)
        col += 1

    # Update layout for better visualization
    fig.update_layout(
        height=400,
        width=1200,
        title="Sentiment Score for Keyword '" + input_passed + "'"
        # title_text="Radial Gauge Charts"
    )

    # fig.show()
    return fig


def return_time_series(Keyword):
    df = datastore_diya_time_series_get()

    # words = ["Emission", "Environment", "Resource Use", "Climate Change", "Diversity", "Innovation","Community", "Social", "Shareholder",  "Governance", "Management", "Workforce"]
    
    # for word in words:
    #     word_df = df[df["Keyword"] == word]
    #     year_df = word_df.sort_values('Year')
    #     fig = px.line(year_df, x="Year", y="Score", color="Bank Name",markers=True,title="Time Series for "+word,)
    #     plotly.offline.plot(fig)
    year_df = df[df["Year"] >= '2014']
    word_df = year_df[year_df["Keyword"] == Keyword]
    year_df = word_df.sort_values('Year')
    fig = px.line(year_df, x="Year", y="Score", color="Bank Name",markers=True,title="Average Yearly Sentiment for Keyword '"+Keyword+"'",)
    # plotly.offline.plot(fig)
        
    return fig

def return_maps(bank_name):
    df= datastore_vedangi_map_get()
    df['Score'] = pd.to_numeric(df['Score'])

    if(bank_name=='JPMorgan Chase & Co'):
        df_map= df[['code','Score']].loc[df['bank_name'] == 'JPMorgan Chase & Co']
        color_scheme = 'YlGnBu'
    elif(bank_name== 'PNC Financial Services'):
        df_map=df[['code','Score']].loc[df['bank_name'] == 'PNC Financial Services']
        color_scheme='greens'
    elif(bank_name=='Fidelity'):
        df_map = df[['code','Score']].loc[df['bank_name'] == 'Fidelity']
        color_scheme='YlOrRd'
    elif(bank_name=='Bank of America'):
        df_map=df[['code','Score']].loc[df['bank_name'] == 'Bank of America']
        color_scheme='reds'    
    else:
        df_map = df[['code','Score']].loc[df['bank_name'] == 'Deutsche Bank']
        color_scheme='RdPu'    

    fig = px.choropleth(df_map, geojson=continents, locations='code', color='Score',
                            color_continuous_scale=color_scheme,
                            scope="world",
                            locationmode='ISO-3'
                            )
    fig.update_layout(
        margin={"r":0,"t":40,"l":0,"b":20},
        title="Regional ESG Presence for " + bank_name
    )
    # fig.show()
    return fig       

# sco = datastore_jai_radial_get("Corporate Tax",kind_passed="Data_Radial_Gauge_Chart")
# print(sco)
# plot = plot_radial_gauge("Corporate Tax")
# plot.show()

def display_pie_chart(bank):
    df = datastore_jack_pie_chart_get()
    vals = df.loc[df['bank'] == bank].iloc[0]
    
    fig = px.pie(
        values=list(vals)[1:],
        names=['Environmental', 'Social', 'Governance'],
        # title=bank,
        height=300,
        width=300
    )
    fig['layout'] = go.Layout(
        margin=dict(t=0,b=0,l=0,r=0),
        showlegend=False
    )
    # fig['layout']['title'] = bank
    
    return fig


# sco = datastore_jai_radial_get("Corporate Tax",kind_passed="Data_Radial_Gauge_Chart")
# print(sco)
# plot = plot_radial_gauge(sco)
# plot.show()
