from dash import Input, Output, State, dcc, html, Dash, ALL, State, callback_context
import pandas as pd
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import random
import json
import requests
from bs4 import BeautifulSoup
import time

external_stylesheets = [dbc.themes.DARKLY]
load_figure_template('darkly')

movies4 = pd.read_csv('movies4.csv')
genometags = pd.read_csv('archive/genome-tags.csv')
genomescores = pd.read_csv('archive/genome-scores.csv')

toptags = list(genometags[genometags['tagId'].isin(genomescores.groupby('tagId').mean().sort_values(by='relevance', ascending=False)[:40].index)]['tagId'])

genres = ['Adventure', 'Animation', 'Children', 'Comedy', 'Fantasy',
       'Romance', 'Action', 'Crime', 'Thriller', 'Drama', 'Horror',
       'Mystery', 'Sci-Fi', 'War', 'Musical', 'Documentary', 'IMAX',
       'Western', 'Film-Noir']

app = Dash(__name__, external_stylesheets=external_stylesheets)
#from app import app

page1 = dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader('Popular or Not?'),
                dbc.CardBody([
                    dbc.Button('Popular', id='choice1a', n_clicks_timestamp=0, style={'width':'50%', 'backgroundColor':'#012345', 'margin':'20px', 'padding':'10px', 'justify-content':'center', 'align-items':'center'}),
                    dbc.Button('Not', id='choice1b', n_clicks_timestamp=0, style={'width':'50%', 'backgroundColor':'#012345', 'margin':'20px', 'padding':'10px', 'justify-content':'center', 'align-items':'center'})
                ], style={'display':'flex', 'width':'100%'})
            ], style={'height':'50vh'})
        ], sm=12, md=12, lg=8),
    ], justify='center', align='center', style={'height':'100vh'})

page2 = dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader('What is your minimum required rating?'),
                dbc.CardBody([
                    dbc.Button('4*', id='choice2a', n_clicks_timestamp=0, style={'width':'50%', 'backgroundColor':'#012345', 'margin':'20px', 'padding':'10px', 'justify-content':'center', 'align-items':'center'}),
                    dbc.Button('3*', id='choice2b', n_clicks_timestamp=0, style={'width':'50%', 'backgroundColor':'#012345', 'margin':'20px', 'padding':'10px', 'justify-content':'center', 'align-items':'center'})
                ], style={'display':'flex', 'width':'100%'})
            ], style={'height':'50vh'})
        ], sm=10, md=10, lg=8),
    ], justify='center', align='center', style={'height':'100vh'})

page3 = dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader('Modern?'),
                dbc.CardBody([
                    dbc.Button('Yes', id='choice3a', n_clicks_timestamp=0, style={'width':'50%', 'backgroundColor':'#012345', 'margin':'20px', 'padding':'10px', 'justify-content':'center', 'align-items':'center'}),
                    dbc.Button('No', id='choice3b', n_clicks_timestamp=0, style={'width':'50%', 'backgroundColor':'#012345', 'margin':'20px', 'padding':'10px', 'justify-content':'center', 'align-items':'center'})
                ], style={'display':'flex', 'width':'100%'})
            ], style={'height':'50vh'})
        ], sm=10, md=10, lg=8),
    ], justify='center', align='center', style={'height':'100vh'})

page4 = dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader('How Important Is This?'),
                html.P(id='choice4_title'),
                dbc.CardBody([
                    dbc.Button(children='Very', id='choice4a', n_clicks_timestamp=0, style={'width':'25%', 'backgroundColor':'#012345', 'margin':'20px', 'padding':'10px', 'justify-content':'center', 'align-items':'center'}),
                    dbc.Button(children='Quite', id='choice4b', n_clicks_timestamp=0, style={'width':'25%', 'backgroundColor':'#012345', 'margin':'20px', 'padding':'10px', 'justify-content':'center', 'align-items':'center'}),
                    dbc.Button(children='Not Much', id='choice4c', n_clicks_timestamp=0, style={'width':'25%', 'backgroundColor':'#012345', 'margin':'20px', 'padding':'10px', 'justify-content':'center', 'align-items':'center'}),
                    dbc.Button(children='Not At All', id='choice4d', n_clicks_timestamp=0, style={'width':'25%', 'backgroundColor':'#012345', 'margin':'20px', 'padding':'10px', 'justify-content':'center', 'align-items':'center'})
                ], style={'display':'flex', 'width':'100%'})
            ], style={'height':'50vh'})
        ], sm=10, md=10, lg=8),
    ], justify='center', align='center', style={'height':'100vh'})

page5 = dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader('Which other genre?'),
                dbc.CardBody([
                    dbc.Button(id='choice5a', n_clicks_timestamp=0, style={'width':'50%', 'backgroundColor':'#012345', 'margin':'20px', 'padding':'10px', 'justify-content':'center', 'align-items':'center'}),
                    dbc.Button(id='choice5b', n_clicks_timestamp=0, style={'width':'50%', 'backgroundColor':'#012345', 'margin':'20px', 'padding':'10px', 'justify-content':'center', 'align-items':'center'})
                ], style={'display':'flex', 'width':'100%'})
            ], style={'height':'50vh'})
        ], sm=10, md=10, lg=8),
    ], justify='center', align='center', style={'height':'100vh'})

page6 = dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader('How Important Is This?'),
                html.P(id='choice6_title'),
                dbc.CardBody([
                    dbc.Button(children='Very', id='choice6a', n_clicks_timestamp=0, style={'width':'25%', 'backgroundColor':'#012345', 'margin':'20px', 'padding':'10px', 'justify-content':'center', 'align-items':'center'}),
                    dbc.Button(children='Quite', id='choice6b', n_clicks_timestamp=0, style={'width':'25%', 'backgroundColor':'#012345', 'margin':'20px', 'padding':'10px', 'justify-content':'center', 'align-items':'center'}),
                    dbc.Button(children='Not Much', id='choice6c', n_clicks_timestamp=0, style={'width':'25%', 'backgroundColor':'#012345', 'margin':'20px', 'padding':'10px', 'justify-content':'center', 'align-items':'center'}),
                    dbc.Button(children='Not At All', id='choice6d', n_clicks_timestamp=0, style={'width':'25%', 'backgroundColor':'#012345', 'margin':'20px', 'padding':'10px', 'justify-content':'center', 'align-items':'center'})
                ], style={'display':'flex', 'width':'100%'})
            ], style={'height':'50vh'})
        ], sm=10, md=10, lg=8),
    ], justify='center', align='center', style={'height':'100vh'})




app.layout = dbc.Container([
    
    dcc.Store(id='store'),
    dcc.Store(id='store2'),
    dcc.Store(id='store3'),
    dcc.Store(id='store4'),
    dcc.Store(id='store5'),
    dcc.Store(id='store6'),
    dbc.Tabs(
            [
                dbc.Tab(label="Tab 1", tab_id="tab-1", children=[page1]),
                dbc.Tab(label="Tab 2", tab_id="tab-2", children=[page2]),
                dbc.Tab(label="Tab 3", tab_id="tab-3", children=[page3]),
                dbc.Tab(label="Tab 4", tab_id="tab-4", children=[page4]),
                dbc.Tab(label="Tab 5", tab_id="tab-5", children=[page5]),
                dbc.Tab(label="Tab 6", tab_id="tab-6", children=[page6]),
                dbc.Tab(label="Tab 7", tab_id="tab-7", children=[dbc.Row([dbc.Col([dbc.ListGroup(id='list-group')], sm=12, md=12, lg=6),dbc.Col([html.Div(id='tab7')], sm=12, md=12, lg=6)])])
            ],
            id="tabs",
            active_tab="tab-1",
        ),
        html.Div(id="content"),
    html.Div(id='temp1'),
    html.Div(id='temp2'),
    html.Div(id='temp3'),
    html.Div(id='temp4'),
    html.Div(id='temp5'),
    html.Div(id='temp6'),
    html.Div(dbc.Button('Try Again', id='button_reset_movies', n_clicks=0, n_clicks_timestamp=0))
    
])

@app.callback(
    Output("tabs", "active_tab"),
    [Input('temp1', 'children'),
    Input('temp2', 'children'),
    Input('temp3', 'children'),
    Input('temp4', 'children'),
    Input('temp5', 'children'),
    Input('temp6', 'children')]
)
def switch_tab(data1,data2,data3,data4,data5,data6):
    if data6:
        return 'tab-7'
    elif data5:
        return 'tab-6'
    elif data4:
        return 'tab-5'
    elif data3:
        return 'tab-4'
    elif data2:
        return 'tab-3'
    elif data1:
        return 'tab-2'
    else:
        return 'tab-1'
            
    
@app.callback(
    [Output('choice4_title', 'children'),
    Output('choice5a', 'children'),
     Output('choice5b', 'children'),
    Output('choice6_title', 'children')],
    Input('button_reset_movies', 'n_clicks')
)
def reset(btn5a):
    return genometags[genometags['tagId']==toptags[random.randint(0,39)]]['tag'].item(), genres[random.randint(0,9)], genres[random.randint(10,18)], genometags[genometags['tagId']==toptags[random.randint(0,39)]]['tag'].item()

@app.callback(
    Output('store', 'data'),
    [Input('choice1a', 'n_clicks_timestamp'),
     Input('choice1b', 'n_clicks_timestamp'),
    Input('button_reset_movies', 'n_clicks_timestamp')]
)
def update_state(n1a,n1b,x):
    choices = []
    if n1a > n1b:
        choices.append(5000)
        choices.append(100000)
    elif n1b > n1a:
        choices.append(0)
        choices.append(3000)
    if x > n1a|n1b:
        choices = []
    return choices

@app.callback(
    Output('store2', 'data'),
    [Input('choice2a', 'n_clicks_timestamp'),
     Input('choice2b', 'n_clicks_timestamp'),
    Input('button_reset_movies', 'n_clicks_timestamp')]
)
def update_state2(n2a,n2b,x):
    choices = []
    if n2a > n2b:
        choices.append(4)
        choices.append(5.1)
    elif n2b > n2a:
        choices.append(3)
        choices.append(5.1)
    if x > n2a|n2b:
        choices = []
    return choices

@app.callback(
    Output('store3', 'data'),
    [Input('choice3a', 'n_clicks_timestamp'),
     Input('choice3b', 'n_clicks_timestamp'),
    Input('button_reset_movies', 'n_clicks_timestamp')]
)
def update_state3(n3a,n3b,x):
    choices = []
    if n3a > n3b:
        choices.append(1995)
        choices.append(2025)
    elif n3b > n3a:
        choices.append(0)
        choices.append(1995)
    if x > n3a|n3b:
        choices = []
    return choices

@app.callback(
    Output('store4', 'data'),
    [Input('choice4a', 'n_clicks_timestamp'),
     Input('choice4b', 'n_clicks_timestamp'),
    Input('choice4c', 'n_clicks_timestamp'),
    Input('choice4d', 'n_clicks_timestamp'),
    Input('button_reset_movies', 'n_clicks_timestamp')],
    State('choice4_title', 'children')
)
def update_state4(n4a,n4b,n4c,n4d,x,title):
    choices = []
    if n4a > n4b|n4c|n4d:
        choices.append(title)
        choices.append(0.7)
    elif n4b > n4a|n4c|n4d:
        choices.append(title)
        choices.append(0.5)
    elif n4c > n4b|n4a|n4d:
        choices.append(title)
        choices.append(0.3)
    elif n4d > n4b|n4c|n4a:
        choices.append(title)
        choices.append(0.1)
    if x > n4a|n4b|n4c|n4d:
        choices = []
    return choices

@app.callback(
    Output('store5', 'data'),
    [Input('choice5a', 'n_clicks_timestamp'),
     Input('choice5b', 'n_clicks_timestamp'),
    Input('button_reset_movies', 'n_clicks_timestamp')],
    [State('choice5a', 'children'),
     State('choice5b', 'children')]
)
def update_state5(n5a,n5b,x,name1,name2):
    choices = []
    if n5a > n5b:
        choices.append(name1)
    elif n5b > n5a:
        choices.append(name2)
    if x > n5a|n5b:
        choices = []
    return choices

@app.callback(
    Output('store6', 'data'),
    [Input('choice6a', 'n_clicks_timestamp'),
     Input('choice6b', 'n_clicks_timestamp'),
    Input('choice6c', 'n_clicks_timestamp'),
    Input('choice6d', 'n_clicks_timestamp'),
    Input('button_reset_movies', 'n_clicks_timestamp')],
    State('choice6_title', 'children')
)
def update_state6(n6a,n6b,n6c,n6d,x,title):
    choices = []
    if n6a > n6b|n6c|n6d:
        choices.append(title)
        choices.append(0.7)
    elif n6b > n6a|n6c|n6d:
        choices.append(title)
        choices.append(0.5)
    elif n6c > n6b|n6a|n6d:
        choices.append(title)
        choices.append(0.3)
    elif n6d > n6b|n6c|n6a:
        choices.append(title)
        choices.append(0.1)
    if x > n6a|n6b|n6c|n6d:
        choices = []
    return choices

@app.callback(
    Output('temp1', 'children'),
    Input('store', 'data')
)
def update_temp(data):
    return data

@app.callback(
    Output('temp2', 'children'),
    Input('store2', 'data')
)
def update_temp2(data):
    return data

@app.callback(
    Output('temp3', 'children'),
    Input('store3', 'data')
)
def update_temp3(data):
    return data

@app.callback(
    Output('temp4', 'children'),
    Input('store4', 'data')
)
def update_temp4(data):
    return data

@app.callback(
    Output('temp5', 'children'),
    Input('store5', 'data')
)
def update_temp5(data):
    return data

@app.callback(
    Output('temp6', 'children'),
    Input('store6', 'data')
)
def update_temp6(data):
    return data

@app.callback(
    Output('list-group', 'children'),
    [Input('store6', 'data')],
    [State('store', 'data'),
     State('store2', 'data'),
    State('store3', 'data'),
    State('store4', 'data'),
    State('store5', 'data')]
)
def update_tab7(data6,data1,data2,data3,data4,data5):
    if data6:
        # tag number for tag
        tag = data4[0]
        a = genometags[genometags['tag']==tag]['tagId'].item()
        # movies with that tag
        b = genomescores[genomescores['tagId']==a]
        # movieId for that tag (over 0.9)
        c = b[b['relevance']>data4[1]]['movieId'].values
        # movies
        choices = data1
        choices.extend(data2)
        choices.extend(data3)
        choices.extend([c])
        choices.extend(data5)
        tag = data6[0]
        a = genometags[genometags['tag']==tag]['tagId'].item()
        b = genomescores[genomescores['tagId']==a]
        c = b[b['relevance']>data6[1]]['movieId'].values
        choices.extend([c])
        #return choices[0]
        df = movies4[(movies4['no_of_ratings']>choices[0])&(movies4['no_of_ratings']<choices[1])&(movies4['rating']>choices[2])&(movies4['rating']<choices[3])&(movies4['year']>choices[4])&(movies4['year']<choices[5])&(movies4['movieId'].isin(choices[6]))&(movies4['genres'].str.contains(choices[7]))&(movies4['movieId'].isin(choices[8]))].reset_index(drop=True)
        return [dbc.ListGroupItem(
            df['title'][i], 
            id={"type": "list-group-item", "index": i}, 
            action=True
        )
        for i in range(len(df))]
    else:
        return ''
    
@app.callback(
    Output("tab7", "children"),
    Input({'type': 'list-group-item', 'index': ALL}, 'n_clicks'),
    State("list-group", "children"),
    prevent_initial_call=True
)
def update(n_clicks_list, children):
    clicked_id = callback_context.triggered[0]["prop_id"]
    # Parsing it 
    clicked_id = int(json.loads(clicked_id.split(".")[0])["index"])
    movie = str(children[clicked_id]['props']['children']).replace(', The', '')
    page = requests.get('https://www.justwatch.com/uk/search?q='+movie)
    soup = BeautifulSoup(page.content)
    alpha = soup.find('div', 'price-comparison__grid__row__holder').find_all('div', 'price-comparison__grid__row__element')
    beta = [alpha[x].find('img')['title'] for x in range(len(alpha))]
    image = soup.find('div', 'title-poster').find('img')['src']
    link = 'https://www.justwatch.com'+soup.find('a', 'title-list-row__column-header')['href']
    page2 = requests.get(link)
    soup2 = BeautifulSoup(page2.content)
    text = soup2.find('p', 'text-wrap-pre-line mt-0').text
    return [html.Img(src=image), 
            html.H3(movie), 
            html.P(text), 
            dcc.RadioItems(options=[{'label':i, 'value':i} for i in [soup2.find_all('div', 'detail-infos')[x].text for x in range(len(soup2.find_all('div', 'detail-infos')))][:4]], labelStyle={'display': 'block', 'cursor': 'pointer'}),
            html.P(dcc.Link(href=link)),
            dcc.RadioItems(options=[{'label':i, 'value':i} for i in beta], labelStyle={'display':'block'})]

if __name__=='__main__':
    app.run_server(debug=True, port=8060)