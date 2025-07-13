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

site_options = [{'label': 'All Sites', 'value': 'ALL'}] + \
               [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()]
# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                        # TASK 1: Add a dropdown list to enable Launch Site selection
                                        # The default select value is for ALL sites
                                        # dcc.Dropdown(id='site-dropdown',...)
                                        dcc.Dropdown(id='site-dropdown',
                                                    options=site_options,
                                                    value='ALL',
                                                    placeholder="Select a Launch Site",
                                                    searchable=True),
                                        html.Br(),
        
                                        # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                        # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                        html.Div(dcc.Graph(id='success-pie-chart')),
                                        html.Br(),
        
                                        html.P("Payload range (Kg):"),
                                        # TASK 3: Add a slider to select payload range
                                        #dcc.RangeSlider(id='payload-slider',...)
                                        dcc.RangeSlider(id='payload-slider',
                                                        min=min_payload,
                                                        max=max_payload,
                                                        step=1000,
                                                        value=[min_payload, max_payload],
                                                        marks={int(min_payload): str(int(min_payload)),
                                                        int(max_payload): str(int(max_payload))}),
                                        # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                        html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                        ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        fig = px.pie(spacex_df, names='Launch Site', 
                     values='class',
                     title='Total Success Launches by Site')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        success_counts = filtered_df['class'].value_counts().reset_index()
        success_counts.columns = ['class', 'count']
        success_counts['class'] = success_counts['class'].map({1: 'Success', 0: 'Failure'})
        fig = px.pie(success_counts, names='class', values='count',
                     title=f'Success vs Failure for {selected_site}')
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)

def update_scatter_chart(selected_site, payload_range):
    low, high = payload_range
    df_filtered = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) &
                            (spacex_df['Payload Mass (kg)'] <= high)]
    
    if selected_site != 'ALL':
        df_filtered = df_filtered[df_filtered['Launch Site'] == selected_site]
    
    fig = px.scatter(df_filtered,
                     x='Payload Mass (kg)', y='class',
                     color='Booster Version Category',
                     title='Payload vs. Outcome Correlation')
    return fig
	
	
# Run the app
if __name__ == '__main__':
    app.run()
