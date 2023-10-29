

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
from urllib.request import urlopen
import json
with urlopen('https://gist.githubusercontent.com/hrbrmstr/91ea5cc9474286c72838/raw/59421ff9b268ff0929b051ddafafbeb94a4c1910/continents.json') as response:
    continents = json.load(response)
import plotly.express as px


df_maaappppppssss= datastore_vedangi_map_get()

df_maaappppppssss['Score'] = pd.to_numeric(df_maaappppppssss['Score'])
def plot_maps(df,color_scheme):
  fig = px.choropleth(df, geojson=continents, locations='code', color='Score',
                            color_continuous_scale=color_scheme,
                            scope="world",
                            locationmode='ISO-3',
                            title="Regional ESG Presence"
                            )
  fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
  fig.show()

# print(df_maaappppppssss[['code','Score']].loc[df_maaappppppssss['bank_name'] == 'Deutsche Bank'])

plot_maps(df_maaappppppssss[['code','Score']].loc[df_maaappppppssss['bank_name'] == 'Deutsche Bank'],'purples')
plot_maps(df_maaappppppssss[['code','Score']].loc[df_maaappppppssss['bank_name'] == 'JPMorgan Chase & Co'],'reds')
plot_maps(df_maaappppppssss[['code','Score']].loc[df_maaappppppssss['bank_name'] == 'PNC Financial Services'],'algae')
plot_maps(df_maaappppppssss[['code','Score']].loc[df_maaappppppssss['bank_name'] == 'Fidelity'],'ylorbr')
plot_maps(df_maaappppppssss[['code','Score']].loc[df_maaappppppssss['bank_name'] == 'Bank of America'],'amp')