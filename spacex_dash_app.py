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

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                 # TASK 1: Add a dropdown list to enable Launch Site selection
                                 # The default select value is for ALL sites
                                   dcc.Dropdown(id='site-dropdown',
                                              options=[
                                                    {'label': 'All Sites', 'value': 'ALL'},
                                                    {'label': 'site1', 'value': 'site1'},],
                                              value='ALL',
                                              placeholder="Select a Launch Site here",
                                              searchable=True
                                              )],
                                              html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                # Function decorator to specify function input and output

                                @app.callback(
                                    Output(component_id='success-pie-chart', component_property='figure'),
                                     Input(component_id='site-dropdown', component_property='value'))
                                def get_pie_chart(entered_site):
                                    filtered_df = spacex_df
                                    if entered_site == 'ALL':
                                        fig = px.pie(data, values='class', 
                                        names='pie chart names', 
                                        title='title')
                                        return fig
                                    else:
                                        # return the outcomes piechart for a selected site
                                               html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0',
                                                       100: '100'},
                                                value=[min_value, max_value])

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                

# TASK 3:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def update_scatter_chart(selected_site, payload_range):
    # Filter data based on payload range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) & 
                            (spacex_df['Payload Mass (kg)'] <= payload_range[1])]

    # Check if 'ALL' sites are selected
    if selected_site == 'ALL':
        fig = px.scatter(
            filtered_df, x='Payload Mass (kg)', y='class',
            color='Booster Version Category',
            title='Payload vs. Outcome for All Sites'
        )
    else:
        # Filter data for the selected site
        site_df = filtered_df[filtered_df['Launch Site'] == selected_site]
        fig = px.scatter(
            site_df, x='Payload Mass (kg)', y='class',
            color='Booster Version Category',
            title=f'Payload vs. Outcome for {selected_site}'
        )

    return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
