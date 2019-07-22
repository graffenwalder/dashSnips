import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans

app = dash.Dash()
app.title='K-Means Clustering'

app.layout = html.Div([

            html.Div([
            html.H4('K-Means Clusters'),
            dcc.Slider(id='slider_kmeans_clusters',className='sliders',
                            min=1,
                            max=10,
                            step=1,
                            marks={i: f'{i}' for i in range(1,11,1)},
                            value=4)
            ],id='slider_kmeans_div',className='slid_divs'),

            html.Div([
            dcc.Graph(id='kmeans_graph',className='big_graph',
                        relayoutData = {'autorange': True}),
            dcc.Graph(id='know_label_graph',className='big_graph',
                        relayoutData = {'autorange': True})
            ],id='graphs_div'),

            html.Div([
                html.H3('Set Original'),
                html.H4('Samples'),
                dcc.Slider(id='slider_known_samples',className='sliders',
                            min=100,
                            max=950,
                            step=25,
                            marks={i: f'{i}' for i in range(100,1000,50)},
                            value=300),

                html.H4('Centers'),
                dcc.Slider(id='slider_known_centers',className='sliders',
                                min=1,
                                max=10,
                                step=1,
                                marks={i: f'{i}' for i in range(1,11,1)},
                                value=4),

                html.H4('Standard Deviation'),
                dcc.Slider(id='slider_known_std',className='sliders',
                                min=0.1,
                                max=5,
                                step=0.1,
                                marks={i: f'{i}' for i in range(0,6,1)},
                                value=1.8),

                html.H4('Random State'),
                dcc.Slider(id='slider_known_randstate',className='sliders',
                            min=1,
                            max=120,
                            step=1,
                            marks={i: f'{i}' for i in range(0,121,10)},
                            value=101),

            ],id='slider_known_div',className='slid_divs'),

],id='moad')
app.css.append_css({'external_url': 'http://growpi.net/css/kmeans.css'})

@app.callback(Output('kmeans_graph','figure'),
            [Input('slider_known_samples','value'),
            Input('slider_known_centers','value'),
            Input('slider_known_std','value'),
            Input('slider_known_randstate','value'),
            Input('slider_kmeans_clusters','value'),
            Input('know_label_graph', 'relayoutData')])
def update_kmeans(samps,centers,std,randstate,kcluster,relay):
    blob_data = make_blobs(n_samples=samps, n_features=2,\
    centers=centers, cluster_std=std,random_state=randstate)

    kmeans = KMeans(n_clusters=kcluster)
    kmeans.fit(blob_data[0])

    data = [go.Scatter(x=blob_data[0][:,0],
                        y=blob_data[0][:,1],
                        mode='markers',
                        marker= dict(color= kmeans.labels_,
                                    colorscale='Viridis'))]

    if 'xaxis.range[0]' in relay and 'yaxis.range[0]' in relay:
        layout = go.Layout(title= 'Kmeans Clustering',
                    hovermode= 'closest',
                    margin=go.layout.Margin(l=50,r=50,b=50,t=100,pad=4),
                    xaxis=dict(zeroline=False,
                    autorange=False,
                    range= [relay['xaxis.range[0]'], relay['xaxis.range[1]']]),
                    yaxis=dict(zeroline=False,
                    autorange=False,
                    range= [relay['yaxis.range[0]'], relay['yaxis.range[1]']]))

    elif 'xaxis.range[0]' in relay:
        layout = go.Layout(title= 'Kmeans Clustering',
                    hovermode= 'closest',
                    margin=go.layout.Margin(l=50,r=50,b=50,t=100,pad=4),
                    xaxis=dict(zeroline=False,
                    autorange=False,
                    range= [relay['xaxis.range[0]'], relay['xaxis.range[1]']]),
                    yaxis=dict(zeroline=False))

    elif 'yaxis.range[0]' in relay:
        layout = go.Layout(title= 'Kmeans Clustering',
                    hovermode= 'closest',
                    margin=go.layout.Margin(l=50,r=50,b=50,t=100,pad=4),
                    xaxis=dict(zeroline=False),
                    yaxis=dict(zeroline=False,
                    autorange=False,
                    range= [relay['yaxis.range[0]'], relay['yaxis.range[1]']]))

    else:
        layout = go.Layout(title= 'Kmeans Clustering',
                    hovermode= 'closest',
                    margin=go.layout.Margin(l=50,r=50,b=50,t=100,pad=4),
                    xaxis=dict(zeroline=False),
                    yaxis=dict(zeroline=False))

    return {'data':data,'layout':layout}

@app.callback(Output('know_label_graph','figure'),
            [Input('slider_known_samples','value'),
            Input('slider_known_centers','value'),
            Input('slider_known_std','value'),
            Input('slider_known_randstate','value'),
            Input('kmeans_graph', 'relayoutData')])
def update_known(samps,centers,std,randstate,relay):
    blob_data = make_blobs(n_samples=samps, n_features=2,\
    centers=centers, cluster_std=std,random_state=randstate)

    data = [go.Scatter(x=blob_data[0][:,0],
                        y=blob_data[0][:,1],
                        mode='markers',
                        marker= dict(color= blob_data[1],
                                    colorscale='Viridis'))]

    if 'xaxis.range[0]' in relay and 'yaxis.range[0]' in relay:
        layout = go.Layout(title= 'Original (known labes)',
                    hovermode= 'closest',
                    margin=go.layout.Margin(l=50,r=50,b=50,t=100,pad=4),
                    xaxis=dict(zeroline=False,
                    autorange=False,
                    range= [relay['xaxis.range[0]'], relay['xaxis.range[1]']]),
                    yaxis=dict(zeroline=False,
                    autorange=False,
                    range= [relay['yaxis.range[0]'], relay['yaxis.range[1]']]))

    elif 'xaxis.range[0]' in relay:
        layout = go.Layout(title= 'Original (known labes)',
                    hovermode= 'closest',
                    margin=go.layout.Margin(l=50,r=50,b=50,t=100,pad=4),
                    xaxis=dict(zeroline=False,
                    autorange=False,
                    range= [relay['xaxis.range[0]'], relay['xaxis.range[1]']]),
                    yaxis=dict(zeroline=False))

    elif 'yaxis.range[0]' in relay:
        layout = go.Layout(title= 'Original (known labes)',
                    hovermode= 'closest',
                    margin=go.layout.Margin(l=50,r=50,b=50,t=100,pad=4),
                    xaxis=dict(zeroline=False),
                    yaxis=dict(zeroline=False,
                    autorange=False,
                    range= [relay['yaxis.range[0]'], relay['yaxis.range[1]']]))

    else:
        layout = go.Layout(title= 'Original (known labes)',
                    hovermode= 'closest',
                    margin=go.layout.Margin(l=50,r=50,b=50,t=100,pad=4),
                    xaxis=dict(zeroline=False),
                    yaxis=dict(zeroline=False))

    return {'data':data,'layout':layout}

if __name__ == '__main__':
    app.run_server()
