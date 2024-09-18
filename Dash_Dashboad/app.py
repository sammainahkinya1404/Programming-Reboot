import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# Sample data
data = {'Year': [2010, 2011, 2012, 2013, 2014],
        'Sales': [100, 150, 200, 250, 300]}

df = pd.DataFrame(data)

# Creating a Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Sales Dashboard'),
    dcc.Graph(
        id='line-chart',
        figure=px.line(df, x='Year', y='Sales', title='Sales Over Time')
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
