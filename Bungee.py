import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression

#線形重回帰による数値予測モデリング

df1 = pd.DataFrame(
    data={'name':['岐阜バンジー','竜神バンジー','五木バンジー','猿ヶ京バンジー','富士バンジー','八ッ場バンジー','みなかみバンジー','開運バンジー','鷲羽山ハイランド','よみうりランド','マザー牧場','南知多グリーンバレイ'],
          'high':[215,100,66,62,54,45,42,30,30,22,21,20],
          'price':[36000,17000,13000,12000,11000,11000,10000,10000,5800,3000,4000,3100]}
)
print(type(df1))
use_data = df1[['name','high','price']]

X = use_data[['high']]
Y = use_data[['price']]

clf = LinearRegression()
clf.fit(X,Y)

#表示するグラフの作成
import plotly.graph_objects as go
from plotly.subplots import make_subplots 

price_plots = make_subplots(rows=1, cols=3, start_cell='bottom-left')
price_plots.add_trace(go.Scatter(x=df1['high'],y=df1['price'],mode='markers',name='high vs price'), row=1,col=1)
price_plots.update_layout(
    xaxis_title_text='High',
    yaxis_title_text='Price (￥)',
)

####アプリ部分
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table
from dash.dependencies import Input, Output, State

app = dash.Dash()

app.layout = html.Div([
    html.H1('バンジージャンプの料金を予測するアプリです！',style={'textAlign':'center'}),
    html.H2('まずは分析に使うデータを見てみましょう！'),
    dash_table.DataTable(
        style_cell={'textAlign':'center','width':'150px'},
        fill_width=False,
        fixed_rows={'headers':True},
        page_size=10,
        filter_action='native',
        sort_action='native',
        columns=[{'name':col,'id':col} for col in df1.columns],
        data=df1.to_dict('recodes')
    ),
    html.P('モデリングに使うのはデータは{}件ですよ！'.format(len(df1))),
    html.H2('次はグラフを見てみましょう！（グラフの要素は固定)'),
    dcc.Graph(
        id='graph',
        figure=price_plots,
        style={}
    ),
    html.H2('予測用のデータをインプットしてみましょう！'),
    dcc.Input(
        id='high',
        placeholder='high ここに値を入れてください',
        type='text',
        style={'width':'20%'},
        value=''
    ),
    html.Button(
        id='submit-button',
        n_clicks=0,
        children='Submit'
    ),
    html.H2('バンジージャンプの予測額はいくらかな？'),
    html.Div(
        id='output-pred',
        style={'textAlign':'center','fontsize':30,'color':'red'}
    )
])
@app.callback(
    Output('output-pred', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State('high','value')]
)
def prediction(n_clicks, high):
    if(high):
        value_df = pd.DataFrame([],columns=['High'])
        record = pd.Series([high], index=value_df.columns, dtype='float64')
        value_df = value_df.append(record, ignore_index=True)
        Y_pred = clf.predict(value_df)
        return_text = '料金はおそらく'+str('{}'.format(Y_pred[0,0])+'円くらいでしょう！！')
        return return_text
    else:
        return 'ちゃんとデータを入力してね！'

if __name__ =='__main__':
    app.run_server()