import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from datetime import date

#Uncomment two lines below if: ImportError: cannot import name 'is_list_like
#import pandas as pd
#pd.core.common.is_list_like = pd.api.types.is_list_like
from pandas_datareader import data, wb


tick = 'TSLA'
start = '2017-01-01'
end = date.today()

tick = tick.upper()
df = data.DataReader(tick, 'iex', start, end)

app = dash.Dash()
app.title=f'BBands: {tick}'

app.layout = html.Div([

            dcc.Graph(id='bb_graph',className='big_graph'),
            html.Div([
                html.H4('Bollinger Bands MA'),
                dcc.Slider(id='slider_bband_ma',className='sliders',
                                min=5,
                                max=60,
                                step=1,
                                marks={i: f'{i}' for i in range(5,65,5)},
                                value=20),

                html.H4('Bollinger Bands STD'),
                dcc.Slider(id='slider_bband_std',className='sliders',
                                min=0.2,
                                max=10,
                                step=0.2,
                                marks={i: f'{i}' for i in range(0,10,1)},
                                value=2)


            ],id='slider_ma_div',className='slid_divs'),


],id='moad')
app.css.append_css({'external_url': 'http://memakewebsite.com/css/newstyle.css'})

# Main Graphs
@app.callback(Output('bb_graph','figure'),
            [Input('slider_bband_ma','value'),
            Input('slider_bband_std','value')])
def update_bands(bbma,bbstd):
    df['BBand MA'] = df['close'].rolling(window=bbma).mean()
    df['Upper'] = df['BBand MA'] + bbstd * df['close'].rolling(window=bbma).std()
    df['Lower'] = df['BBand MA'] - bbstd * df['close'].rolling(window=bbma).std()

    data = [go.Scatter(x=df.index,y=df['close'],name=tick),
            go.Scatter(x=df.index,y=df['BBand MA'],name=f'{bbma} MA(BB)'),
            go.Scatter(x=df.index,y=df['Upper'],name='Upper BBand'),
            go.Scatter(x=df.index,y=df['Lower'],name='Lower BBand')]

    layout = go.Layout(title=f'{tick} BOLLINGER BANDS')

    return {'data':data,'layout':layout}

if __name__ == '__main__':
    app.run_server()
