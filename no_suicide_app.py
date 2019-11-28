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


#### LOAD AND PREPARE DATA
initial_df = pd.read_csv('https://raw.githubusercontent.com/UBC-MDS/DSCI_532_Group102_No_Suicide_Squad/master/data/SD_data_information.csv', index_col=0, parse_dates=True).reset_index()
continent_df = pd.read_excel('https://github.com/UBC-MDS/DSCI_532_Group102_No_Suicide_Squad/blob/master/data/countryContinent_data_excel.xlsx?raw=true')
final_df = initial_df.merge(continent_df, on='country', how='left')
final_df = final_df.drop(['country-year', ' gdp_for_year ($) ','HDI for year', 'code_2','country_code','region_code','sub_region_code'],axis=1)
final_df = final_df.rename(columns={'gdp_per_capita ($)': 'gdp_per_capita_usd', 'code_3': 'country_code_name','suicides/100k pop':'suicides_per_100k_pop'})
final_df["age"]= final_df["age"].str.replace("5-14", "05-14", case = False)
final_df['demo_group'] = final_df["sex"].map(str) +[" : "]+ final_df["age"]
plot_a_data = final_df.query('suicides_per_100k_pop>0.1').query('year < 2015 and year > 1986').groupby(['year','continent'],as_index = False).agg({"suicides_per_100k_pop":"mean","country":"nunique"})
general_data = final_df.query('suicides_per_100k_pop>0.1').query('year < 2015 and year > 1986').groupby(['year'],as_index = False).agg({"suicides_per_100k_pop":"mean","country":"nunique"})
general_data['Label'] = 'Worldwide Benchmark'


#### DEFINE THEME
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

#### DEFINE PLOT 1a FUNCTION (continent)
def make_plot_1a():
    # Create a plot 1a
    source = plot_a_data.round(1)

    nearest = alt.selection(type='single', nearest=True, on='mouseover',
                        fields=['year'], empty='none')
    line= alt.Chart(source).mark_line(point=False).encode(
        x = alt.X('year:O',axis=alt.Axis(title='Date:Year')),
        y = alt.Y('suicides_per_100k_pop',axis=alt.Axis(title='Suicides per 100 k pop'),scale=alt.Scale(zero=False)),
        color = alt.Color('continent',legend=alt.Legend(title="Legend"))
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
    line2 = alt.Chart(general_data).mark_line(stroke="black",point=False,strokeDash=[1,5],interpolate ='monotone',size =5,color="#FFAA00").encode(
    x = alt.X('year:O',axis=alt.Axis(title='Date:Year')),
    y = alt.Y('suicides_per_100k_pop',axis=alt.Axis(title='Suicides per 100 k pop'),scale=alt.Scale(zero=False)),
    color = alt.Color('Label',legend=alt.Legend())
    )
    chart_1a = alt.layer(
        line,line2, selectors, points, rules, text
    ).properties(
        width=600, height=300
    ).configure_legend(
    strokeColor='gray',
    fillColor='#EEEEEE',
    padding=10,
    cornerRadius=10
    )          

    return chart_1a

#### DEFINE PLOT 1b FUNCTION (region)
def make_plot_1b(selected_region = 'Select a Region Please'):

    # Update Data source based on user selection:
    a = selected_region
    plot_b_data = final_df.query('sub_region in @a').query('suicides_per_100k_pop>0.1').query('year < 2015 and year > 1986').groupby(['year','sub_region'],as_index = False).agg({"suicides_per_100k_pop":"mean","country":"nunique"})

    # Create a plot 1b
    source = plot_b_data.round(1)

    nearest = alt.selection(type='single', nearest=True, on='mouseover',
                        fields=['year'], empty='none')
    line= alt.Chart(source).mark_line(point=False).encode(
        x = alt.X('year:O',axis=alt.Axis(title='Date:Year')),
        y = alt.Y('suicides_per_100k_pop',axis=alt.Axis(title='Suicides per 100 k pop'),scale=alt.Scale(zero=False)),
        color = alt.Color('sub_region',legend=alt.Legend(title = 'Legend'))
    ).properties(
        width=500,
        height=200,
        title='Suicide Rate per Region'
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
    line2= alt.Chart(general_data).mark_line(stroke="black",point=False,strokeDash=[1,5],interpolate ='monotone',size =5,color="#FFAA00").encode(
    x = alt.X('year:O',axis=alt.Axis(title='Date:Year')),
    y = alt.Y('suicides_per_100k_pop',axis=alt.Axis(title='Suicides per 100 k pop'),scale=alt.Scale(zero=False)),
    color = alt.Color('Label',legend=alt.Legend())
    )
    chart_1b = alt.layer(
        line,line2, selectors, points, rules, text
    ).properties(
        width=600, height=300
    ).configure_legend(
    strokeColor='gray',
    fillColor='#EEEEEE',
    padding=10,
    cornerRadius=10
    )         

    return chart_1b

#### DEFINE PLOT 1c FUNCTION (countries)
def make_plot_1c(selected_country = 'Select a Country Please'):

    # Update Data source based on user selection:
    a = selected_country
    plot_c_data = final_df.query('country in @a').query('suicides_per_100k_pop>0.1').query('year < 2015 and year > 1986').groupby(['year','country'],as_index = False).agg({"suicides_per_100k_pop":"mean"})

    # Create a plot C
    source = plot_c_data.round(1)

    nearest = alt.selection(type='single', nearest=True, on='mouseover',
                        fields=['year'], empty='none')
    line= alt.Chart(source).mark_line(point=False).encode(
        x = alt.X('year:O',axis=alt.Axis(title='Date:Year')),
        y = alt.Y('suicides_per_100k_pop',axis=alt.Axis(title='Suicides per 100 k pop'),scale=alt.Scale(zero=False)),
        color = alt.Color('country',legend=alt.Legend(title='Legend'))
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
    line2= alt.Chart(general_data).mark_line(stroke="black",point=False,strokeDash=[1,5],interpolate ='monotone',size =5,color="#FFAA00").encode(
    x = alt.X('year:O',axis=alt.Axis(title='Date:Year')),
    y = alt.Y('suicides_per_100k_pop',axis=alt.Axis(title='Suicides per 100 k pop'),scale=alt.Scale(zero=False)),
    color = alt.Color('Label',legend=alt.Legend())
    )
    chart_C = alt.layer(
        line,line2, selectors, points, rules, text
    ).properties(
        width=600, height=300
    ).configure_legend(
    strokeColor='gray',
    fillColor='#EEEEEE',
    padding=10,
    cornerRadius=10
    )           

    return chart_C

#### DEFINE PLOT 1d FUNCTION (countries)
def make_plot_1d(selected_country = 'Select a Country Please'):

    # Update Data source based on user selection:
    a = selected_country
    plot_d_data = final_df.query('country in @a').query('suicides_per_100k_pop>0.1').query('year < 2015 and year > 1986').groupby(['year','demo_group'],as_index = False).agg({"suicides_per_100k_pop":"mean"})
    
    # Create a plot D
    source = plot_d_data.round(1)

    nearest = alt.selection(type='single', nearest=True, on='mouseover',
                        fields=['year'], empty='none')
    line= alt.Chart(source).mark_line(point=False).encode(
        x = alt.X('year:O',axis=alt.Axis(title='Date:Year')),
        y = alt.Y('suicides_per_100k_pop',axis=alt.Axis(title='Suicides per 100 k pop'),scale=alt.Scale(zero=False)),
        color = alt.Color('demo_group',legend=alt.Legend(title='Legend'))
    ).properties(
        width=500,
        height=200,
        title='Average Suicide Rate per Demographic Group in Selected Country (Countries)'
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
    line2= alt.Chart(general_data).mark_line(stroke="black",point=False,strokeDash=[1,5],interpolate ='monotone',size =5,color="#FFAA00").encode(
    x = alt.X('year:O',axis=alt.Axis(title='Date:Year')),
    y = alt.Y('suicides_per_100k_pop',axis=alt.Axis(title='Suicides per 100 k pop'),scale=alt.Scale(zero=False)),
    color = alt.Color('Label',legend=alt.Legend())
    )
    chart_D = alt.layer(
        line,line2, selectors, points, rules, text
    ).properties(
        width=600, height=300
    ).configure_legend(
    strokeColor='gray',
    fillColor='#EEEEEE',
    padding=10,
    cornerRadius=10
    )           

    return chart_D

#### DEFINE PLOT 2a FUNCTION (2 country comparison: avg total suicide rate)
def make_plot2a(country_a = 'Any Country', country_b = 'Any Country', year_list = [0,0]):

    # Sets default values
    year_start = year_list[0]
    year_end = year_list[1]

    a = country_a
    b = country_b

    # Makes DataFrame of average suicide rates for the 2 countries
    data2a = final_df.query('suicides_per_100k_pop>0.1').query('year > @year_start & year < @year_end').query('country == @a | country == @b').groupby(['country']).agg({'suicides_per_100k_pop':'mean'})
    data2a = data2a.reset_index()

    # Rounds values to 2 decimal points
    data2a = data2a.round(2)

    # Plots chart
    chart_2a = alt.Chart(data2a).mark_bar(size = 50).encode(
        color = alt.Color('country:N'),
        x = alt.X('suicides_per_100k_pop:Q', axis = alt.Axis(title = 'Average Suicide Rate (per 100k people)', 
                                                            labelAngle = 0)),
        y = alt.Y('country:N', axis = alt.Axis(title = 'Countries', labelAngle = 0)),
        tooltip = ['suicides_per_100k_pop']
    ).properties(width = 500, height = 150,
                title = "Suicide Rate by Country"
    ).configure_title(fontSize = 15
    ).configure_axis(labelFontSize = 12,
                    titleFontSize = 12,
                    labelColor = '#4c5c5c',
                    titleColor = '#3a4242'
    )
    return chart_2a

#### DEFINE PLOT 2b FUNCTION (2 country comparison: by demographic group)
def make_plot2b(country_a = 'Any Country', country_b = 'Any Country', year_list = [0,0], demo_selection = ['female : 25-34 years']):

    # Sets default values
    year_start = year_list[0]
    year_end = year_list[1]

    a = country_a
    b = country_b
    
    #demo_selection = ['female : 05-14 years', 'female : 15-24 years', 'female : 25-34 years', 'male : 05-14 years', 'male : 15-24 years', 'male: 25-34 years']
    d = demo_selection

    # Makes DataFrame of average suicide rates for the 2 countries by demo group
    data2b = final_df
    data2b = final_df.query('suicides_per_100k_pop>0.1'
                            ).query('year > @year_start & year < @year_end'
                            ).query('country == @a | country == @b'
                            ).query('demo_group in @d')
    data2b = data2b.groupby(['demo_group', 'country']).agg({'suicides_per_100k_pop': 'mean'})
    data2b = data2b.reset_index()
    
    # Rounds values to 2 decimal points
    data2b = data2b.round(2)

    # Plots chart
    chart_2b = alt.Chart(data2b).mark_bar(size = 40).encode(
        color = alt.Color('country:N'),
        y = alt.Y('suicides_per_100k_pop:Q', axis = alt.Axis(title = 'Average Suicide Rate (per 100k people)', 
                                                            labelAngle = 0)),
        x = alt.X('country:N', axis = None),
        tooltip = ['suicides_per_100k_pop'],
        column = alt.Column('demo_group:N', title = '')
    ).properties(width = 100, height = 300,
                title = "Suicide Rate by Demographic Group"
    ).configure_title(fontSize = 15
    ).configure_axis(labelFontSize = 12,
                    titleFontSize = 12,
                    labelColor = '#4c5c5c',
                    titleColor = '#3a4242'
    )
    return chart_2b

#### SET UP LAYOUT
app.layout = html.Div([
    html.Div(
        className="app-header",
        children=[
            html.Div('Suicide Rate Dashboard', className="app-header--title")
        ]
    ),    
    #### ADD TABS TO TOP OF PAGE
    dcc.Tabs(id='tabs', value='tab1', children=[
        #### TAB 1
        dcc.Tab(label='Dashboard - Suicide Rate', value='tab-1', children = [
            
            #### MAIN PAGE HEADER
            html.H1('Tab 1 Title - need to change me'),
            html.H2('Tab 1 Subtitle - change me too please'),

            # Text for Plot 1a
            html.Div([html.P('''Step 1: This graph shows the average suicide rate over time, by continent. The dashed line shows the worldwide average for each year. You can hover over each line to see the exact suicide rate for that continent and year. ''')]),

            #### IFRAME: PLOT 1a
            html.Iframe(
                sandbox='allow-scripts',
                id='plot_1a',
                height='300',
                width='1500',
                style={'border-width': '0'},
                ################ The magic happens here
                srcDoc=make_plot_1a().to_html()
                ################ The magic happens here
                ),
            # Just to add some space
            html.Iframe(height='25', width='10',style={'border-width': '0'}),

            # Text for Plot 1b
            html.Div([html.P('''Step 2: Are there any sub-regions you are specifically interested in looking at? You can use this drop-down to select one or more sub-regions (arranged by continent) to view the average suicide rate by year. You can hover over each line to see the exact suicide rate for that sub-region and year. The dashed line shows the worldwide average for each year.''')]), 
            
            #### DROPDOWNS: PLOT 1b
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
                value='',
                multi=True,
                style=dict(width='45%',
                    verticalAlign="middle"
                    )
                ),
            
            # Add space
            html.Iframe(height='20', width='10',style={'border-width': '0'}),

            #### IFRAME: PLOT 1b
            html.Iframe(
                sandbox='allow-scripts',
                id='plot_1b',
                height='300',
                width='1500',
                style={'border-width': '0'}
                ),

             # Text for Plot 1b
            
            # Text for Plot 1c
            html.Div([html.P('''Step 3: Now that you’ve had a chance to explore the suicide rate by continent and subregion, are there any countries you’d like to look into more? Use the drop-down to select one or more countries (arranged by continent) to view the average suicide rate by year. You can hover over each line to see the exact suicide rate for that country and year. The dashed line shows the worldwide average for each year.''')]),
            
            #### DROPDOWNS: PLOT 1c
            html.H3('Suicide Rate by Country'),
            html.H4('Select one or multiple countries'),
            dcc.Dropdown(
                id='dd-country',
                options=[
                        {'label': 'Africa', 'value': 'Africa','disabled': True},
                    {'label': 'Cabo Verde', 'value': 'Cabo Verde'},
                    {'label': 'Mauritius', 'value': 'Mauritius'},
                    {'label': 'Seychelles', 'value': 'Seychelles'},
                    {'label': 'South Africa', 'value': 'South Africa'},
                    {'label': 'Americas', 'value': 'Americas','disabled': True},
                    {'label': 'Antigua and Barbuda', 'value': 'Antigua and Barbuda'},
                    {'label': 'Argentina', 'value': 'Argentina'},
                    {'label': 'Aruba', 'value': 'Aruba'},
                    {'label': 'Bahamas', 'value': 'Bahamas'},
                    {'label': 'Barbados', 'value': 'Barbados'},
                    {'label': 'Belize', 'value': 'Belize'},
                    {'label': 'Brazil', 'value': 'Brazil'},
                    {'label': 'Canada', 'value': 'Canada'},
                    {'label': 'Chile', 'value': 'Chile'},
                    {'label': 'Colombia', 'value': 'Colombia'},
                    {'label': 'Costa Rica', 'value': 'Costa Rica'},
                    {'label': 'Cuba', 'value': 'Cuba'},
                    {'label': 'Dominica', 'value': 'Dominica'},
                    {'label': 'Ecuador', 'value': 'Ecuador'},
                    {'label': 'El Salvador', 'value': 'El Salvador'},
                    {'label': 'Grenada', 'value': 'Grenada'},
                    {'label': 'Guatemala', 'value': 'Guatemala'},
                    {'label': 'Guyana', 'value': 'Guyana'},
                    {'label': 'Jamaica', 'value': 'Jamaica'},
                    {'label': 'Mexico', 'value': 'Mexico'},
                    {'label': 'Nicaragua', 'value': 'Nicaragua'},
                    {'label': 'Panama', 'value': 'Panama'},
                    {'label': 'Paraguay', 'value': 'Paraguay'},
                    {'label': 'Puerto Rico', 'value': 'Puerto Rico'},
                    {'label': 'Saint Kitts and Nevis', 'value': 'Saint Kitts and Nevis'},
                    {'label': 'Saint Lucia', 'value': 'Saint Lucia'},
                    {'label': 'Saint Vincent and Grenadines', 'value': 'Saint Vincent and Grenadines'},
                    {'label': 'Suriname', 'value': 'Suriname'},
                    {'label': 'Trinidad and Tobago', 'value': 'Trinidad and Tobago'},
                    {'label': 'United States', 'value': 'United States'},
                    {'label': 'Uruguay', 'value': 'Uruguay'},
                    {'label': 'Asia', 'value': 'Asia','disabled': True},
                    {'label': 'Armenia', 'value': 'Armenia'},
                    {'label': 'Azerbaijan', 'value': 'Azerbaijan'},
                    {'label': 'Bahrain', 'value': 'Bahrain'},
                    {'label': 'Cyprus', 'value': 'Cyprus'},
                    {'label': 'Georgia', 'value': 'Georgia'},
                    {'label': 'Israel', 'value': 'Israel'},
                    {'label': 'Japan', 'value': 'Japan'},
                    {'label': 'Kazakhstan', 'value': 'Kazakhstan'},
                    {'label': 'Kuwait', 'value': 'Kuwait'},
                    {'label': 'Kyrgyzstan', 'value': 'Kyrgyzstan'},
                    {'label': 'Macau', 'value': 'Macau'},
                    {'label': 'Maldives', 'value': 'Maldives'},
                    {'label': 'Mongolia', 'value': 'Mongolia'},
                    {'label': 'Oman', 'value': 'Oman'},
                    {'label': 'Philippines', 'value': 'Philippines'},
                    {'label': 'Qatar', 'value': 'Qatar'},
                    {'label': 'Republic of Korea', 'value': 'Republic of Korea'},
                    {'label': 'Singapore', 'value': 'Singapore'},
                    {'label': 'Sri Lanka', 'value': 'Sri Lanka'},
                    {'label': 'Thailand', 'value': 'Thailand'},
                    {'label': 'Turkey', 'value': 'Turkey'},
                    {'label': 'Turkmenistan', 'value': 'Turkmenistan'},
                    {'label': 'United Arab Emirates', 'value': 'United Arab Emirates'},
                    {'label': 'Uzbekistan', 'value': 'Uzbekistan'},
                    {'label': 'Europe', 'value': 'Europe','disabled': True},
                    {'label': 'Albania', 'value': 'Albania'},
                    {'label': 'Austria', 'value': 'Austria'},
                    {'label': 'Belarus', 'value': 'Belarus'},
                    {'label': 'Belgium', 'value': 'Belgium'},
                    {'label': 'Bosnia and Herzegovina', 'value': 'Bosnia and Herzegovina'},
                    {'label': 'Bulgaria', 'value': 'Bulgaria'},
                    {'label': 'Croatia', 'value': 'Croatia'},
                    {'label': 'Czech Republic', 'value': 'Czech Republic'},
                    {'label': 'Denmark', 'value': 'Denmark'},
                    {'label': 'Estonia', 'value': 'Estonia'},
                    {'label': 'Finland', 'value': 'Finland'},
                    {'label': 'France', 'value': 'France'},
                    {'label': 'Germany', 'value': 'Germany'},
                    {'label': 'Greece', 'value': 'Greece'},
                    {'label': 'Hungary', 'value': 'Hungary'},
                    {'label': 'Iceland', 'value': 'Iceland'},
                    {'label': 'Ireland', 'value': 'Ireland'},
                    {'label': 'Latvia', 'value': 'Latvia'},
                    {'label': 'Lithuania', 'value': 'Lithuania'},
                    {'label': 'Luxembourg', 'value': 'Luxembourg'},
                    {'label': 'Malta', 'value': 'Malta'},
                    {'label': 'Montenegro', 'value': 'Montenegro'},
                    {'label': 'Netherlands', 'value': 'Netherlands'},
                    {'label': 'Norway', 'value': 'Norway'},
                    {'label': 'Poland', 'value': 'Poland'},
                    {'label': 'Portugal', 'value': 'Portugal'},
                    {'label': 'Romania', 'value': 'Romania'},
                    {'label': 'Russian Federation', 'value': 'Russian Federation'},
                    {'label': 'San Marino', 'value': 'San Marino'},
                    {'label': 'Serbia', 'value': 'Serbia'},
                    {'label': 'Slovakia', 'value': 'Slovakia'},
                    {'label': 'Slovenia', 'value': 'Slovenia'},
                    {'label': 'Spain', 'value': 'Spain'},
                    {'label': 'Sweden', 'value': 'Sweden'},
                    {'label': 'Switzerland', 'value': 'Switzerland'},
                    {'label': 'Ukraine', 'value': 'Ukraine'},
                    {'label': 'United Kingdom', 'value': 'United Kingdom'},
                    {'label': 'Oceania', 'value': 'Oceania','disabled': True},
                    {'label': 'Australia', 'value': 'Australia'},
                    {'label': 'Fiji', 'value': 'Fiji'},
                    {'label': 'Kiribati', 'value': 'Kiribati'},
                    {'label': 'New Zealand', 'value': 'New Zealand'}
                ],
                value='Please Select a Country',
                multi=True,
                style=dict(width='45%',
                    verticalAlign="middle"
                    )
                ),

            #### IFRAME: PLOT 1c
            html.Iframe(
                sandbox='allow-scripts',
                id='plot_1c',
                height='300',
                width='1500',
                style={'border-width': '0'},
                ),
            
            # Text for Plot 1d
            html.Div([html.P('''Step 4: You may be wondering what factors other than location affect the suicide rate. Make sure you have at least one country selected above, and then this graph will automatically show the average suicide rates for 12 demographic groups (based on age and gender) over time. If you have chosen multiple countries, it will display the average suicide rate for each of the 12 demographic groups of all selected countries. You can hover over each line to see the exact suicide rate for that country/countries and demographic group. The dashed line shows the worldwide average for each year.''')]),
            
            #### IFRAME: PLOT 1d
            html.Iframe(
                sandbox='allow-scripts',
                id='plot_1d',
                height='300',
                width='1500',
                style={'border-width': '0'},
                ),

            # Add space
            html.Iframe(height='25', width='10',style={'border-width': '0'}),
            ]),

        #### TAB 2
        dcc.Tab(label='Country Comparison', value='tab-2', children = [

            #### MAIN PAGE HEADER
            html.H1('Tab 2 Title - need to change me'),
            html.H2('Tab 2 Subtitle - change me too please'),

            # Add space
            html.Iframe(height='20', width='10',style={'border-width': '0'}),

            # Text for Plot 2a - Country Dropdowns
            html.Div([html.P('''Step 1: Pick 2 countries that you would like to compare. Select them in each dropdown (1 country per dropdown).''')]),

            #### DROPDOWNS: PLOT 2a
            dcc.Dropdown(
                id = 'country_a_dropdown',
                options=[
                    {'label': 'Albania', 'value': 'Albania'},
                    {'label': 'Antigua and Barbuda', 'value': 'Antigua and Barbuda'},
                    {'label': 'Argentina', 'value': 'Argentina'},
                    {'label': 'Armenia', 'value': 'Armenia'},
                    {'label': 'Aruba', 'value': 'Aruba'},
                    {'label': 'Australia', 'value': 'Australia'},
                    {'label': 'Austria', 'value': 'Austria'},
                    {'label': 'Azerbaijan', 'value': 'Azerbaijan'},
                    {'label': 'Bahamas', 'value': 'Bahamas'},
                    {'label': 'Bahrain', 'value': 'Bahrain'},
                    {'label': 'Barbados', 'value': 'Barbados'},
                    {'label': 'Belarus', 'value': 'Belarus'},
                    {'label': 'Belgium', 'value': 'Belgium'},
                    {'label': 'Belize', 'value': 'Belize'},
                    {'label': 'Bosnia and Herzegovina', 'value': 'Bosnia and Herzegovina'},
                    {'label': 'Brazil', 'value': 'Brazil'},
                    {'label': 'Bulgaria', 'value': 'Bulgaria'},
                    {'label': 'Cabo Verde', 'value': 'Cabo Verde'},
                    {'label': 'Canada', 'value': 'Canada'},
                    {'label': 'Chile', 'value': 'Chile'},
                    {'label': 'Colombia', 'value': 'Colombia'},
                    {'label': 'Costa Rica', 'value': 'Costa Rica'},
                    {'label': 'Croatia', 'value': 'Croatia'},
                    {'label': 'Cuba', 'value': 'Cuba'},
                    {'label': 'Cyprus', 'value': 'Cyprus'},
                    {'label': 'Czech Republic', 'value': 'Czech Republic'},
                    {'label': 'Denmark', 'value': 'Denmark'},
                    {'label': 'Dominica', 'value': 'Dominica'},
                    {'label': 'Ecuador', 'value': 'Ecuador'},
                    {'label': 'El Salvador', 'value': 'El Salvador'},
                    {'label': 'Estonia', 'value': 'Estonia'},
                    {'label': 'Fiji', 'value': 'Fiji'},
                    {'label': 'Finland', 'value': 'Finland'},
                    {'label': 'France', 'value': 'France'},
                    {'label': 'Georgia', 'value': 'Georgia'},
                    {'label': 'Germany', 'value': 'Germany'},
                    {'label': 'Greece', 'value': 'Greece'},
                    {'label': 'Grenada', 'value': 'Grenada'},
                    {'label': 'Guatemala', 'value': 'Guatemala'},
                    {'label': 'Guyana', 'value': 'Guyana'},
                    {'label': 'Hungary', 'value': 'Hungary'},
                    {'label': 'Iceland', 'value': 'Iceland'},
                    {'label': 'Ireland', 'value': 'Ireland'},
                    {'label': 'Israel', 'value': 'Israel'},
                    {'label': 'Italy', 'value': 'Italy'},
                    {'label': 'Jamaica', 'value': 'Jamaica'},
                    {'label': 'Japan', 'value': 'Japan'},
                    {'label': 'Kazakhstan', 'value': 'Kazakhstan'},
                    {'label': 'Kiribati', 'value': 'Kiribati'},
                    {'label': 'Kuwait', 'value': 'Kuwait'},
                    {'label': 'Kyrgyzstan', 'value': 'Kyrgyzstan'},
                    {'label': 'Latvia', 'value': 'Latvia'},
                    {'label': 'Lithuania', 'value': 'Lithuania'},
                    {'label': 'Luxembourg', 'value': 'Luxembourg'},
                    {'label': 'Macau', 'value': 'Macau'},
                    {'label': 'Maldives', 'value': 'Maldives'},
                    {'label': 'Malta', 'value': 'Malta'},
                    {'label': 'Mauritius', 'value': 'Mauritius'},
                    {'label': 'Mexico', 'value': 'Mexico'},
                    {'label': 'Mongolia', 'value': 'Mongolia'},
                    {'label': 'Montenegro', 'value': 'Montenegro'},
                    {'label': 'Netherlands', 'value': 'Netherlands'},
                    {'label': 'New Zealand', 'value': 'New Zealand'},
                    {'label': 'Nicaragua', 'value': 'Nicaragua'},
                    {'label': 'Norway', 'value': 'Norway'},
                    {'label': 'Oman', 'value': 'Oman'},
                    {'label': 'Panama', 'value': 'Panama'},
                    {'label': 'Paraguay', 'value': 'Paraguay'},
                    {'label': 'Philippines', 'value': 'Philippines'},
                    {'label': 'Poland', 'value': 'Poland'},
                    {'label': 'Portugal', 'value': 'Portugal'},
                    {'label': 'Puerto Rico', 'value': 'Puerto Rico'},
                    {'label': 'Qatar', 'value': 'Qatar'},
                    {'label': 'Republic of Korea', 'value': 'Republic of Korea'},
                    {'label': 'Romania', 'value': 'Romania'},
                    {'label': 'Russian Federation', 'value': 'Russian Federation'},
                    {'label': 'Saint Kitts and Nevis', 'value': 'Saint Kitts and Nevis'},
                    {'label': 'Saint Lucia', 'value': 'Saint Lucia'},
                    {'label': 'Saint Vincent and Grenadines', 'value': 'Saint Vincent and Grenadines'},
                    {'label': 'San Marino', 'value': 'San Marino'},
                    {'label': 'Serbia', 'value': 'Serbia'},
                    {'label': 'Seychelles', 'value': 'Seychelles'},
                    {'label': 'Singapore', 'value': 'Singapore'},
                    {'label': 'Slovakia', 'value': 'Slovakia'},
                    {'label': 'Slovenia', 'value': 'Slovenia'},
                    {'label': 'South Africa', 'value': 'South Africa'},
                    {'label': 'Spain', 'value': 'Spain'},
                    {'label': 'Sri Lanka', 'value': 'Sri Lanka'},
                    {'label': 'Suriname', 'value': 'Suriname'},
                    {'label': 'Sweden', 'value': 'Sweden'},
                    {'label': 'Switzerland', 'value': 'Switzerland'},
                    {'label': 'Thailand', 'value': 'Thailand'},
                    {'label': 'Trinidad and Tobago', 'value': 'Trinidad and Tobago'},
                    {'label': 'Turkey', 'value': 'Turkey'},
                    {'label': 'Turkmenistan', 'value': 'Turkmenistan'},
                    {'label': 'Ukraine', 'value': 'Ukraine'},
                    {'label': 'United Arab Emirates', 'value': 'United Arab Emirates'},
                    {'label': 'United Kingdom', 'value': 'United Kingdom'},
                    {'label': 'United States', 'value': 'United States'},
                    {'label': 'Uruguay', 'value': 'Uruguay'},
                    {'label': 'Uzbekistan', 'value': 'Uzbekistan'}
                ],
                value = 'United States',
                style = dict(width = '45%',
                        verticalAlign = 'middle')
            ),

            dcc.Dropdown(
                id = 'country_b_dropdown',
                options=[
                    {'label': 'Albania', 'value': 'Albania'},
                    {'label': 'Antigua and Barbuda', 'value': 'Antigua and Barbuda'},
                    {'label': 'Argentina', 'value': 'Argentina'},
                    {'label': 'Armenia', 'value': 'Armenia'},
                    {'label': 'Aruba', 'value': 'Aruba'},
                    {'label': 'Australia', 'value': 'Australia'},
                    {'label': 'Austria', 'value': 'Austria'},
                    {'label': 'Azerbaijan', 'value': 'Azerbaijan'},
                    {'label': 'Bahamas', 'value': 'Bahamas'},
                    {'label': 'Bahrain', 'value': 'Bahrain'},
                    {'label': 'Barbados', 'value': 'Barbados'},
                    {'label': 'Belarus', 'value': 'Belarus'},
                    {'label': 'Belgium', 'value': 'Belgium'},
                    {'label': 'Belize', 'value': 'Belize'},
                    {'label': 'Bosnia and Herzegovina', 'value': 'Bosnia and Herzegovina'},
                    {'label': 'Brazil', 'value': 'Brazil'},
                    {'label': 'Bulgaria', 'value': 'Bulgaria'},
                    {'label': 'Cabo Verde', 'value': 'Cabo Verde'},
                    {'label': 'Canada', 'value': 'Canada'},
                    {'label': 'Chile', 'value': 'Chile'},
                    {'label': 'Colombia', 'value': 'Colombia'},
                    {'label': 'Costa Rica', 'value': 'Costa Rica'},
                    {'label': 'Croatia', 'value': 'Croatia'},
                    {'label': 'Cuba', 'value': 'Cuba'},
                    {'label': 'Cyprus', 'value': 'Cyprus'},
                    {'label': 'Czech Republic', 'value': 'Czech Republic'},
                    {'label': 'Denmark', 'value': 'Denmark'},
                    {'label': 'Dominica', 'value': 'Dominica'},
                    {'label': 'Ecuador', 'value': 'Ecuador'},
                    {'label': 'El Salvador', 'value': 'El Salvador'},
                    {'label': 'Estonia', 'value': 'Estonia'},
                    {'label': 'Fiji', 'value': 'Fiji'},
                    {'label': 'Finland', 'value': 'Finland'},
                    {'label': 'France', 'value': 'France'},
                    {'label': 'Georgia', 'value': 'Georgia'},
                    {'label': 'Germany', 'value': 'Germany'},
                    {'label': 'Greece', 'value': 'Greece'},
                    {'label': 'Grenada', 'value': 'Grenada'},
                    {'label': 'Guatemala', 'value': 'Guatemala'},
                    {'label': 'Guyana', 'value': 'Guyana'},
                    {'label': 'Hungary', 'value': 'Hungary'},
                    {'label': 'Iceland', 'value': 'Iceland'},
                    {'label': 'Ireland', 'value': 'Ireland'},
                    {'label': 'Israel', 'value': 'Israel'},
                    {'label': 'Italy', 'value': 'Italy'},
                    {'label': 'Jamaica', 'value': 'Jamaica'},
                    {'label': 'Japan', 'value': 'Japan'},
                    {'label': 'Kazakhstan', 'value': 'Kazakhstan'},
                    {'label': 'Kiribati', 'value': 'Kiribati'},
                    {'label': 'Kuwait', 'value': 'Kuwait'},
                    {'label': 'Kyrgyzstan', 'value': 'Kyrgyzstan'},
                    {'label': 'Latvia', 'value': 'Latvia'},
                    {'label': 'Lithuania', 'value': 'Lithuania'},
                    {'label': 'Luxembourg', 'value': 'Luxembourg'},
                    {'label': 'Macau', 'value': 'Macau'},
                    {'label': 'Maldives', 'value': 'Maldives'},
                    {'label': 'Malta', 'value': 'Malta'},
                    {'label': 'Mauritius', 'value': 'Mauritius'},
                    {'label': 'Mexico', 'value': 'Mexico'},
                    {'label': 'Mongolia', 'value': 'Mongolia'},
                    {'label': 'Montenegro', 'value': 'Montenegro'},
                    {'label': 'Netherlands', 'value': 'Netherlands'},
                    {'label': 'New Zealand', 'value': 'New Zealand'},
                    {'label': 'Nicaragua', 'value': 'Nicaragua'},
                    {'label': 'Norway', 'value': 'Norway'},
                    {'label': 'Oman', 'value': 'Oman'},
                    {'label': 'Panama', 'value': 'Panama'},
                    {'label': 'Paraguay', 'value': 'Paraguay'},
                    {'label': 'Philippines', 'value': 'Philippines'},
                    {'label': 'Poland', 'value': 'Poland'},
                    {'label': 'Portugal', 'value': 'Portugal'},
                    {'label': 'Puerto Rico', 'value': 'Puerto Rico'},
                    {'label': 'Qatar', 'value': 'Qatar'},
                    {'label': 'Republic of Korea', 'value': 'Republic of Korea'},
                    {'label': 'Romania', 'value': 'Romania'},
                    {'label': 'Russian Federation', 'value': 'Russian Federation'},
                    {'label': 'Saint Kitts and Nevis', 'value': 'Saint Kitts and Nevis'},
                    {'label': 'Saint Lucia', 'value': 'Saint Lucia'},
                    {'label': 'Saint Vincent and Grenadines', 'value': 'Saint Vincent and Grenadines'},
                    {'label': 'San Marino', 'value': 'San Marino'},
                    {'label': 'Serbia', 'value': 'Serbia'},
                    {'label': 'Seychelles', 'value': 'Seychelles'},
                    {'label': 'Singapore', 'value': 'Singapore'},
                    {'label': 'Slovakia', 'value': 'Slovakia'},
                    {'label': 'Slovenia', 'value': 'Slovenia'},
                    {'label': 'South Africa', 'value': 'South Africa'},
                    {'label': 'Spain', 'value': 'Spain'},
                    {'label': 'Sri Lanka', 'value': 'Sri Lanka'},
                    {'label': 'Suriname', 'value': 'Suriname'},
                    {'label': 'Sweden', 'value': 'Sweden'},
                    {'label': 'Switzerland', 'value': 'Switzerland'},
                    {'label': 'Thailand', 'value': 'Thailand'},
                    {'label': 'Trinidad and Tobago', 'value': 'Trinidad and Tobago'},
                    {'label': 'Turkey', 'value': 'Turkey'},
                    {'label': 'Turkmenistan', 'value': 'Turkmenistan'},
                    {'label': 'Ukraine', 'value': 'Ukraine'},
                    {'label': 'United Arab Emirates', 'value': 'United Arab Emirates'},
                    {'label': 'United Kingdom', 'value': 'United Kingdom'},
                    {'label': 'United States', 'value': 'United States'},
                    {'label': 'Uruguay', 'value': 'Uruguay'},
                    {'label': 'Uzbekistan', 'value': 'Uzbekistan'}
                ],
                value = 'Canada',
                style = dict(width = '45%',
                        verticalAlign = 'middle')
            ),

            # Add space
            html.Iframe(height='20', width='10',style={'border-width': '0'}),

            # Text for Plot 2a - Year Slider
            html.Div([html.P('''Step 2: Pick a range of years that you are interested in looking into. Use the slider to select this range. The graph below will show the average suicide rate for the year range selected for each of the 2 countries. ''')]),
            
            dcc.RangeSlider(
                id='my-range-slider',
                min = 1984,
                max = 2016,
                step = None,
                marks = {1986: '1986', 
                            1987: '1987',
                            1988: '1988',
                            1989: '1989',
                            1990: '1990',
                            1991: '1991',
                            1992: '1992',
                            1993: '1993',
                            1994: '1994',
                            1995: '1995',
                            1996: '1996',
                            1997: '1997',
                            1998: '1998',
                            1999: '1999',
                            2000: '2000',
                            2001: '2001',
                            2002: '2002',
                            2003: '2003',
                            2004: '2004',
                            2005: '2005',
                            2006: '2006',
                            2007: '2007',
                            2008: '2008',
                            2009: '2009',
                            2010: '2010',
                            2011: '2011',
                            2012: '2012',
                            2013: '2013',
                            2014: '2014'},
                value = [1986, 2014]
                ),

            # Add space
            html.Iframe(height='20', width='10',style={'border-width': '0'}),

            #### IFRAME: PLOT 2a
            html.Iframe(
                sandbox='allow-scripts',
                id='plot2a',
                height='250',
                width='1500',
                style={'border-width': '0'},
                ),
            
             # Text for Plot 2b
            html.Div([html.P('''Step 3: You might be wondering about how the suicide rate for the 2 countries changes by demographic group. You can select one or more demographic groups (by gender and age) to see the different suicide rates by demographic group for your 2 chosen countries. ''')]),

            #### DROPDOWNS: PLOT 2b
            dcc.Checklist(
                id = 'demo_checklist',
                options = [
                    {'label': 'female : 05-14 years', 'value': 'female : 05-14 years'},
                    {'label': 'female : 15-24 years', 'value': 'female : 15-24 years'},
                    {'label': 'female : 25-34 years', 'value': 'female : 25-34 years'},
                    {'label': 'female : 35-54 years', 'value': 'female : 35-54 years'},
                    {'label': 'female : 54-74 years', 'value': 'female : 54-74 years'},
                    {'label': 'female : 75+ years', 'value': 'female : 75+ years'},
                    {'label': 'male : 05-14 years', 'value': 'male : 05-14 years'},
                    {'label': 'male : 15-24 years', 'value': 'male : 15-24 years'},
                    {'label': 'male : 25-34 years', 'value': 'male : 25-34 years'},
                    {'label': 'male : 35-54 years', 'value': 'male : 35-54 years'},
                    {'label': 'male : 54-74 years', 'value': 'male : 54-74 years'},
                    {'label': 'male : 75+ years', 'value': 'male : 75+ years'},
                ],
                value = ['female : 25-34 years'],
                labelStyle={'display': 'inline-block', 'text-align': 'justify'}
            ),

            #### IFRAME: PLOT 2b
            html.Iframe(
                sandbox='allow-scripts',
                id='plot2b',
                height='500',
                width='1200',
                style={'border-width': '0'},
                ),
        ]),
    ]),    

    #### MAIN TAB TEXT
    html.Div([
        html.P('''
        Welcome to our virtual dashboard! The purpose of this app is to help you visualize suicide rates in different locations over time, and how a variety of different factors (i.e. age, gender, and year) affect these rates. 
        We have 2 main questions we are trying to answer: 
        '''),
        html.P('''
        Tab 1: How does the suicide rate change over time, and what effect does continent, region, country, age, and gender have on this? 
        '''),
        html.P('''
        Tab 2: How does the suicide rate of one coountry compare against the suicide rate of another country? 
        '''),
        html.P('''
        Please click on a tab to get started! 
        '''),    
        html.P('''
        If you have thoughts of suicide, please do not hesitate to reach out to your local Crisis Centre or Suicide Prevention Hotline. In British Columbia, you can get help by visiting www.crisiscentre.bc.ca or by calling 1-800-784-2433 from anywhere in the province.
        ''')
    ]),


])

#### DECORATOR: PLOT 1B
@app.callback(
    dash.dependencies.Output('plot_1b', 'srcDoc'),
    [dash.dependencies.Input('dd-chart', 'value')])
def update_plot_1b(sub_region):
    updated_plot_1b = make_plot_1b(sub_region).to_html()
    return updated_plot_1b

#### DECORATOR: PLOT 1C
@app.callback(
    dash.dependencies.Output('plot_1c', 'srcDoc'),
    [dash.dependencies.Input('dd-country', 'value')])
def update_plot_1c(country):
    updated_plot_1c = make_plot_1c(country).to_html()
    return updated_plot_1c

#### DECORATOR: PLOT 1D
@app.callback(
    dash.dependencies.Output('plot_1d', 'srcDoc'),
    [dash.dependencies.Input('dd-country', 'value')])
def update_plot_1d(country):
    updated_plot_1d = make_plot_1d(country).to_html()
    return updated_plot_1d

#### DECORATOR: PLOT 2a
@app.callback(
    dash.dependencies.Output('plot2a', 'srcDoc'), 
    [dash.dependencies.Input('country_a_dropdown', 'value'),
     dash.dependencies.Input('country_b_dropdown', 'value'),
     dash.dependencies.Input('my-range-slider', 'value')])
def update_plot2a(country_a, country_b, year_list):
    updated_plot_2a = make_plot2a(country_a, country_b, year_list).to_html()
    return updated_plot_2a 

#### DECORATOR: PLOT 2b
@app.callback(
    dash.dependencies.Output('plot2b', 'srcDoc'), 
    [dash.dependencies.Input('country_a_dropdown', 'value'),
     dash.dependencies.Input('country_b_dropdown', 'value'),
     dash.dependencies.Input('my-range-slider', 'value'),
     dash.dependencies.Input('demo_checklist', 'value')
     ])

def update_plot2b(country_a, country_b, year_list, demo_selection):
    updated_plot_2b = make_plot2b(country_a, country_b, year_list, demo_selection).to_html()
    return updated_plot_2b

if __name__ == '__main__':
    app.run_server(debug=True)