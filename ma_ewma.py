import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from pandas_datareader import data, wb

start = '2017-01-01'
end = '2018-09-20'

<<<<<<< HEAD
df = data.DataReader('NFLX', 'iex', start, end)
df_name = 'Netflix'
=======
tick = tick.upper()
df = data.DataReader(tick, 'iex', start, end)
>>>>>>> d34252c... removed f string from df

app = dash.Dash()
app.title=f'MA vs EWMA: {df_name}'

app.layout = html.Div([
            dcc.Graph(id='main_ma_graph',className='big_graph'),

            html.Div([
                html.H4('MA'),
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
            ],id='slider_ma_div',className='slid_divs')
],id='moad')

app.css.append_css({'external_url': 'https://memakewebsite.com/css/newstyle.css'})

@app.callback(Output('main_ma_graph','figure'),
            [Input('slider_ma','value'),
            Input('slider_ewma','value')])
def update_figure(ma,ewma):
    df['MA'] = df['close'].rolling(window=ma).mean()
    df['EWMA'] = df['close'].ewm(span=ewma).mean()

    data = [go.Scatter(x=df.index,y=df['close'],name=df_name),
            go.Scatter(x=df.index,y=df['MA'],name=f'{ma} MA'),
            go.Scatter(x=df.index,y=df['EWMA'],name=f'{ewma} EWMA')]

    layout = go.Layout(title=f'MA vs EWMA: {df_name}')

    return {'data':data,'layout':layout}

if __name__ == '__main__':
    app.run_server()
