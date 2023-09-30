# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
def get_launch_sites():
    launch_sites = spacex_df['Launch Site'].unique()
    tmp = [{'label': 'All Sites', 'value': 'ALL'}]
    for val in launch_sites:
        tmp.append({'label' : val, 'value' : val})
    return tmp

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(
                                    id = 'site-dropdown',
                                    options = get_launch_sites(),
                                    placeholder = 'Select a Launch Site here',
                                    searchable = True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                            marks={0: '0', 100: '100'},
                                            value=[min_payload, max_payload]
                                ),


                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    data = pd.DataFrame()
    if entered_site == 'ALL':
        data['class'] = ['Success', 'Failure']
        data['nb'] = [filtered_df[filtered_df['class'] == 1].shape[0],filtered_df[filtered_df['class'] == 0].shape[0]]
        fig = px.pie(data, values='nb',
        names='class',
        title='Overall Pie Chart'
        )
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        data['class'] = ['Success', 'Failure']
        data['nb'] = [filtered_df[filtered_df['class'] == 1].shape[0],
                      filtered_df[filtered_df['class'] == 0].shape[0]]
        fig = px.pie(
            data,
            values='nb',
            names='class',
            title=f'Pie Chart for {entered_site}' if entered_site != 'ALL' else 'Overall Pie Chart'
        )
    return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")])
def get_scatter_chart(selected_site, payload_range):
    if selected_site == 'ALL':
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
                                (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
        title = 'Payload Mass vs. Class (All Sites)'
    else:
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
                                (spacex_df['Payload Mass (kg)'] <= payload_range[1]) &
                                (spacex_df['Launch Site'] == selected_site)]
        title = f'Payload Mass vs. Class ({selected_site})'

    fig = px.scatter(
        filtered_df,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        title=title
    )

    return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
