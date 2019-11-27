import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
import altair as alt
import vega_datasets

app = dash.Dash(__name__, assets_folder='assets')
app.config['suppress_callback_exceptions'] = True

server = app.server
app.title = 'Dash app with pure Altair HTML'


#Load and Prepare Data

initial_df = pd.read_csv('https://raw.githubusercontent.com/UBC-MDS/DSCI_532_Group102_No_Suicide_Squad/master/data/SD_data_information.csv', index_col=0, parse_dates=True).reset_index()
continent_df = pd.read_excel('https://github.com/UBC-MDS/DSCI_532_Group102_No_Suicide_Squad/blob/master/data/countryContinent_data_excel.xlsx?raw=true')
final_df = initial_df.merge(continent_df, on='country', how='left')
final_df = final_df.drop(['country-year', ' gdp_for_year ($) ','HDI for year', 'code_2','country_code','region_code','sub_region_code'],axis=1)
final_df = final_df.rename(columns={'gdp_per_capita ($)': 'gdp_per_capita_usd', 'code_3': 'country_code_name','suicides/100k pop':'suicides_per_100k_pop'})
plot_a_data = final_df.query('suicides_per_100k_pop>0.1').query('year < 2015 and year > 1986').groupby(['year','continent'],as_index = False).agg({"suicides_per_100k_pop":"mean","country":"nunique"})

#End Data Preparation

def make_plot(xval = 'Displacement'):

    def mds_special():
        font = "Arial"
        axisColor = "#000000"
        gridColor = "#DEDDDD"
        return {
            "config": {
                "title": {
                    "fontSize": 24,
                    "font": font,
                    "anchor": "start", # equivalent of left-aligned.
                    "fontColor": "#000000"
                },
                'view': {
                    "height": 300, 
                    "width": 400
                },
                "axisX": {
                    "domain": True,
                    #"domainColor": axisColor,
                    "gridColor": gridColor,
                    "domainWidth": 1,
                    "grid": False,
                    "labelFont": font,
                    "labelFontSize": 12,
                    "labelAngle": 0, 
                    "tickColor": axisColor,
                    "tickSize": 5, # default, including it just to show you can change it
                    "titleFont": font,
                    "titleFontSize": 16,
                    "titlePadding": 10, # guessing, not specified in styleguide
                    "title": "X Axis Title (units)", 
                },
                "axisY": {
                    "domain": False,
                    "grid": True,
                    "gridColor": gridColor,
                    "gridWidth": 1,
                    "labelFont": font,
                    "labelFontSize": 14,
                    "labelAngle": 0, 
                    #"ticks": False, # even if you don't have a "domain" you need to turn these off.
                    "titleFont": font,
                    "titleFontSize": 16,
                    "titlePadding": 10, # guessing, not specified in styleguide
                    "title": "Y Axis Title (units)", 
                    # titles are by default vertical left of axis so we need to hack this 
                    #"titleAngle": 0, # horizontal
                    #"titleY": -10, # move it up
                    #"titleX": 18, # move it to the right so it aligns with the labels 
                },
            }
                }

    # register the custom theme under a chosen name
    alt.themes.register('mds_special', mds_special)

    # enable the newly registered theme
    alt.themes.enable('mds_special')
    #alt.themes.enable('none') # to return to default

    # Create a plot A
    source = plot_a_data.round(1)

    nearest = alt.selection(type='single', nearest=True, on='mouseover',
                        fields=['year'], empty='none')
    line= alt.Chart(source).mark_line(point=True).encode(
        x = alt.X('year:O',axis=alt.Axis(title='Date:Year')),
        y = alt.Y('suicides_per_100k_pop',axis=alt.Axis(title='Suicides per 100 k pop'),scale=alt.Scale(zero=False)),
        color='continent'
    ).properties(
        width=500,
        height=200,
        title='Suicide Rate per Continent'
    )
    selectors = alt.Chart(source).mark_point().encode(
        x='year:O',
        opacity=alt.value(0),
    ).add_selection(
        nearest
    )
    points = line.mark_point().encode(
        opacity=alt.condition(nearest, alt.value(1), alt.value(0))
    )
    text = line.mark_text(align='left', dx=5, dy=-5).encode(
        text=alt.condition(nearest, 'suicides_per_100k_pop', alt.value(' '))
    )
    rules = alt.Chart(source).mark_rule(color='gray').encode(
        x='year:O',
    ).transform_filter(
        nearest
    )
    chart_A = alt.layer(
        line, selectors, points, rules, text
    ).properties(
        width=600, height=300
    )        

    return chart_A


def make_plot_B(selected_region = 'Select a Region Please'):

    def mds_special():
        font = "Arial"
        axisColor = "#000000"
        gridColor = "#DEDDDD"
        return {
            "config": {
                "title": {
                    "fontSize": 24,
                    "font": font,
                    "anchor": "start", # equivalent of left-aligned.
                    "fontColor": "#000000"
                },
                'view': {
                    "height": 300, 
                    "width": 400
                },
                "axisX": {
                    "domain": True,
                    #"domainColor": axisColor,
                    "gridColor": gridColor,
                    "domainWidth": 1,
                    "grid": False,
                    "labelFont": font,
                    "labelFontSize": 12,
                    "labelAngle": 0, 
                    "tickColor": axisColor,
                    "tickSize": 5, # default, including it just to show you can change it
                    "titleFont": font,
                    "titleFontSize": 16,
                    "titlePadding": 10, # guessing, not specified in styleguide
                    "title": "X Axis Title (units)", 
                },
                "axisY": {
                    "domain": False,
                    "grid": True,
                    "gridColor": gridColor,
                    "gridWidth": 1,
                    "labelFont": font,
                    "labelFontSize": 14,
                    "labelAngle": 0, 
                    #"ticks": False, # even if you don't have a "domain" you need to turn these off.
                    "titleFont": font,
                    "titleFontSize": 16,
                    "titlePadding": 10, # guessing, not specified in styleguide
                    "title": "Y Axis Title (units)", 
                    # titles are by default vertical left of axis so we need to hack this 
                    #"titleAngle": 0, # horizontal
                    #"titleY": -10, # move it up
                    #"titleX": 18, # move it to the right so it aligns with the labels 
                },
            }
                }

    # register the custom theme under a chosen name
    alt.themes.register('mds_special', mds_special)

    # enable the newly registered theme
    alt.themes.enable('mds_special')
    #alt.themes.enable('none') # to return to default

    # Update Data source based on user selection:
    a = selected_region
    plot_b_data = final_df.query('sub_region in @a').query('suicides_per_100k_pop>0.1').query('year < 2015 and year > 1986').groupby(['year','sub_region'],as_index = False).agg({"suicides_per_100k_pop":"mean","country":"nunique"})

    # Create a plot B
    source = plot_b_data.round(1)

    nearest = alt.selection(type='single', nearest=True, on='mouseover',
                        fields=['year'], empty='none')
    line= alt.Chart(source).mark_line(point=True).encode(
        x = alt.X('year:O',axis=alt.Axis(title='Date:Year')),
        y = alt.Y('suicides_per_100k_pop',axis=alt.Axis(title='Suicides per 100 k pop'),scale=alt.Scale(zero=False)),
        color='sub_region'
    ).properties(
        width=500,
        height=200,
        title='Suicide Rate per Continent'
    )
    selectors = alt.Chart(source).mark_point().encode(
        x='year:O',
        opacity=alt.value(0),
    ).add_selection(
        nearest
    )
    points = line.mark_point().encode(
        opacity=alt.condition(nearest, alt.value(1), alt.value(0))
    )
    text = line.mark_text(align='left', dx=5, dy=-5).encode(
        text=alt.condition(nearest, 'suicides_per_100k_pop', alt.value(' '))
    )
    rules = alt.Chart(source).mark_rule(color='gray').encode(
        x='year:O',
    ).transform_filter(
        nearest
    )
    chart_B = alt.layer(
        line, selectors, points, rules, text
    ).properties(
        width=600, height=300
    )        

    return chart_B

app.layout = html.Div([

    html.Div(
        className="app-header",
        children=[
            html.Div('Suicide Rate Dashboard', className="app-header--title")
        ]
    ),    

    ### Add Tabs to the top of the page
    dcc.Tabs(id='tabs', value='tab1', children=[
        dcc.Tab(label='Dashboard - Suicide Rate', value='tab-1'),
        dcc.Tab(label='Country Comparison', value='tab-2'),
    ]),    

#    ADD CONTENT HERE like: html.H1('text'),
    html.H1('WorldWide Rate'),
#    html.H2('This is a subtitle'),

#    html.H3('Here is our first plot:'),
    html.Iframe(
        sandbox='allow-scripts',
        id='plot_a',
        height='300',
        width='1500',
        style={'border-width': '0'},
        ################ The magic happens here
        srcDoc=make_plot().to_html()
        ################ The magic happens here
        ),

    #dcc.Markdown('''
    ### Dash and Markdown
    #            '''),

    ## these two components are related to dropdown
    # Let's comment out the demo-dropdown and dd-output to de-clutter our app a bit

    #dcc.Dropdown(
    #    id='demo-dropdown',
    #    options=[
    #        {'label': 'New York City', 'value': 'NYC'},
    #        {'label': 'Montreal', 'value': 'MTL'},
    #       {'label': 'San Francisco', 'value': 'SF'}
    #    ],
    #    value='NYC',
    #    style=dict(width='45%',
    #          verticalAlign="middle"
    #          )
    #    ),
    #    html.Div(id='dd-output'),
        
        # Just to add some space
        html.Iframe(height='25', width='10',style={'border-width': '0'}),

        html.H3('Suicide Rate by Region'),
        html.H4('Select one or multiple Regions'),

        dcc.Dropdown(
        id='dd-chart',
        options=[
            {'label': 'Africa', 'value': 'Africa','disabled': True},
            {'label': 'Eastern Africa', 'value': 'Eastern Africa'},
            {'label': 'Middle Africa', 'value': 'Middle Africa'},
            {'label': 'Northern Africa', 'value': 'Northern Africa'},
            {'label': 'Southern Africa', 'value': 'Southern Africa'},
            {'label': 'Western Africa', 'value': 'Western Africa'},
            {'label': 'Americas', 'value': 'Americas','disabled': True},
            {'label': 'Caribbean', 'value': 'Caribbean'},
            {'label': 'Central America', 'value': 'Central America'},
            {'label': 'Northern America', 'value': 'Northern America'},
            {'label': 'South America', 'value': 'South America'},
            {'label': 'Asia', 'value': 'Asia','disabled': True},
            {'label': 'Central Asia', 'value': 'Central Asia'},
            {'label': 'Eastern Asia', 'value': 'Eastern Asia'},
            {'label': 'South-Eastern Asia', 'value': 'South-Eastern Asia'},
            {'label': 'Southern Asia', 'value': 'Southern Asia'},
            {'label': 'Western Asia', 'value': 'Western Asia'},
            {'label': 'Europe', 'value': 'Europe','disabled': True},
            {'label': 'Eastern Europe', 'value': 'Eastern Europe'},
            {'label': 'Northern Europe', 'value': 'Northern Europe'},
            {'label': 'Southern Europe', 'value': 'Southern Europe'},
            {'label': 'Western Europe', 'value': 'Western Europe'},
            {'label': 'Oceania', 'value': 'Oceania','disabled': True},
            {'label': 'Australia and New Zealand', 'value': 'Australia and New Zealand'},
            {'label': 'Melanesia', 'value': 'Melanesia'},
            {'label': 'Micronesia', 'value': 'Micronesia'},        
            {'label': 'Polynesia', 'value': 'Polynesia'}
        ],
        value='Central America',
        multi=True,
        style=dict(width='45%',
              verticalAlign="middle"
              )
        ),
        # Just to add some space
        html.Iframe(height='200', width='10',style={'border-width': '0'}),

        html.Iframe(
        sandbox='allow-scripts',
        id='plot_b',
        height='300',
        width='1500',
        style={'border-width': '0'},
        ################ The magic happens here
        srcDoc=make_plot_B().to_html()
        ################ The magic happens here
        )  
])

# This first callback inserts raw text into an html.Div with id 'dd-output'
#       We normally omit the 'children' property as it is always the first property but this
#       just tells Dash to show the text. Every dash component has a 'children' property
# Note that the input argument needs to be provided as a list
# update_output is simply the function that runs when `demo-dropdown` is changed
# Let's comment out this to de-clutter our app once we know how it works

# This second callback tells Dash the output is the `plot` IFrame; srcDoc is a 
# special property that takes in RAW html as an input and renders it
# As input we take in the values from second dropdown we created (dd-chart) 
# then we run update_plot
@app.callback(
    dash.dependencies.Output('plot_b', 'srcDoc'),
    [dash.dependencies.Input('dd-chart', 'value')])
def update_plot(sub_region):

    updated_plot = make_plot_B(sub_region).to_html()

    return updated_plot

if __name__ == '__main__':
    app.run_server(debug=True)