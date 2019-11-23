# DSCI_532_Group102_No_Suicide_Squad
DSCI 532 Lab 1 Group 102: Anny Chih, Suvarna Moharir, &amp; Manuel Maldonado Aguilar

### DESCRIPTION OF THE APP
Our app contains 2 tabs which allow users to explore suicide rates by location (Tab 1), and to compare suicide rates in 2 countries by demographic group (Tab 2). All suicide rates are shown per 100,000 people.
 
#### Tab 1: Suicide Rates Over Time by Location
[Sketch of Tab 1](https://github.com/UBC-MDS/DSCI_532_Group102_No_Suicide_Squad/blob/master/img/Dashboard_Tab1_Sketch.png)
This tab shows 4 line graphs* representing suicide rates (y-axis) over time (x-axis):
1. 	Suicide Rates by Continent: Populated by default to show suicide rates of the 5 continents from which data is available.
2. 	Suicide Rates by Region (Blank by default): Using a checklist of regions, the graph is populated with suicide rates of selected regions over time.
3. 	Suicide Rates by Country (Blank by default): Using a checklist of countries, the graph is populated with suicide rates of selected countries over time.
4. 	Average Suicide Rates by Demographic Group in Selected Countries (Blank by default): Populated with the average suicide rates of the 12 demographic groups (listed below) for the countries previously selected. 
 
*A line representing the average suicide rate across all countries is shown in the first 3 graphs for reference. A vertical line is also present in all line graphs which users can move across time to show a tooltip with the changing values of the continent/region/country/demographic group represented in the graph.
 
#### Tab 2: Two-Country Comparison of Suicide Rates by Demographic Group
[Sketch of Tab 2](https://github.com/UBC-MDS/DSCI_532_Group102_No_Suicide_Squad/blob/master/img/Dashboard_Tab2_Sketch.png)
This tab shows 2 identical drop-down menus where users can select 2 countries, and a RangeSlider where users can examine a specific time period. This tab also shows 2 bar graphs:
1. 	Average Total Suicide Rate by Country (Blank by default): After 2 countries are selected, the graph displays average suicide rates for all people in each country.
2. 	Suicide Rate by Demographic Group (Blank by default): After demographic groups are selected, the graph is populated with a pair of bars for each group. Each pair represents the suicide rates for the 2 previously selected countries.
 
#### Demographic Groups:
1. 	Females 5-14 years
2. 	Females 15-24 years
3. 	Females 25-34 years
4. 	Females 35-54 years
5. 	Females 55-74 years
6. 	Females 75+ years
7. 	Males 5-14 years
8. 	Males 15-24 years
9. 	Males 25-34 years
10.  Males 35-54 years
11.  Males 55-74 years
12.  Males 75+ years
