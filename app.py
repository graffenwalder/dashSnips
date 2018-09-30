import json
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from datetime import date
import requests
import quandl
#quandl.ApiConfig.api_key = 'XXXXXXX'

start = '2017-01-01'
end = date.today()

df = quandl.get("BCHAIN/MKPRU",start_date= start)
df.columns = ['Price']
df_name = 'BTC'

#Functions
def get_stamp_price(market):
    '''
    get_stamp_price('ltcusd') ==> LTC: 55.66 USD,     -1.35%
    '''
    r = requests.get(f'https://www.bitstamp.net/api/v2/ticker/{market}/')
    x = r.json()
    return f"{market[:3].upper()}: {x['last']} {market[3:].upper()}, \
    {(((float(x['last']) / float(x['open'])) -1) * 100):.2f}%"

#layout for 2 main graphs
layout = go.Layout(title=df_name,
            autosize=False,
            #width=800,
            #height=500,
            margin=go.layout.Margin(l=45,r=10,b=50,t=70,pad=4),
            legend=dict(orientation="h",y=-0.2))

app = dash.Dash()
app.title='Crypto Dashboard'

app.layout = html.Div([
            dcc.Graph(id='main_ma_graph',className='big_graph'),

            html.Div([
                html.H4('SMA'),
                dcc.Slider(id='slider_ma',className='sliders',
                            min=10,
                            max=200,
                            step=5,
                            marks={i: f'{i}' for i in range(10,210,10)},
                            value=30),
                html.H4('EWMA'),
                dcc.Slider(id='slider_ewma',className='sliders',
                            min=10,
                            max=200,
                            step=5,
                            marks={i: f'{i}' for i in range(10,210,10)},
                            value=45)
            ],id='slider_ma_div',className='slid_divs'),

            dcc.Graph(id='bb_graph',className='big_graph'),
            html.Div([
                html.H4('Bollinger Bands'),
                dcc.Slider(id='slider_bband',className='sliders',
                                min=5,
                                max=60,
                                step=1,
                                marks={i: f'{i}' for i in range(5,65,5)},
                                value=20)
            ],id='slider_bb_div',className='slid_divs'),

            html.Div([
            dcc.Graph(id='rsi_main',
                    relayoutData = {'xaxis.range[0]': start,
                                    'xaxis.range[1]': end}),
            dcc.Graph(id='rsi_graph',
                    relayoutData = {'xaxis.range[0]': start,
                                    'xaxis.range[1]': end}),
            ],id='rsi_graphs_div'),

            html.Div([
                html.H4('RSI'),
                dcc.Slider(id='slider_rsi',className='sliders',
                                min=5,
                                max=60,
                                step=1,
                                marks={i: f'{i}' for i in range(5,65,5)},
                                value=14)
            ],id='slider_rsi_div',className='slid_divs'),

            html.Div([
            html.Div(id='widget1',className='widgets'),
            html.Div(id='widget2',className='widgets'),
            html.Div(id='widget3',className='widgets'),
            ],id='widget_div'),

            html.Button(id='submit_widget',
                        n_clicks=0,
                        children='Update Widgets'),

            html.Div([dcc.Markdown(id='mark_stats')],
            id='mark_div'),
            html.Button(id='stats_submit',
                        n_clicks=0,
                        children='Update Stats'),

            dcc.Interval(id='widget_interval',
                        interval=5 *60 *1000,# *1000 for seconds, *60 for minutes
                        n_intervals=0)
],id='moad')
app.css.append_css({'external_url': 'http://memakewebsite.com/css/newstyle.css'})

# Main Graphs
@app.callback(Output('main_ma_graph','figure'),
            [Input('slider_ma','value'),
            Input('slider_ewma','value')])
def update_figure(ma,ewma):
    df['MA'] = df['Price'].rolling(window=ma).mean()
    df['EWMA'] = df['Price'].ewm(span=ewma).mean()

    data = [go.Scatter(x=df.index,y=df['Price'],name=df_name),
            go.Scatter(x=df.index,y=df['MA'],name=f'{ma} MA'),
            go.Scatter(x=df.index,y=df['EWMA'],name=f'{ewma} EWMA')]

    return {'data':data,'layout':layout}

@app.callback(Output('bb_graph','figure'),
            [Input('slider_bband','value')])
def update_bands(bband):
    df['BBand MA'] = df['Price'].rolling(window=bband).mean()
    df['Upper'] = df['BBand MA'] + 2 * df['Price'].rolling(window=bband).std()
    df['Lower'] = df['BBand MA'] - 2 * df['Price'].rolling(window=bband).std()

    data = [go.Scatter(x=df.index,y=df['Price'],name=df_name),
            go.Scatter(x=df.index,y=df['BBand MA'],name=f'{bband} MA(BB)'),
            go.Scatter(x=df.index,y=df['Upper'],name='Upper BBand'),
            go.Scatter(x=df.index,y=df['Lower'],name='Lower BBand')]

    return {'data':data,'layout':layout}

@app.callback(Output('rsi_graph','figure'),
            [Input('slider_rsi','value'),
            Input('rsi_main', 'relayoutData')])
def update_rsi(rsi,m_relay):
    df['Up']=df['Price'].diff().apply(lambda x:x if x>0 else 0)
    df['Down']=df['Price'].diff().apply(lambda x:-x if x<0 else 0)
    df['UpAvg']=df['Up'].rolling(window=rsi).mean()
    df['DownAvg']=df['Down'].rolling(window=rsi).mean()
    df['RSI']=100-(100/(1+df['UpAvg']/df['DownAvg']))

    data = [go.Scatter(x=df.index,y=df['RSI'],name=f'{rsi} period RSI')]

    if 'xaxis.range[0]' in m_relay:
        layout = go.Layout(autosize=False,height=150,
                margin=go.layout.Margin(l=45,r=10,b=50,t=10,pad=4),
                xaxis=dict(
                    autorange=False,
                    range= [m_relay['xaxis.range[0]'], m_relay['xaxis.range[1]']],
                    ))
    else:
        layout = go.Layout(autosize=False,height=150,
                margin=go.layout.Margin(l=45,r=10,b=50,t=10,pad=4))

    return {'data':data,'layout':layout}


@app.callback(Output('rsi_main','figure'),
            [Input('rsi_graph', 'relayoutData')])
def update_rsmain(r_relay):
    data = [go.Scatter(x=df.index,y=df['Price'],name=f'{df_name} RSI')]

    if 'xaxis.range[0]' in r_relay:
        layout = go.Layout(title= f'{df_name} RSI',
                autosize=False,height=400,
                margin=go.layout.Margin(l=45,r=10,b=23,t=70,pad=4),
                xaxis=dict(
                    autorange=False,
                    range= [r_relay['xaxis.range[0]'], r_relay['xaxis.range[1]']],
                    zeroline=False,
                    showline=False,
                    ticks='',
                    showticklabels=False))
    else:
        layout = go.Layout(title= f'{df_name} RSI',
            autosize=False,height=400,
            margin=go.layout.Margin(l=45,r=10,b=23,t=70,pad=4),
            xaxis=dict(
                zeroline=False,
                showline=False,
                ticks='',
                showticklabels=False))

    return {'data':data,'layout':layout}

# Widgets
#stamp_options = [None, 'btcusd', 'btceur', 'eurusd', 'xrpusd', 'xrpeur',
# 'xrpbtc', 'ltcusd', 'ltceur', 'ltcbtc', 'ethusd', 'etheur', 'ethbtc',
# 'bchusd', 'bcheur', 'bchbtc']

@app.callback(Output('widget1','children'),
                [Input('submit_widget','n_clicks'),
                Input('widget_interval','n_intervals')])
def widg1(biba,bobo):
    return get_stamp_price('btcusd')

@app.callback(Output('widget2','children'),
                [Input('submit_widget','n_clicks'),
                Input('widget_interval','n_intervals')])
def widg2(biba,bobo):
    return get_stamp_price('ethusd')

@app.callback(Output('widget3','children'),
                [Input('submit_widget','n_clicks'),
                Input('widget_interval','n_intervals')])
def widg3(biba,bobo):
    return get_stamp_price('ltcusd')

@app.callback(Output('mark_stats','children'),
                [Input('stats_submit','n_clicks'),
                Input('widget_interval','n_intervals')])
def total_crypto(merry,christmas):
    r = requests.get('https://api.coinmarketcap.com/v2/global/')
    data = r.json()["data"]

    return f'''
    Active Crypto\'s:\t{data["active_cryptocurrencies"]}\t\t\
    Total MarketCap:\t$ {data["quotes"]["USD"]["total_market_cap"]/1000000000} billion
	Active Markets:\t\t{data["active_markets"]}\t\t\
    Total Volume 24h:\t$ {data["quotes"]["USD"]["total_volume_24h"]/1000000000} billion
	Bitcoin Dominance:\t{data["bitcoin_percentage_of_market_cap"]}%
    '''

if __name__ == '__main__':
    app.run_server()
