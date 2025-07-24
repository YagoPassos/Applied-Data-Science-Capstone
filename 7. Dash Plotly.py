# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                
                                dcc.Dropdown(id='site-dropdown',
                                             options=[
                                                     {'label': 'All Sites', 'value': 'ALL'},
                                                     {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                     {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                     {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                     {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                                                     ],
                                             value='ALL',
                                             placeholder='Select a Launch Site here',
                                             searchable=True
                                             ),
                                html.Br(),

                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),

                                dcc.RangeSlider(id='payload-slider',
                                                min=0,
                                                max=10000,
                                                step=1000,
                                                marks={0: '0',100: '100'},
                                                value=[min_payload, max_payload]
                                                ),

                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    if (entered_site == 'ALL'):
        fig = px.pie(
        spacex_df,
        names = 'Launch Site',
        title = 'Total Success Launches by Site')
    else:
        fig = px.pie(
        spacex_df.loc[spacex_df['Launch Site'] == entered_site], 
        names = 'class',
        title = f'Total Success Launches for site {entered_site}')
    return fig

# TASK 4:
@app.callback( Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider',component_property='value')])

def get_payload_chart(entered_site, payload_mass):
    if entered_site == 'ALL':
        fig = px.scatter(
            spacex_df[spacex_df['Payload Mass (kg)'].between(payload_mass[0], payload_mass[1])], 
            x="Payload Mass (kg)",
            y="class",
            color="Booster Version Category",
            hover_data=['Launch Site'],
            title='Correlation Between Payload and Success for All Sites')
    else:
        all_launchs = spacex_df[spacex_df['Payload Mass (kg)'].between(payload_mass[0], payload_mass[1])]
        fig = px.scatter(
            all_launchs[all_launchs['Launch Site'] == entered_site],
            x="Payload Mass (kg)",
            y="class",
            color="Booster Version Category",
            hover_data=['Launch Site'],
            title=f'Correlation Between Payload and Success for Site {entered_site}')
    return fig



# Run the app
if __name__ == '__main__':
    app.run()
