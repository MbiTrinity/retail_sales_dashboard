import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Load the data
df = pd.read_csv('sales_data.csv')

# Convert 'Date' column to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "Retail Sales Dashboard"

# App Layout
app.layout = html.Div([
    html.H1("Retail Sales Dashboard", className="header-title"),
    
    html.Div([
        html.Label("Select Region"),
        dcc.Dropdown(
            id='region-dropdown',
            options=[{'label': region, 'value': region} for region in df['Region'].unique()],
            value='North-West Region',
            multi=False
        )
    ], className='filter-container'),

    html.Div([
        html.Label("Select Product"),
        dcc.Dropdown(
            id='product-dropdown',
            options=[{'label': product, 'value': product} for product in df['Product'].unique()],
            value='Ream of Paper',
            multi=False
        )
    ], className='filter-container'),

    html.Div([
        html.Label("Select Date Range"),
        dcc.DatePickerRange(
            id='date-range',
            start_date=df['Date'].min(),
            end_date=df['Date'].max(),
            display_format='YYYY-MM-DD'
        )
    ], className='filter-container'),

    html.Div([
        dcc.Graph(id='bar-chart'),
        dcc.Graph(id='line-chart'),
        dcc.Graph(id='pie-chart')
    ], className='chart-container')
], className='container')

# Callbacks
@app.callback(
    [Output('bar-chart', 'figure'),
     Output('line-chart', 'figure'),
     Output('pie-chart', 'figure')],
    [Input('region-dropdown', 'value'),
     Input('product-dropdown', 'value'),
     Input('date-range', 'start_date'),
     Input('date-range', 'end_date')]
)
def update_charts(selected_region, selected_product, start_date, end_date):
    filtered_df = df[
        (df['Region'] == selected_region) &
        (df['Product'] == selected_product) &
        (df['Date'] >= pd.to_datetime(start_date)) &
        (df['Date'] <= pd.to_datetime(end_date))
    ]

    bar_fig = px.bar(filtered_df, x='Date', y='Sales', title='Sales Over Time (Bar Chart)')
    line_fig = px.line(filtered_df, x='Date', y='Sales', title='Sales Over Time (Line Chart)')
    pie_fig = px.pie(filtered_df, names='Region', values='Sales', title='Sales Share by Region')

    return bar_fig, line_fig, pie_fig

# Run the app
if __name__ == '__main__':
    import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8050))
    app.run_server(debug=True, host='0.0.0.0', port=port)


