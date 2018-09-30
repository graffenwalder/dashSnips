import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from pandas_datareader import data, wb

start = '2017-01-01'
end = '2018-09-20'

<<<<<<< HEAD
df = data.DataReader('TSLA', 'iex', start, end)
df_name = 'TESLA'
=======
tick = tick.upper()
<<<<<<< HEAD
df = data.DataReader(f'{tick}', 'iex', start, end)
>>>>>>> d6a14df... ticktest
=======
df = data.DataReader(tick, 'iex', start, end)
>>>>>>> d34252c... removed f string from df

app = dash.Dash()
app.title=f'BBands: {df_name}'

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
app.css.append_css({'external_url': 'https://memakewebsite.com/css/newstyle.css'})

# Main Graphs
@app.callback(Output('bb_graph','figure'),
            [Input('slider_bband_ma','value'),
            Input('slider_bband_std','value')])
def update_bands(bbma,bbstd):
    df['BBand MA'] = df['close'].rolling(window=bbma).mean()
    df['Upper'] = df['BBand MA'] + bbstd * df['close'].rolling(window=bbma).std()
    df['Lower'] = df['BBand MA'] - bbstd * df['close'].rolling(window=bbma).std()

    data = [go.Scatter(x=df.index,y=df['close'],name=df_name),
            go.Scatter(x=df.index,y=df['BBand MA'],name=f'{bbma} MA(BB)'),
            go.Scatter(x=df.index,y=df['Upper'],name='Upper BBand'),
            go.Scatter(x=df.index,y=df['Lower'],name='Lower BBand')]

    layout = go.Layout(title=f'{df_name} BOLLINGER BANDS')

    return {'data':data,'layout':layout}

if __name__ == '__main__':
    app.run_server()
