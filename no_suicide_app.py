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

#### TAB 2 YEAR SLIDER ####
app.layout = html.Div([
    dcc.RangeSlider(
        id='my-range-slider',
        min=1986,
        max=2015,
        step=1,
        value=[1986, 2015]
    ),
    html.Div(id='output-container-range-slider')
])

#### END OF TAB 2 YEAR SLIDER ####

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

#plot_C = COUNTRIES
def make_plot_C(selected_country = 'Select a Country Please'):

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
    a = selected_country
    plot_c_data = final_df.query('country in @a').query('suicides_per_100k_pop>0.1').query('year < 2015 and year > 1986').groupby(['year','country'],as_index = False).agg({"suicides_per_100k_pop":"mean"})

    # Create a plot C
    source = plot_c_data.round(1)

    nearest = alt.selection(type='single', nearest=True, on='mouseover',
                        fields=['year'], empty='none')
    line= alt.Chart(source).mark_line(point=True).encode(
        x = alt.X('year:O',axis=alt.Axis(title='Date:Year')),
        y = alt.Y('suicides_per_100k_pop',axis=alt.Axis(title='Suicides per 100 k pop'),scale=alt.Scale(zero=False)),
        color='country'
    ).properties(
        width=500,
        height=200,
        title='Suicide Rate per Country'
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
    chart_C = alt.layer(
        line, selectors, points, rules, text
    ).properties(
        width=600, height=300
    )        

    return chart_C


#### TAB 2 CHARTS ####
def make_plot2a(country_a = '', country_b = ''):
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
​
    # register the custom theme under a chosen name
    alt.themes.register('mds_special', mds_special)
​
    # enable the newly registered theme
    alt.themes.enable('mds_special')
    #alt.themes.enable('none') # to return to default
​
    # Create Tab 2 Plot 1

    # Data Filtering
    # User selects the 2 countries 
    #country_a = 'Albania' # Needs to be replaced with value from Dropdown A
    #country_b = 'Canada' # Needs to be replaced with value from Dropdown A

    # Makes list of the 2 countries for use in later query
   # countries = [country_a, country_b]

    # User selects year range
    #year_start = 1988
    #year_end = 2010

    # Makes DataFrame of average suicide rates for the 2 countries
    data2a = final_df.query('suicides_per_100k_pop>0.1').query('year > @year_start & year < @year_end').query('country = @country_a OR country = @country_b').groupby(['country']).agg({'suicides_per_100k_pop':'mean'})
    data2a = data.reset_index()

    data2a = data2a.round(1)
​
    chart_2a = alt.Chart(data2a).mark_bar().encode(
        color = alt.Color('country:N'),
        x = alt.X('country:N', axis = alt.Axis(title = 'Countries', labelAngle = 0)),
        y = alt.Y('suicides_per_100k_pop:Q', axis = alt.Axis(title = 'Average Suicide Rate (per 100k people)', 
                                                            labelAngle = 90))
    ).properties(width = 700, height = 300,
                title = "Avg Suicide Rate by Country"
    ).configure_title(fontSize = 15
    ).configure_axis(labelFontSize = 12,
                    titleFontSize = 12,
                    labelColor = '#4c5c5c',
                    titleColor = '#3a4242'
    )
    return chart_2a

#### END OF TAB 2 CHARTS ####
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
        ),

        #    html.H3('Here is our first plot:'),
        html.Iframe(
        sandbox='allow-scripts',
        id='plot_c',
        height='300',
        width='1500',
        style={'border-width': '0'},
        ################ The magic happens here
        srcDoc=make_plot_C().to_html()
        ################ The magic happens here
        ),

#### TAB 2 PLOT 2A IFRAME ####
        html.Iframe(
        sandbox='allow-scripts',
        id='plot2a',
        height='300',
        width='1500',
        style={'border-width': '0'},
        ################ The magic happens here
        srcDoc=make_plot2a().to_html()
        ################ The magic happens here
        ),  
#### END OF TAB 2 PLOT 2A IFRAME ####
        html.Iframe(height='25', width='10',style={'border-width': '0'}),

        html.H3('Suicide Rate by Country'),
        html.H4('Select one or multiple countries'),

        dcc.Dropdown(
        id='dd-country',
        options=[
            {'label': 'Africa', 'value': 'Africa','disabled': True},
            {'label': 'Argentina', 'value': 'Argentina'},
            {'label': 'Bolivia', 'value': 'Bolivia'},
            {'label': 'Canada', 'value': 'Canada'}
        ],
        value='Please Select a Country',
        multi=True,
        style=dict(width='45%',
              verticalAlign="middle"
              )
        ),
#### TAB 2 DROPDOWNS START ####
        dcc.Dropdown(
        id='country_a_dropdown',
        options=[
            {'label': 'Afghanistan, 'value': 'Afghanistan},
            {'label': 'Aland Islands, 'value': 'Aland Islands},
            {'label': 'Albania, 'value': 'Albania},
            {'label': 'Algeria, 'value': 'Algeria},
            {'label': 'American Samoa, 'value': 'American Samoa},
            {'label': 'Andorra, 'value': 'Andorra},
            {'label': 'Angola, 'value': 'Angola},
            {'label': 'Anguilla, 'value': 'Anguilla},
            {'label': 'Antarctica, 'value': 'Antarctica},
            {'label': 'Antigua and Barbuda, 'value': 'Antigua and Barbuda},
            {'label': 'Argentina, 'value': 'Argentina},
            {'label': 'Armenia, 'value': 'Armenia},
            {'label': 'Aruba, 'value': 'Aruba},
            {'label': 'Australia, 'value': 'Australia},
            {'label': 'Austria, 'value': 'Austria},
            {'label': 'Azerbaijan, 'value': 'Azerbaijan},
            {'label': 'Bahamas, 'value': 'Bahamas},
            {'label': 'Bahrain, 'value': 'Bahrain},
            {'label': 'Bangladesh, 'value': 'Bangladesh},
            {'label': 'Barbados, 'value': 'Barbados},
            {'label': 'Belarus, 'value': 'Belarus},
            {'label': 'Belgium, 'value': 'Belgium},
            {'label': 'Belize, 'value': 'Belize},
            {'label': 'Benin, 'value': 'Benin},
            {'label': 'Bermuda, 'value': 'Bermuda},
            {'label': 'Bhutan, 'value': 'Bhutan},
            {'label': 'Bolivia (Plurinational State of), 'value': 'Bolivia (Plurinational State of)},
            {'label': 'Bonaire, Sint Eustatius and Saba, 'value': 'Bonaire, Sint Eustatius and Saba},
            {'label': 'Bosnia and Herzegovina, 'value': 'Bosnia and Herzegovina},
            {'label': 'Botswana, 'value': 'Botswana},
            {'label': 'Bouvet Island, 'value': 'Bouvet Island},
            {'label': 'Brazil, 'value': 'Brazil},
            {'label': 'British Indian Ocean Territory, 'value': 'British Indian Ocean Territory},
            {'label': 'Brunei Darussalam, 'value': 'Brunei Darussalam},
            {'label': 'Bulgaria, 'value': 'Bulgaria},
            {'label': 'Burkina Faso, 'value': 'Burkina Faso},
            {'label': 'Burundi, 'value': 'Burundi},
            {'label': 'Cambodia, 'value': 'Cambodia},
            {'label': 'Cameroon, 'value': 'Cameroon},
            {'label': 'Canada, 'value': 'Canada},
            {'label': 'Cabo Verde, 'value': 'Cabo Verde},
            {'label': 'Cayman Islands, 'value': 'Cayman Islands},
            {'label': 'Central African Republic, 'value': 'Central African Republic},
            {'label': 'Chad, 'value': 'Chad},
            {'label': 'Chile, 'value': 'Chile},
            {'label': 'China, 'value': 'China},
            {'label': 'Christmas Island, 'value': 'Christmas Island},
            {'label': 'Cocos (Keeling) Islands, 'value': 'Cocos (Keeling) Islands},
            {'label': 'Colombia, 'value': 'Colombia},
            {'label': 'Comoros, 'value': 'Comoros},
            {'label': 'Congo, 'value': 'Congo},
            {'label': 'Congo (Democratic Republic of the), 'value': 'Congo (Democratic Republic of the)},
            {'label': 'Cook Islands, 'value': 'Cook Islands},
            {'label': 'Costa Rica, 'value': 'Costa Rica},
            {'label': 'CÙte d'Ivoire, 'value': 'CÙte d'Ivoire},
            {'label': 'Croatia, 'value': 'Croatia},
            {'label': 'Cuba, 'value': 'Cuba},
            {'label': 'CuraÁao, 'value': 'CuraÁao},
            {'label': 'Cyprus, 'value': 'Cyprus},
            {'label': 'Czech Republic, 'value': 'Czech Republic},
            {'label': 'Denmark, 'value': 'Denmark},
            {'label': 'Djibouti, 'value': 'Djibouti},
            {'label': 'Dominica, 'value': 'Dominica},
            {'label': 'Dominican Republic, 'value': 'Dominican Republic},
            {'label': 'Ecuador, 'value': 'Ecuador},
            {'label': 'Egypt, 'value': 'Egypt},
            {'label': 'El Salvador, 'value': 'El Salvador},
            {'label': 'Equatorial Guinea, 'value': 'Equatorial Guinea},
            {'label': 'Eritrea, 'value': 'Eritrea},
            {'label': 'Estonia, 'value': 'Estonia},
            {'label': 'Ethiopia, 'value': 'Ethiopia},
            {'label': 'Falkland Islands (Malvinas), 'value': 'Falkland Islands (Malvinas)},
            {'label': 'Faroe Islands, 'value': 'Faroe Islands},
            {'label': 'Fiji, 'value': 'Fiji},
            {'label': 'Finland, 'value': 'Finland},
            {'label': 'France, 'value': 'France},
            {'label': 'French Guiana, 'value': 'French Guiana},
            {'label': 'French Polynesia, 'value': 'French Polynesia},
            {'label': 'French Southern Territories, 'value': 'French Southern Territories},
            {'label': 'Gabon, 'value': 'Gabon},
            {'label': 'Gambia, 'value': 'Gambia},
            {'label': 'Georgia, 'value': 'Georgia},
            {'label': 'Germany, 'value': 'Germany},
            {'label': 'Ghana, 'value': 'Ghana},
            {'label': 'Gibraltar, 'value': 'Gibraltar},
            {'label': 'Greece, 'value': 'Greece},
            {'label': 'Greenland, 'value': 'Greenland},
            {'label': 'Grenada, 'value': 'Grenada},
            {'label': 'Guadeloupe, 'value': 'Guadeloupe},
            {'label': 'Guam, 'value': 'Guam},
            {'label': 'Guatemala, 'value': 'Guatemala},
            {'label': 'Guernsey, 'value': 'Guernsey},
            {'label': 'Guinea, 'value': 'Guinea},
            {'label': 'Guinea-Bissau, 'value': 'Guinea-Bissau},
            {'label': 'Guyana, 'value': 'Guyana},
            {'label': 'Haiti, 'value': 'Haiti},
            {'label': 'Heard Island and McDonald Islands, 'value': 'Heard Island and McDonald Islands},
            {'label': 'Holy See, 'value': 'Holy See},
            {'label': 'Honduras, 'value': 'Honduras},
            {'label': 'Hong Kong, 'value': 'Hong Kong},
            {'label': 'Hungary, 'value': 'Hungary},
            {'label': 'Iceland, 'value': 'Iceland},
            {'label': 'India, 'value': 'India},
            {'label': 'Indonesia, 'value': 'Indonesia},
            {'label': 'Iran (Islamic Republic of), 'value': 'Iran (Islamic Republic of)},
            {'label': 'Iraq, 'value': 'Iraq},
            {'label': 'Ireland, 'value': 'Ireland},
            {'label': 'Isle of Man, 'value': 'Isle of Man},
            {'label': 'Israel, 'value': 'Israel},
            {'label': 'Italy, 'value': 'Italy},
            {'label': 'Jamaica, 'value': 'Jamaica},
            {'label': 'Japan, 'value': 'Japan},
            {'label': 'Jersey, 'value': 'Jersey},
            {'label': 'Jordan, 'value': 'Jordan},
            {'label': 'Kazakhstan, 'value': 'Kazakhstan},
            {'label': 'Kenya, 'value': 'Kenya},
            {'label': 'Kiribati, 'value': 'Kiribati},
            {'label': 'Korea (Democratic People's Republic of), 'value': 'Korea (Democratic People's Republic of)},
            {'label': 'Korea (Republic of), 'value': 'Korea (Republic of)},
            {'label': 'Kuwait, 'value': 'Kuwait},
            {'label': 'Kyrgyzstan, 'value': 'Kyrgyzstan},
            {'label': 'Lao People's Democratic Republic, 'value': 'Lao People's Democratic Republic},
            {'label': 'Latvia, 'value': 'Latvia},
            {'label': 'Lebanon, 'value': 'Lebanon},
            {'label': 'Lesotho, 'value': 'Lesotho},
            {'label': 'Liberia, 'value': 'Liberia},
            {'label': 'Libya, 'value': 'Libya},
            {'label': 'Liechtenstein, 'value': 'Liechtenstein},
            {'label': 'Lithuania, 'value': 'Lithuania},
            {'label': 'Luxembourg, 'value': 'Luxembourg},
            {'label': 'Macao, 'value': 'Macao},
            {'label': 'Macedonia (the former Yugoslav Republic of), 'value': 'Macedonia (the former Yugoslav Republic of)},
            {'label': 'Madagascar, 'value': 'Madagascar},
            {'label': 'Malawi, 'value': 'Malawi},
            {'label': 'Malaysia, 'value': 'Malaysia},
            {'label': 'Maldives, 'value': 'Maldives},
            {'label': 'Mali, 'value': 'Mali},
            {'label': 'Malta, 'value': 'Malta},
            {'label': 'Marshall Islands, 'value': 'Marshall Islands},
            {'label': 'Martinique, 'value': 'Martinique},
            {'label': 'Mauritania, 'value': 'Mauritania},
            {'label': 'Mauritius, 'value': 'Mauritius},
            {'label': 'Mayotte, 'value': 'Mayotte},
            {'label': 'Mexico, 'value': 'Mexico},
            {'label': 'Micronesia (Federated States of), 'value': 'Micronesia (Federated States of)},
            {'label': 'Moldova (Republic of), 'value': 'Moldova (Republic of)},
            {'label': 'Monaco, 'value': 'Monaco},
            {'label': 'Mongolia, 'value': 'Mongolia},
            {'label': 'Montenegro, 'value': 'Montenegro},
            {'label': 'Montserrat, 'value': 'Montserrat},
            {'label': 'Morocco, 'value': 'Morocco},
            {'label': 'Mozambique, 'value': 'Mozambique},
            {'label': 'Myanmar, 'value': 'Myanmar},
            {'label': 'Namibia, 'value': 'Namibia},
            {'label': 'Nauru, 'value': 'Nauru},
            {'label': 'Nepal, 'value': 'Nepal},
            {'label': 'Netherlands, 'value': 'Netherlands},
            {'label': 'New Caledonia, 'value': 'New Caledonia},
            {'label': 'New Zealand, 'value': 'New Zealand},
            {'label': 'Nicaragua, 'value': 'Nicaragua},
            {'label': 'Niger, 'value': 'Niger},
            {'label': 'Nigeria, 'value': 'Nigeria},
            {'label': 'Niue, 'value': 'Niue},
            {'label': 'Norfolk Island, 'value': 'Norfolk Island},
            {'label': 'Northern Mariana Islands, 'value': 'Northern Mariana Islands},
            {'label': 'Norway, 'value': 'Norway},
            {'label': 'Oman, 'value': 'Oman},
            {'label': 'Pakistan, 'value': 'Pakistan},
            {'label': 'Palau, 'value': 'Palau},
            {'label': 'Palestine, State of, 'value': 'Palestine, State of},
            {'label': 'Panama, 'value': 'Panama},
            {'label': 'Papua New Guinea, 'value': 'Papua New Guinea},
            {'label': 'Paraguay, 'value': 'Paraguay},
            {'label': 'Peru, 'value': 'Peru},
            {'label': 'Philippines, 'value': 'Philippines},
            {'label': 'Pitcairn, 'value': 'Pitcairn},
            {'label': 'Poland, 'value': 'Poland},
            {'label': 'Portugal, 'value': 'Portugal},
            {'label': 'Puerto Rico, 'value': 'Puerto Rico},
            {'label': 'Qatar, 'value': 'Qatar},
            {'label': 'RÈunion, 'value': 'RÈunion},
            {'label': 'Romania, 'value': 'Romania},
            {'label': 'Russian Federation, 'value': 'Russian Federation},
            {'label': 'Rwanda, 'value': 'Rwanda},
            {'label': 'Saint BarthÈlemy, 'value': 'Saint BarthÈlemy},
            {'label': 'Saint Helena, Ascension and Tristan da Cunha, 'value': 'Saint Helena, Ascension and Tristan da Cunha},
            {'label': 'Saint Kitts and Nevis, 'value': 'Saint Kitts and Nevis},
            {'label': 'Saint Lucia, 'value': 'Saint Lucia},
            {'label': 'Saint Martin (French part), 'value': 'Saint Martin (French part)},
            {'label': 'Saint Pierre and Miquelon, 'value': 'Saint Pierre and Miquelon},
            {'label': 'Saint Vincent and the Grenadines, 'value': 'Saint Vincent and the Grenadines},
            {'label': 'Samoa, 'value': 'Samoa},
            {'label': 'San Marino, 'value': 'San Marino},
            {'label': 'Sao Tome and Principe, 'value': 'Sao Tome and Principe},
            {'label': 'Saudi Arabia, 'value': 'Saudi Arabia},
            {'label': 'Senegal, 'value': 'Senegal},
            {'label': 'Serbia, 'value': 'Serbia},
            {'label': 'Seychelles, 'value': 'Seychelles},
            {'label': 'Sierra Leone, 'value': 'Sierra Leone},
            {'label': 'Singapore, 'value': 'Singapore},
            {'label': 'Sint Maarten (Dutch part), 'value': 'Sint Maarten (Dutch part)},
            {'label': 'Slovakia, 'value': 'Slovakia},
            {'label': 'Slovenia, 'value': 'Slovenia},
            {'label': 'Solomon Islands, 'value': 'Solomon Islands},
            {'label': 'Somalia, 'value': 'Somalia},
            {'label': 'South Africa, 'value': 'South Africa},
            {'label': 'South Georgia and the South Sandwich Islands, 'value': 'South Georgia and the South Sandwich Islands},
            {'label': 'South Sudan, 'value': 'South Sudan},
            {'label': 'Spain, 'value': 'Spain},
            {'label': 'Sri Lanka, 'value': 'Sri Lanka},
            {'label': 'Sudan, 'value': 'Sudan},
            {'label': 'Suriname, 'value': 'Suriname},
            {'label': 'Svalbard and Jan Mayen, 'value': 'Svalbard and Jan Mayen},
            {'label': 'Swaziland, 'value': 'Swaziland},
            {'label': 'Sweden, 'value': 'Sweden},
            {'label': 'Switzerland, 'value': 'Switzerland},
            {'label': 'Syrian Arab Republic, 'value': 'Syrian Arab Republic},
            {'label': 'Taiwan, Province of China, 'value': 'Taiwan, Province of China},
            {'label': 'Tajikistan, 'value': 'Tajikistan},
            {'label': 'Tanzania, United Republic of, 'value': 'Tanzania, United Republic of},
            {'label': 'Thailand, 'value': 'Thailand},
            {'label': 'Timor-Leste, 'value': 'Timor-Leste},
            {'label': 'Togo, 'value': 'Togo},
            {'label': 'Tokelau, 'value': 'Tokelau},
            {'label': 'Tonga, 'value': 'Tonga},
            {'label': 'Trinidad and Tobago, 'value': 'Trinidad and Tobago},
            {'label': 'Tunisia, 'value': 'Tunisia},
            {'label': 'Turkey, 'value': 'Turkey},
            {'label': 'Turkmenistan, 'value': 'Turkmenistan},
            {'label': 'Turks and Caicos Islands, 'value': 'Turks and Caicos Islands},
            {'label': 'Tuvalu, 'value': 'Tuvalu},
            {'label': 'Uganda, 'value': 'Uganda},
            {'label': 'Ukraine, 'value': 'Ukraine},
            {'label': 'United Arab Emirates, 'value': 'United Arab Emirates},
            {'label': 'United Kingdom of Great Britain and Northern Ireland, 'value': 'United Kingdom of Great Britain and Northern Ireland},
            {'label': 'United States of America, 'value': 'United States of America},
            {'label': 'United States Minor Outlying Islands, 'value': 'United States Minor Outlying Islands},
            {'label': 'Uruguay, 'value': 'Uruguay},
            {'label': 'Uzbekistan, 'value': 'Uzbekistan},
            {'label': 'Vanuatu, 'value': 'Vanuatu},
            {'label': 'Venezuela (Bolivarian Republic of), 'value': 'Venezuela (Bolivarian Republic of)},
            {'label': 'Viet Nam, 'value': 'Viet Nam},
            {'label': 'Virgin Islands (British), 'value': 'Virgin Islands (British)},
            {'label': 'Virgin Islands (U.S.), 'value': 'Virgin Islands (U.S.)},
            {'label': 'Wallis and Futuna, 'value': 'Wallis and Futuna},
            {'label': 'Western Sahara, 'value': 'Western Sahara},
            {'label': 'Yemen, 'value': 'Yemen},
            {'label': 'Zambia, 'value': 'Zambia},
            {'label': 'Zimbabwe, 'value': 'Zimbabwe},
        ],
        value='Afghanistan',
        style=dict(width='45%',
             verticalAlign="middle"
             )
       ),
       html.Div(id='dd-output'),
    
    dcc.Dropdown(
        id='country_b_dropdown',
        options=[
            {'label': 'Afghanistan, 'value': 'Afghanistan},
            {'label': 'Aland Islands, 'value': 'Aland Islands},
            {'label': 'Albania, 'value': 'Albania},
            {'label': 'Algeria, 'value': 'Algeria},
            {'label': 'American Samoa, 'value': 'American Samoa},
            {'label': 'Andorra, 'value': 'Andorra},
            {'label': 'Angola, 'value': 'Angola},
            {'label': 'Anguilla, 'value': 'Anguilla},
            {'label': 'Antarctica, 'value': 'Antarctica},
            {'label': 'Antigua and Barbuda, 'value': 'Antigua and Barbuda},
            {'label': 'Argentina, 'value': 'Argentina},
            {'label': 'Armenia, 'value': 'Armenia},
            {'label': 'Aruba, 'value': 'Aruba},
            {'label': 'Australia, 'value': 'Australia},
            {'label': 'Austria, 'value': 'Austria},
            {'label': 'Azerbaijan, 'value': 'Azerbaijan},
            {'label': 'Bahamas, 'value': 'Bahamas},
            {'label': 'Bahrain, 'value': 'Bahrain},
            {'label': 'Bangladesh, 'value': 'Bangladesh},
            {'label': 'Barbados, 'value': 'Barbados},
            {'label': 'Belarus, 'value': 'Belarus},
            {'label': 'Belgium, 'value': 'Belgium},
            {'label': 'Belize, 'value': 'Belize},
            {'label': 'Benin, 'value': 'Benin},
            {'label': 'Bermuda, 'value': 'Bermuda},
            {'label': 'Bhutan, 'value': 'Bhutan},
            {'label': 'Bolivia (Plurinational State of), 'value': 'Bolivia (Plurinational State of)},
            {'label': 'Bonaire, Sint Eustatius and Saba, 'value': 'Bonaire, Sint Eustatius and Saba},
            {'label': 'Bosnia and Herzegovina, 'value': 'Bosnia and Herzegovina},
            {'label': 'Botswana, 'value': 'Botswana},
            {'label': 'Bouvet Island, 'value': 'Bouvet Island},
            {'label': 'Brazil, 'value': 'Brazil},
            {'label': 'British Indian Ocean Territory, 'value': 'British Indian Ocean Territory},
            {'label': 'Brunei Darussalam, 'value': 'Brunei Darussalam},
            {'label': 'Bulgaria, 'value': 'Bulgaria},
            {'label': 'Burkina Faso, 'value': 'Burkina Faso},
            {'label': 'Burundi, 'value': 'Burundi},
            {'label': 'Cambodia, 'value': 'Cambodia},
            {'label': 'Cameroon, 'value': 'Cameroon},
            {'label': 'Canada, 'value': 'Canada},
            {'label': 'Cabo Verde, 'value': 'Cabo Verde},
            {'label': 'Cayman Islands, 'value': 'Cayman Islands},
            {'label': 'Central African Republic, 'value': 'Central African Republic},
            {'label': 'Chad, 'value': 'Chad},
            {'label': 'Chile, 'value': 'Chile},
            {'label': 'China, 'value': 'China},
            {'label': 'Christmas Island, 'value': 'Christmas Island},
            {'label': 'Cocos (Keeling) Islands, 'value': 'Cocos (Keeling) Islands},
            {'label': 'Colombia, 'value': 'Colombia},
            {'label': 'Comoros, 'value': 'Comoros},
            {'label': 'Congo, 'value': 'Congo},
            {'label': 'Congo (Democratic Republic of the), 'value': 'Congo (Democratic Republic of the)},
            {'label': 'Cook Islands, 'value': 'Cook Islands},
            {'label': 'Costa Rica, 'value': 'Costa Rica},
            {'label': 'CÙte d'Ivoire, 'value': 'CÙte d'Ivoire},
            {'label': 'Croatia, 'value': 'Croatia},
            {'label': 'Cuba, 'value': 'Cuba},
            {'label': 'CuraÁao, 'value': 'CuraÁao},
            {'label': 'Cyprus, 'value': 'Cyprus},
            {'label': 'Czech Republic, 'value': 'Czech Republic},
            {'label': 'Denmark, 'value': 'Denmark},
            {'label': 'Djibouti, 'value': 'Djibouti},
            {'label': 'Dominica, 'value': 'Dominica},
            {'label': 'Dominican Republic, 'value': 'Dominican Republic},
            {'label': 'Ecuador, 'value': 'Ecuador},
            {'label': 'Egypt, 'value': 'Egypt},
            {'label': 'El Salvador, 'value': 'El Salvador},
            {'label': 'Equatorial Guinea, 'value': 'Equatorial Guinea},
            {'label': 'Eritrea, 'value': 'Eritrea},
            {'label': 'Estonia, 'value': 'Estonia},
            {'label': 'Ethiopia, 'value': 'Ethiopia},
            {'label': 'Falkland Islands (Malvinas), 'value': 'Falkland Islands (Malvinas)},
            {'label': 'Faroe Islands, 'value': 'Faroe Islands},
            {'label': 'Fiji, 'value': 'Fiji},
            {'label': 'Finland, 'value': 'Finland},
            {'label': 'France, 'value': 'France},
            {'label': 'French Guiana, 'value': 'French Guiana},
            {'label': 'French Polynesia, 'value': 'French Polynesia},
            {'label': 'French Southern Territories, 'value': 'French Southern Territories},
            {'label': 'Gabon, 'value': 'Gabon},
            {'label': 'Gambia, 'value': 'Gambia},
            {'label': 'Georgia, 'value': 'Georgia},
            {'label': 'Germany, 'value': 'Germany},
            {'label': 'Ghana, 'value': 'Ghana},
            {'label': 'Gibraltar, 'value': 'Gibraltar},
            {'label': 'Greece, 'value': 'Greece},
            {'label': 'Greenland, 'value': 'Greenland},
            {'label': 'Grenada, 'value': 'Grenada},
            {'label': 'Guadeloupe, 'value': 'Guadeloupe},
            {'label': 'Guam, 'value': 'Guam},
            {'label': 'Guatemala, 'value': 'Guatemala},
            {'label': 'Guernsey, 'value': 'Guernsey},
            {'label': 'Guinea, 'value': 'Guinea},
            {'label': 'Guinea-Bissau, 'value': 'Guinea-Bissau},
            {'label': 'Guyana, 'value': 'Guyana},
            {'label': 'Haiti, 'value': 'Haiti},
            {'label': 'Heard Island and McDonald Islands, 'value': 'Heard Island and McDonald Islands},
            {'label': 'Holy See, 'value': 'Holy See},
            {'label': 'Honduras, 'value': 'Honduras},
            {'label': 'Hong Kong, 'value': 'Hong Kong},
            {'label': 'Hungary, 'value': 'Hungary},
            {'label': 'Iceland, 'value': 'Iceland},
            {'label': 'India, 'value': 'India},
            {'label': 'Indonesia, 'value': 'Indonesia},
            {'label': 'Iran (Islamic Republic of), 'value': 'Iran (Islamic Republic of)},
            {'label': 'Iraq, 'value': 'Iraq},
            {'label': 'Ireland, 'value': 'Ireland},
            {'label': 'Isle of Man, 'value': 'Isle of Man},
            {'label': 'Israel, 'value': 'Israel},
            {'label': 'Italy, 'value': 'Italy},
            {'label': 'Jamaica, 'value': 'Jamaica},
            {'label': 'Japan, 'value': 'Japan},
            {'label': 'Jersey, 'value': 'Jersey},
            {'label': 'Jordan, 'value': 'Jordan},
            {'label': 'Kazakhstan, 'value': 'Kazakhstan},
            {'label': 'Kenya, 'value': 'Kenya},
            {'label': 'Kiribati, 'value': 'Kiribati},
            {'label': 'Korea (Democratic People's Republic of), 'value': 'Korea (Democratic People's Republic of)},
            {'label': 'Korea (Republic of), 'value': 'Korea (Republic of)},
            {'label': 'Kuwait, 'value': 'Kuwait},
            {'label': 'Kyrgyzstan, 'value': 'Kyrgyzstan},
            {'label': 'Lao People's Democratic Republic, 'value': 'Lao People's Democratic Republic},
            {'label': 'Latvia, 'value': 'Latvia},
            {'label': 'Lebanon, 'value': 'Lebanon},
            {'label': 'Lesotho, 'value': 'Lesotho},
            {'label': 'Liberia, 'value': 'Liberia},
            {'label': 'Libya, 'value': 'Libya},
            {'label': 'Liechtenstein, 'value': 'Liechtenstein},
            {'label': 'Lithuania, 'value': 'Lithuania},
            {'label': 'Luxembourg, 'value': 'Luxembourg},
            {'label': 'Macao, 'value': 'Macao},
            {'label': 'Macedonia (the former Yugoslav Republic of), 'value': 'Macedonia (the former Yugoslav Republic of)},
            {'label': 'Madagascar, 'value': 'Madagascar},
            {'label': 'Malawi, 'value': 'Malawi},
            {'label': 'Malaysia, 'value': 'Malaysia},
            {'label': 'Maldives, 'value': 'Maldives},
            {'label': 'Mali, 'value': 'Mali},
            {'label': 'Malta, 'value': 'Malta},
            {'label': 'Marshall Islands, 'value': 'Marshall Islands},
            {'label': 'Martinique, 'value': 'Martinique},
            {'label': 'Mauritania, 'value': 'Mauritania},
            {'label': 'Mauritius, 'value': 'Mauritius},
            {'label': 'Mayotte, 'value': 'Mayotte},
            {'label': 'Mexico, 'value': 'Mexico},
            {'label': 'Micronesia (Federated States of), 'value': 'Micronesia (Federated States of)},
            {'label': 'Moldova (Republic of), 'value': 'Moldova (Republic of)},
            {'label': 'Monaco, 'value': 'Monaco},
            {'label': 'Mongolia, 'value': 'Mongolia},
            {'label': 'Montenegro, 'value': 'Montenegro},
            {'label': 'Montserrat, 'value': 'Montserrat},
            {'label': 'Morocco, 'value': 'Morocco},
            {'label': 'Mozambique, 'value': 'Mozambique},
            {'label': 'Myanmar, 'value': 'Myanmar},
            {'label': 'Namibia, 'value': 'Namibia},
            {'label': 'Nauru, 'value': 'Nauru},
            {'label': 'Nepal, 'value': 'Nepal},
            {'label': 'Netherlands, 'value': 'Netherlands},
            {'label': 'New Caledonia, 'value': 'New Caledonia},
            {'label': 'New Zealand, 'value': 'New Zealand},
            {'label': 'Nicaragua, 'value': 'Nicaragua},
            {'label': 'Niger, 'value': 'Niger},
            {'label': 'Nigeria, 'value': 'Nigeria},
            {'label': 'Niue, 'value': 'Niue},
            {'label': 'Norfolk Island, 'value': 'Norfolk Island},
            {'label': 'Northern Mariana Islands, 'value': 'Northern Mariana Islands},
            {'label': 'Norway, 'value': 'Norway},
            {'label': 'Oman, 'value': 'Oman},
            {'label': 'Pakistan, 'value': 'Pakistan},
            {'label': 'Palau, 'value': 'Palau},
            {'label': 'Palestine, State of, 'value': 'Palestine, State of},
            {'label': 'Panama, 'value': 'Panama},
            {'label': 'Papua New Guinea, 'value': 'Papua New Guinea},
            {'label': 'Paraguay, 'value': 'Paraguay},
            {'label': 'Peru, 'value': 'Peru},
            {'label': 'Philippines, 'value': 'Philippines},
            {'label': 'Pitcairn, 'value': 'Pitcairn},
            {'label': 'Poland, 'value': 'Poland},
            {'label': 'Portugal, 'value': 'Portugal},
            {'label': 'Puerto Rico, 'value': 'Puerto Rico},
            {'label': 'Qatar, 'value': 'Qatar},
            {'label': 'RÈunion, 'value': 'RÈunion},
            {'label': 'Romania, 'value': 'Romania},
            {'label': 'Russian Federation, 'value': 'Russian Federation},
            {'label': 'Rwanda, 'value': 'Rwanda},
            {'label': 'Saint BarthÈlemy, 'value': 'Saint BarthÈlemy},
            {'label': 'Saint Helena, Ascension and Tristan da Cunha, 'value': 'Saint Helena, Ascension and Tristan da Cunha},
            {'label': 'Saint Kitts and Nevis, 'value': 'Saint Kitts and Nevis},
            {'label': 'Saint Lucia, 'value': 'Saint Lucia},
            {'label': 'Saint Martin (French part), 'value': 'Saint Martin (French part)},
            {'label': 'Saint Pierre and Miquelon, 'value': 'Saint Pierre and Miquelon},
            {'label': 'Saint Vincent and the Grenadines, 'value': 'Saint Vincent and the Grenadines},
            {'label': 'Samoa, 'value': 'Samoa},
            {'label': 'San Marino, 'value': 'San Marino},
            {'label': 'Sao Tome and Principe, 'value': 'Sao Tome and Principe},
            {'label': 'Saudi Arabia, 'value': 'Saudi Arabia},
            {'label': 'Senegal, 'value': 'Senegal},
            {'label': 'Serbia, 'value': 'Serbia},
            {'label': 'Seychelles, 'value': 'Seychelles},
            {'label': 'Sierra Leone, 'value': 'Sierra Leone},
            {'label': 'Singapore, 'value': 'Singapore},
            {'label': 'Sint Maarten (Dutch part), 'value': 'Sint Maarten (Dutch part)},
            {'label': 'Slovakia, 'value': 'Slovakia},
            {'label': 'Slovenia, 'value': 'Slovenia},
            {'label': 'Solomon Islands, 'value': 'Solomon Islands},
            {'label': 'Somalia, 'value': 'Somalia},
            {'label': 'South Africa, 'value': 'South Africa},
            {'label': 'South Georgia and the South Sandwich Islands, 'value': 'South Georgia and the South Sandwich Islands},
            {'label': 'South Sudan, 'value': 'South Sudan},
            {'label': 'Spain, 'value': 'Spain},
            {'label': 'Sri Lanka, 'value': 'Sri Lanka},
            {'label': 'Sudan, 'value': 'Sudan},
            {'label': 'Suriname, 'value': 'Suriname},
            {'label': 'Svalbard and Jan Mayen, 'value': 'Svalbard and Jan Mayen},
            {'label': 'Swaziland, 'value': 'Swaziland},
            {'label': 'Sweden, 'value': 'Sweden},
            {'label': 'Switzerland, 'value': 'Switzerland},
            {'label': 'Syrian Arab Republic, 'value': 'Syrian Arab Republic},
            {'label': 'Taiwan, Province of China, 'value': 'Taiwan, Province of China},
            {'label': 'Tajikistan, 'value': 'Tajikistan},
            {'label': 'Tanzania, United Republic of, 'value': 'Tanzania, United Republic of},
            {'label': 'Thailand, 'value': 'Thailand},
            {'label': 'Timor-Leste, 'value': 'Timor-Leste},
            {'label': 'Togo, 'value': 'Togo},
            {'label': 'Tokelau, 'value': 'Tokelau},
            {'label': 'Tonga, 'value': 'Tonga},
            {'label': 'Trinidad and Tobago, 'value': 'Trinidad and Tobago},
            {'label': 'Tunisia, 'value': 'Tunisia},
            {'label': 'Turkey, 'value': 'Turkey},
            {'label': 'Turkmenistan, 'value': 'Turkmenistan},
            {'label': 'Turks and Caicos Islands, 'value': 'Turks and Caicos Islands},
            {'label': 'Tuvalu, 'value': 'Tuvalu},
            {'label': 'Uganda, 'value': 'Uganda},
            {'label': 'Ukraine, 'value': 'Ukraine},
            {'label': 'United Arab Emirates, 'value': 'United Arab Emirates},
            {'label': 'United Kingdom of Great Britain and Northern Ireland, 'value': 'United Kingdom of Great Britain and Northern Ireland},
            {'label': 'United States of America, 'value': 'United States of America},
            {'label': 'United States Minor Outlying Islands, 'value': 'United States Minor Outlying Islands},
            {'label': 'Uruguay, 'value': 'Uruguay},
            {'label': 'Uzbekistan, 'value': 'Uzbekistan},
            {'label': 'Vanuatu, 'value': 'Vanuatu},
            {'label': 'Venezuela (Bolivarian Republic of), 'value': 'Venezuela (Bolivarian Republic of)},
            {'label': 'Viet Nam, 'value': 'Viet Nam},
            {'label': 'Virgin Islands (British), 'value': 'Virgin Islands (British)},
            {'label': 'Virgin Islands (U.S.), 'value': 'Virgin Islands (U.S.)},
            {'label': 'Wallis and Futuna, 'value': 'Wallis and Futuna},
            {'label': 'Western Sahara, 'value': 'Western Sahara},
            {'label': 'Yemen, 'value': 'Yemen},
            {'label': 'Zambia, 'value': 'Zambia},
            {'label': 'Zimbabwe, 'value': 'Zimbabwe},
        ],
        value='Afghanistan',
        style=dict(width='45%',
             verticalAlign="middle"
             )
       ),
       html.Div(id='dd-output'),
#### END OF TAB 2 DROPDOWNS ####
        # Just to add some space
        html.Iframe(height='200', width='10',style={'border-width': '0'})
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

@app.callback(
    dash.dependencies.Output('plot_c', 'srcDoc'),
    [dash.dependencies.Input('dd-country', 'value')])
def update_plot_c(country):

    updated_plot_c = make_plot_C(country).to_html()

    return updated_plot_c

@app.callback(
    dash.dependencies.Output('plot2a', 'srcDoc'),
    [dash.dependencies.Input('country_a_dropdown', 'value'),
    dash.dependencies.Input('country_b_dropdown', 'value')])
def update_plot(country_a, country_b):
    updated_plot2a = make_plot2a(country_a, country_b).to_html()
    return updated_plot2a

if __name__ == '__main__':
    app.run_server(debug=True)