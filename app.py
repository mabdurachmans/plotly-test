import os
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
from urllib.request import urlopen
import json
import requests



app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
app.title = 'Covid19 Jawa Barat'
server = app.server


blackbold={'color':'black', 'font-weight': 'bold'}

#retrieving covid data in west java, Indonesia
url = 'https://covid19-public.digitalservice.id/api/v1/sebaran/jabar'
res = requests.get(url)
df_map = pd.DataFrame(res.json()['data']['content'])
# df_map = pd.read_csv("jabar.csv")

token = open(".mapbox_token").read()


df_map['nama_kab']=df_map['nama_kab'].str.title()
df_map['nama_kab']=df_map['nama_kab'].str.replace('Kab.','Kabupaten', regex=False)
df_map['nama_kab']=df_map['nama_kab'].str.replace('Bandung Barat','Bandung', regex=False)
df_map['nama_kec']=df_map['nama_kec'].str.title()
df_map['nama_kel']=df_map['nama_kel'].str.title()
df_map['color'] = df_map['status'].replace({'ODP': 'lightsalmon', 'OTG': 'blue', 'PDP': 'purple', 'Positif': 'indianred'})
# df_map.to_csv('df_map.csv')

app.layout = html.Div(
    html.Div([

# title
        html.Div([
            html.H1(children='Persebaran Kasus Covid19 di Jawa Barat',
                style={#'font-family': 'Helvetica',
                       "margin-top": "25",
                       "margin-bottom": "0"},
                className='nine columns'),
        ], className="row"),

# map
        html.Div([
            html.Div([
                dcc.Graph(
                    id='covid-map', config={'displayModeBar': False, 'scrollZoom': True},
                )
            ], className='seven columns'),

# Kota/Kabupaten dropdown
            html.Div([
                html.Label(children=['Kota/Kabupaten: '], style=blackbold),
                    dcc.Dropdown(id='drop-down_kab',
                            options=[{'label':str(b),'value':b} for b in sorted(df_map['nama_kab'].unique())],
                            value=[b for b in sorted(df_map['nama_kab'].unique())],
                            placeholder="Pilih Kota/Kabupaten",
                            multi=True,
                    ),
# Status dropdown
                html.Label(children=['Status: '], style=blackbold),
                    dcc.Dropdown(id='drop-down_status',
                            options=[{'label':str(b),'value':b} for b in sorted(df_map['status'].unique())],
                            value=[],#[b for b in sorted(df_map['status'].unique())],
                            placeholder="Pilih Status",
                            multi=True,
                    ),

#source link    
                html.Br(),
                    dcc.Link('Sumber Data', href='https://covid19-public.digitalservice.id/api/v1/sebaran/jabar', target="_blank"),
            ], className='five columns'),
        ], className="row"),

# graph
        html.Div([
            html.Div([
                dcc.Graph(
                    id='graph1', config={'displayModeBar': False},
                )
            ], className='twelve columns'),
        ], className="row")

    ], className='ten columns offset-by-one')
)

#---------------------------------------------------------------
# Output of Graph
@app.callback(
    Output("covid-map", "figure"),
    [Input("drop-down_kab", "value"),
    Input("drop-down_status", "value")])

def update_figure(chosen_kab,chosen_status):
    df_sub = df_map[(df_map['nama_kab'].isin(chosen_kab)) &
                (df_map['status'].isin(chosen_status))]

    # Create figure
    locations=[go.Scattermapbox(
                    lon = df_sub['longitude'],
                    lat = df_sub['latitude'],
                    mode='markers',
                    unselected={'marker' : {'opacity':1}},
                    selected={'marker' : {'opacity':0.5, 'size':25}},
                    marker={'color' : df_sub['color']},
                    hovertext=df_sub['nama_kec'],
    )]

    # Return figure
    return {
        'data': locations,
        'layout': go.Layout(
            uirevision= 'foo', #preserves state of figure/map after callback activated
            height=600,
            margin=dict(
                l=0,
                r=15,
                b=35,
                t=20),
            clickmode= 'event+select',
            hovermode='closest',
            hoverdistance=2,
            mapbox=dict(
                accesstoken=token,
                # bearing=25,
                style='light',
                center=dict(
                    lat=-6.9175, 
                    lon=107.6191,
                ),
                pitch=20,
                zoom=8
            ),
        )
    }

#---------------------------------------------------------------
# callback for Web_link
@app.callback(
    Output('graph1', 'figure'),
    [Input('covid-map', 'clickData'),#])
    Input("drop-down_status", "value")])
def display_click_data(clickData,chosen_status):
    if clickData is None:
        df_drop = df_map[(df_map['status'].isin(chosen_status))]
        layout = go.Layout(
            bargap=0.5,
            # bargroupgap=0.15,
            barmode='stack',
            # margin=Margin(l=50, r=10, t=0, b=100),
            showlegend=False,
            # height=250,
            xaxis=dict(
                showgrid=False,
                # nticks=50,
                # fixedrange=False,
                tickangle=-45,
                categoryorder='category ascending'
            ),
            yaxis=dict(
                showticklabels=False,
                showgrid=False,
                # fixedrange=False,
                rangemode='nonnegative',
                # zeroline='hidden'
            )
        )

        data = go.Bar(
                 x=df_drop['nama_kab'],
                 y=df_drop['status'],
                 # marker = {'color': color_scale(df_click)},
                 hovertext=df_drop['nama_kec'],
                 marker_color = df_drop['color'],
             )
        return go.Figure(data=data, layout=layout)
    else:
        # print(clickData)
        clickkecamatan = clickData['points'][0]['hovertext']
        clickkabupaten = df_map[df_map['nama_kec']==clickkecamatan]['nama_kab'].iloc[0]
        df_click = df_map[df_map['nama_kab'].isin([clickkabupaten]) &
                         (df_map['status'].isin(chosen_status))]
        # print(clickkabupaten)
        layout = go.Layout(
            bargap=0.5,
            # bargroupgap=0.15,
            barmode='stack',
            # margin=Margin(l=50, r=10, t=0, b=100),
            showlegend=False,
            # height=250,
            # dragmode="select",
            xaxis=dict(
                showgrid=False,
                # nticks=50,
                # fixedrange=False,
                tickangle=-45,
                categoryorder='category ascending'
            ),
            yaxis=dict(
                showticklabels=False,
                showgrid=False,
                # fixedrange=False,
                rangemode='nonnegative',
                # zeroline='hidden'
            )
        )

        data = go.Bar(
                 x=df_click['nama_kec'],
                 y=df_click['status'],
                 hovertext=df_click['nama_kel'],
                 marker_color = df_click['color'],
             )
    return go.Figure(data=data, layout=layout)

#---------------------------------------------------------------


if __name__ == '__main__':
    app.run_server(debug=True)