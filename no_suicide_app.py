import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output, State
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
import altair as alt
import vega_datasets
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, assets_folder='assets', external_stylesheets=external_stylesheets)
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
general_data['Label'] = 'Worldwide Average'

#### DEFINE PLOT 1a FUNCTION (continent)
def make_plot_1a():
    # Create a plot 1a
    source = plot_a_data.round(1)

    nearest = alt.selection(type='single', nearest=True, on='mouseover',
                        fields=['year'],empty='none')
    line= alt.Chart(source).mark_line(point=False).encode(
        x = alt.X('year:O',axis=alt.Axis(title='Year', grid=False,labelAngle=-45)),
        y = alt.Y('suicides_per_100k_pop',axis=alt.Axis(title='Suicides per 100 k pop'),scale=alt.Scale(zero=True)),
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
    line2 = alt.Chart(general_data).mark_line(stroke="black",point=False,strokeDash=[10],interpolate ='monotone',size =2,color="#FFAA00").encode(
    x = alt.X('year:O',axis=alt.Axis(title='Year',labelAngle=-45)),
    y = alt.Y('suicides_per_100k_pop',axis=alt.Axis(title='Suicides per 100 k pop'),scale=alt.Scale(zero=True)),
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
                        fields=['year'],empty='none')
    line= alt.Chart(source).mark_line(point=False).encode(
        x = alt.X('year:O',axis=alt.Axis(title='Year',labelAngle=-45)),
        y = alt.Y('suicides_per_100k_pop',axis=alt.Axis(title='Suicides per 100 k pop'),scale=alt.Scale(zero=True)),
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
    line2= alt.Chart(general_data).mark_line(stroke="black",point=False,strokeDash=[10],interpolate ='monotone',size =2,color="#FFAA00").encode(
    x = alt.X('year:O',axis=alt.Axis(title='Year',labelAngle=-45)),
    y = alt.Y('suicides_per_100k_pop',axis=alt.Axis(title='Suicides per 100 k pop'),scale=alt.Scale(zero=True)),
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

#### DROPDOWN LISTS FOR 1B

regions = ['Africa',
            'Eastern Africa',
            'Middle Africa',
            'Northern Africa',
            'Southern Africa',
            'Western Africa',
            'Americas',
            'Caribbean',
            'Central America',
            'Northern America',
            'South America',
            'Asia',
            'Central Asia',
            'Eastern Asia',
            'South-Eastern Asia',
            'Southern Asia',
            'Western Asia',
            'Europe',
            'Eastern Europe',
            'Northern Europe',
            'Southern Europe',
            'Western Europe',
            'Oceania',
            'Australia and New Zealand',
            'Melanesia',
            'Micronemia',
            'Polynesia']

continents = ['Africa',
            'Americas',
            'Asia',
            'Europe',
            'Oceania']

#### DEFINE PLOT 1c FUNCTION (countries)
def make_plot_1c(selected_country = 'Select a Country Please'):

    # Update Data source based on user selection:
    a = selected_country
    plot_c_data = final_df.query('country in @a').query('suicides_per_100k_pop>0.1').query('year < 2015 and year > 1986').groupby(['year','country'],as_index = False).agg({"suicides_per_100k_pop":"mean"})

    # Create a plot C
    source = plot_c_data.round(1)

    nearest = alt.selection(type='single', nearest=True, on='mouseover',
                        fields=['year'],empty='none')
    line= alt.Chart(source).mark_line(point=False).encode(
        x = alt.X('year:O',axis=alt.Axis(title='Year',labelAngle=-45)),
        y = alt.Y('suicides_per_100k_pop',axis=alt.Axis(title='Suicides per 100 k pop'),scale=alt.Scale(zero=True)),
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
    line2= alt.Chart(general_data).mark_line(stroke="black",point=False,strokeDash=[10],interpolate ='monotone',size =2,color="#FFAA00").encode(
    x = alt.X('year:O',axis=alt.Axis(title='Year',labelAngle=-45)),
    y = alt.Y('suicides_per_100k_pop',axis=alt.Axis(title='Suicides per 100 k pop'),scale=alt.Scale(zero=True)),
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

#### DROPDOWN LIST FOR 1c
countries_1 = ['Africa', 
                'Cabo Verde',
                 'Mauritius', 
                 'Seychelles',
                 'South Africa',
                 'Americas',
                 'Antigua and Barbuda',
                 'Argentina',
                 'Aruba',
                 'Bahamas',
                 'Barbados',
                 'Belize',
                 'Brazil',
                 'Canada',
                 'Chile',
                 'Colombia',
                 'Costa Rica',
                 'Cuba',
                 'Dominica',
                 'Ecuador',
                 'El Salvador',
                 'Grenada',
                 'Guyana',
                 'Jamaica',
                 'Mexico',
                 'Nicaragua',
                 'Panama',
                 'Paraguay',
                 'Puerto Rico',
                 'Saint Kitts and Nevis',
                 'Saint Lucia',
                 'Saint Vincent and Grenadines',
                 'Suriname',
                 'Trinidad and Tobago',
                 'United States',
                 'Uruguay',
                 'Asia',
                 'Armenia',
                 'Azerbaijan',
                 'Bahrain',
                 'Cyprus',
                 'Georgia',
                 'Israel',
                 'Japan',
                 'Kazakhstan',
                 'Kuwait',
                 'Kyrgyzstan',
                 'Macau',
                 'Maldives',
                 'Mongolia',
                 'Oman',
                 'Philippines',
                 'Qatar',
                 'Republic of Korea',
                 'Singapore',
                 'Sri Lanka',
                 'Thailand',
                 'Turkey',
                 'Turkmenistan',
                 'United Arab Emirates',
                 'Uzbekistan',
                 'Europe',
                 'Albania',
                 'Austria',
                 'Belarus',
                 'Belgium',
                 'Bosnia and Herzegovina',
                 'Bulgaria',
                 'Croatia',
                 'Czech Republic',
                 'Denmark',
                 'Estonia',
                 'Finland',
                 'France',
                 'Germany',
                 'Greece',
                 'Hungary',
                 'Iceland',
                 'Ireland',
                 'Latvia',
                 'Lithuania',
                 'Luxembourg',
                 'Malta',
                 'Montenegro',
                 'Netherlands',
                 'Norway',
                 'Poland',
                 'Portugal',
                 'Romania',
                 'Russian Federation',
                 'San Marino',
                 'Serbia',
                 'Slovakia',
                 'Slovenia',
                 'Spain',
                 'Sweden',
                 'Switzerland',
                 'Ukraine',
                 'United Kingdom',
                 'Oceania',
                 'Australia',
                 'Fiji',
                 'Kiribati',
                 'New Zealand'] 

regions_1 = ['Africa',
            'Americas',
            'Asia',
            'Europe',
            'Oceania']

#### DEFINE PLOT 1d FUNCTION (countries)
def make_plot_1d(selected_country = 'Select a Country Please'):

    # Update Data source based on user selection:
    a = selected_country
    plot_d_data = final_df.query('country in @a').query('suicides_per_100k_pop>0.1').query('year < 2015 and year > 1986').groupby(['year','demo_group'],as_index = False).agg({"suicides_per_100k_pop":"mean"})
    
    # Create a plot D
    source = plot_d_data.round(1)

    nearest = alt.selection(type='single', nearest=True, on='mouseover',
                        fields=['year'],empty='none')
    line= alt.Chart(source).mark_line(point=False).encode(
        x = alt.X('year:O',axis=alt.Axis(title='Year',labelAngle=-45)),
        y = alt.Y('suicides_per_100k_pop',axis=alt.Axis(title='Suicides per 100 k pop'),scale=alt.Scale(zero=True)),
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
    line2= alt.Chart(general_data).mark_line(stroke="black",point=False,strokeDash=[10],interpolate ='monotone',size =2,color="#FFAA00").encode(
    x = alt.X('year:O',axis=alt.Axis(title='Year',labelAngle=-45)),
    y = alt.Y('suicides_per_100k_pop',axis=alt.Axis(title='Suicides per 100 k pop'),scale=alt.Scale(zero=True)),
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
        y = alt.Y('suicides_per_100k_pop:Q', axis = alt.Axis(title = 'Average Suicide Rate (per 100k pop)', 
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

#### COUNTRIES_2 LIST FOR TAB 2 DROPDOWN
countries_2 = ['Albania', 
                    'Antigua and Barbuda', 
                    'Argentina',
                    'Armenia',
                    'Aruba',
                    'Australia',
                    'Austria',
                    'Azerbaijan',
                    'Bahamas',
                    'Bahrain',
                    'Barbados',
                    'Belarus',
                    'Belgium',
                    'Belize',
                    'Bosnia and Herzegovina',
                    'Brazil',
                    'Bulgaria',
                    'Cabo Verde',
                    'Canada',
                    'Chile',
                    'Colombia',
                    'Costa Rica',
                    'Croatia',
                    'Cuba',
                    'Cyprus',
                    'Czech Republic',
                    'Denmark',
                    'Dominica',
                    'Ecuador',
                    'El Salvador',
                    'Estonia',
                    'Fiji',
                    'Finland',
                    'France',
                    'Georgia',
                    'Germany',
                    'Greece',
                    'Grenada',
                    'Guatemala',
                    'Guyana',
                    'Hungary',
                    'Iceland',
                    'Ireland',
                    'Israel',
                    'Italy',
                    'Jamaica',
                    'Japan',
                    'Kazakhstan',
                    'Kiribati',
                    'Kuwait',
                    'Kyrgyzstan',
                    'Latvia',
                    'Lithuania',
                    'Luxembourg',
                    'Macau',
                    'Maldives',
                    'Malta',
                    'Mauritius',
                    'Mexico',
                    'Mongolia',
                    'Montenegro',
                    'Netherlands',
                    'New Zealand',
                    'Nicaragua',
                    'Norway',
                    'Oman',
                    'Panama',
                    'Paraguay',
                    'Philippines',
                    'Poland',
                    'Portugal',
                    'Puerto Rico',
                    'Qatar',
                    'Republic of Korea'
                    'Romania',
                    'Russian Federation',
                    'Saint Kitts and Nevis',
                    'Saint Lucia',
                    'Saint Vincent and Grenadines',
                    'San Marino',
                    'Serbia',
                    'Seychelles',
                    'Singapore',
                    'Slovakia',
                    'Slovenia',
                    'South Africa',
                    'Spain',
                    'Sri Lanka',
                    'Suriname',
                    'Sweden',
                    'Switzerland',
                    'Thailand',
                    'Trinidad and Tobago',
                    'Turkey',
                    'Turkmenistan',
                    'Ukraine',
                    'United Arab Emirates',
                    'United Kingdom',
                    'United States',
                    'Uruguay',
                    'Uzbekistan']


#### SET UP LAYOUT
app.layout = html.Div([
    dbc.Jumbotron([
        dbc.Container([
            html.H1("Understanding Suicide Rates", className = 'display-3'),
            dcc.Markdown(
                '''
                The purpose of this app is to help you visualize suicide rates in different locations over time, and see how a variety of different factors (i.e. age, gender, and year) affect these rates. 
                We have 2 main questions we are trying to answer: 

                **Tab 1**: How does the suicide rate change over time, and what effect does continent, region, country, age, and gender have on this?  
                **Tab 2**: How does the suicide rate of one country compare against the suicide rate of another country? 

                Please click on a tab to get started! 

                **If you have thoughts of suicide, please reach out to your local Crisis Centre or Suicide Prevention Hotline.**  
                **In BC, you can get help by visiting [www.crisiscentre.bc.ca](https://crisiscentre.bc.ca) or by calling 1-800-784-2433 from anywhere in the province.**
                '''
                )
        ],
        )
    ]), 

    #### ADD TABS TO TOP OF PAGE
    dcc.Tabs(id='tabs', value='tab1', children=[
        #### TAB 1
        dcc.Tab(label='Tab 1: Continent-Region-Country Analysis', value='tab-1', children = [
            
            #### MAIN PAGE HEADER
            #html.H1('Understanding Suicide Rate Historical Behavior'),
            html.H2('Continent - Region - Country Analysis'),
             # Just to add some space
            html.Iframe(height='5', width='05',style={'border-width': '0'}),
            html.H3('Suicide Rate by Continent'),


            # Text for Plot 1a
            html.Div([dcc.Markdown('''**Step 1:** This graph shows the average suicide rate over time, by continent.  
            The dashed line shows the worldwide average for each year.  
            You can hover over each line to see the exact suicide rate for that continent and year. ''')]),

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

            
            
            #### DROPDOWNS: PLOT 1b
            html.H3('Suicide Rate by Region'),
            # Text for Plot 1b
            html.Div([dcc.Markdown('''**Step 2:** Are there any sub-regions you are specifically interested in looking at?  
            You can use this drop-down to select one or more sub-regions (arranged by continent) to view the average suicide rate by year.  
            You can hover over each line to see the exact suicide rate for that sub-region and year. The dashed line shows the worldwide average for each year.''')]), 
            html.H4('Select one or multiple Regions'),

            dcc.Dropdown(
                id='dd-chart',
                options=[{'label' : region, 'value' : region, 'disabled' : False if region not in continents else True} for region in regions],
                value = 'Please select a region',
                multi = True, 
                style = dict(width = '45%',
                        verticalAlign = 'middle')
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
            html.Iframe(height='25', width='10',style={'border-width': '0'}),
            
            #### DROPDOWNS: PLOT 1c
            html.H3('Suicide Rate by Country'),
            html.Div([dcc.Markdown('''**Step 3:** Now that you’ve had a chance to explore the suicide rate by continent and subregion, are there any countries you’d like to look into more?  
            Use the drop-down to select one or more countries (arranged by continent) to view the average suicide rate by year.  
            You can hover over each line to see the exact suicide rate for that country and year. The dashed line shows the worldwide average for each year.''')]),
            html.H4('Select one or multiple countries'),


            dcc.Dropdown(
                id='dd-country',
                options=[{'label' : country, 'value' : country, 'disabled' : False if country not in continents else True} for country in countries_1],
                value = 'Please select a country',
                multi = True, 
                style = dict(width = '45%',
                        verticalAlign = 'middle')
            ), 

            #### IFRAME: PLOT 1c
            html.Iframe(
                sandbox='allow-scripts',
                id='plot_1c',
                height='300',
                width='1500',
                style={'border-width': '0'},
                ),
            html.Iframe(height='25', width='10',style={'border-width': '0'}),
            # Text for Plot 1d
            html.H3('Suicide Rate by Demographic Groups'),
            html.Div([dcc.Markdown('''**Step 4:** You may be wondering what factors other than location affect the suicide rate.  
            Make sure you have at least one country selected above, and then this graph will automatically show the average suicide rates for 12 demographic groups (based on age and gender) over time.  
            If you have chosen multiple countries, it will display the average suicide rate for each of the 12 demographic groups of all selected countries.  
            You can hover over each line to see the exact suicide rate for that country/countries and demographic group. The dashed line shows the worldwide average for each year.''')]),
            
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
        dcc.Tab(label='Tab 2: Two Country Comparison', value='tab-2', children = [

            #### MAIN PAGE HEADER
            #html.H1('Understanding Suicide Rate Historical Behavior'),
            html.H2('Two Country Comparison'),

            # Add space
            html.Iframe(height='20', width='10',style={'border-width': '0'}),

            # Text for Plot 2a - Country Dropdowns
            html.Div([dcc.Markdown('''**Step 1:** Pick 2 countries that you would like to compare. Select them in each dropdown (1 country per dropdown).''')]),

            #### DROPDOWNS: PLOT 2a
            dcc.Dropdown(
                id = 'country_a_dropdown',
                options= [{'label': country, 'value' : country} for country in countries_2],
                value = 'United States',
                style = dict(width = '45%',
                        verticalAlign = 'middle')
            ),

            dcc.Dropdown(
                id = 'country_b_dropdown',
                options= [{'label': country, 'value' : country} for country in countries_2],
                value = 'Canada',
                style = dict(width = '45%',
                        verticalAlign = 'middle')
            ),

            # Add space
            html.Iframe(height='20', width='10',style={'border-width': '0'}),

            # Text for Plot 2a - Year Slider
            html.Div([dcc.Markdown('''**Step 2:** Pick a range of years that you are interested in looking into. Use the slider to select this range.  
            The graph below will show the average suicide rate for the year range selected for each of the 2 countries.''')]),
            
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
            html.Iframe(height='40', width='10',style={'border-width': '0'}),

            #### IFRAME: PLOT 2a
            html.Iframe(
                sandbox='allow-scripts',
                id='plot2a',
                height='250',
                width='1500',
                style={'border-width': '0'},
                ),
            
             # Text for Plot 2b
            html.Div([dcc.Markdown('''**Step 3:** You might be wondering about how the suicide rate for the 2 countries changes by demographic group.  
            You can select one or more demographic groups (gender and age) to see the different suicide rates by demographic group for your 2 chosen countries.''')]),

            #### DROPDOWNS: PLOT 2b
            dcc.Checklist(
                id = 'demo_checklist',
                options = [
                    {'label': 'female : 05-14 years', 'value': 'female : 05-14 years'},
                    {'label': 'female : 15-24 years', 'value': 'female : 15-24 years'},
                    {'label': 'female : 25-34 years', 'value': 'female : 25-34 years'},
                    {'label': 'female : 35-54 years', 'value': 'female : 35-54 years'},
                    {'label': 'female : 55-74 years', 'value': 'female : 55-74 years'},
                    {'label': 'female : 75+ years', 'value': 'female : 75+ years'},
                    {'label': 'male : 05-14 years', 'value': 'male : 05-14 years'},
                    {'label': 'male : 15-24 years', 'value': 'male : 15-24 years'},
                    {'label': 'male : 25-34 years', 'value': 'male : 25-34 years'},
                    {'label': 'male : 35-54 years', 'value': 'male : 35-54 years'},
                    {'label': 'male : 55-74 years', 'value': 'male : 55-74 years'},
                    {'label': 'male : 75+ years', 'value': 'male : 75+ years'},
                ],
                value = ['female : 25-34 years'],

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