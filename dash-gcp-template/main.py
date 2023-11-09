#!/usr/bin/env python
# coding: utf-8
# %%
from plotly.graph_objs import Layout
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Load your data into a DataFrame
df = pd.read_csv('us_chronic_disease_indicators.csv')  # Replace with the path to your actual data file

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    # Components for Question 1
    html.H1("Interactive Chart by Question"),
    dcc.Dropdown(
        id='question1-dropdown',
        options=[{'label': i, 'value': i} for i in df['question'].unique()],
        value=df['question'].unique()[0]
    ),
    dcc.Graph(id='question1-chart'),
    
    # Components for Question 2
    html.H1("Alcohol Use in Youth by State"),
    dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': year, 'value': year} for year in df['yearstart'].unique()],
        value=2019
    ),
    dcc.Graph(id='alcohol-use-chart'),

    # Components for Question 3
    html.H1("Invasive Cancer Incidence Across Race"),
    dcc.Dropdown(
        id='question3-dropdown',
        options=[{'label': i, 'value': i} for i in df[df.datavaluetype == 'Average Annual Crude Rate']['question'].unique()],
        value='Invasive cancer (all sites combined), incidence'
    ),
    dcc.Graph(id='cancer-trend-chart'),

    # Components for Question 4
    html.H1("Obesity Heatmap by Gender and Race"),
    dcc.Dropdown(
        id='gender-dropdown',
        options=[{'label': gender, 'value': gender} for gender in df['stratification1'].unique()],
        value='Overall'
    ),
    dcc.Dropdown(
        id='race-dropdown',
        options=[{'label': race, 'value': race} for race in df['stratification1'].unique()],
        value='Overall'
    ),
    dcc.Graph(id='obesity-heatmap')
])

# Callback for Question 1
@app.callback(
    Output('question1-chart', 'figure'),
    [Input('question1-dropdown', 'value')]
)
def update_question1_chart(selected_question):
    df_filtered = df[(df['question'] == selected_question) & (df['datavaluetypeid'] == 'CRDPREV')]
    fig = px.line(df_filtered, x='yearstart', y='datavalue', color='stratification1', title=selected_question)
    return fig

# Callback for Question 2
@app.callback(
    Output('alcohol-use-chart', 'figure'),
    [Input('year-dropdown', 'value')]
)
def update_alcohol_use_chart(selected_year):
    df_filtered = df[(df['yearstart'] == selected_year) & 
                     (df['question'] == 'Alcohol use among youth') &
                     (~df['locationabbr'].isin(['US', 'PR', 'GU'])) &
                     (df['datavaluetypeid'] == 'CRDPREV')]
    fig = px.bar(df_filtered, x='locationabbr', y='datavalue', title='Alcohol Use Rate in Youth by State')
    return fig

# Callback for Question 3
@app.callback(
    Output('cancer-trend-chart', 'figure'),
    [Input('question3-dropdown', 'value')]
)
def update_cancer_trend(selected_question):
    df_filtered = df[(df['question'] == selected_question) &
                     (df['datavaluetype'] == 'Average Annual Crude Rate') &
                     (df['locationabbr'] == 'US') &
                     (df['stratificationcategory1'] == 'Race/Ethnicity')]
    pivot_df = df_filtered.pivot(index='yearstart', columns='stratification1', values='datavalue')
    fig = px.line(pivot_df, x=pivot_df.index, y=pivot_df.columns, title=selected_question)
    fig.update_layout(xaxis_title='Year', yaxis_title='Average Annual Crude Rate')
    return fig

# Callback for Question 4
@app.callback(
    Output('obesity-heatmap', 'figure'),
    [Input('gender-dropdown', 'value'), Input('race-dropdown', 'value')]
)
def update_obesity_heatmap(selected_gender, selected_race):
    df_filtered = df[(df['question'] == 'Obesity among adults aged >= 18 years') &
                     (df['yearstart'] == 2021) &
                     (df['stratification1'] == selected_gender) &
                     (df['stratificationcategoryid1'] == 'GENDER') &
                     (~df['locationabbr'].isin(['US', 'PR', 'GU'])) &
                     (df['datavaluetypeid'] == 'AGEADJPREV')]
    fig = px.choropleth(df_filtered, locations='locationabbr', locationmode="USA-states", color='datavalue',
                        scope="usa", labels={'datavalue': 'ObesityRate'})
    fig.update_layout(title='Heatmap of Obesity Rate by Gender and Race')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port = 8080)


# %%




