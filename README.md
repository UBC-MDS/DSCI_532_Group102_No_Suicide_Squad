# DSCI_532_Group102_No_Suicide_Squad
DSCI 532 Lab 1 Group 102: Anny Chih, Suvarna Moharir, &amp; Manuel Maldonado Aguilar

[Understanding Suicide Rates App Link](https://dsci-532-group102-milestone2.herokuapp.com/)

**Note: The original proposed app sketches are still available at the bottom of this README file** 

### DESCRIPTION OF THE APP
The purpose of this app is to help you visualize suicide rates in different locations over time, and see how a variety of different factors (i.e. age, gender, and year) affect these rates. There are 2 main research questions the app aims to answer using 2 tabs: 

**Tab 1:** How does the suicide rate change over time, and what effect does continent, region, country, age, and gender have on this?
**Tab 2:** How does the suicide rate of one country compare against the suicide rate of another country? 

#### Tab 1: Continent-Region-Country Analysis
### Suicide Rate by Continent ###
**Step 1:** This graph shows the average suicide rate over time, by continent.
The dashed line shows the worldwide average for each year.
You can hover over each line to see the exact suicide rate for that continent and year.

[plot_1a](https://github.com/UBC-MDS/DSCI_532_Group102_No_Suicide_Squad/blob/master/img/plot_1a.png)

### Suicide Rate by Region ###
**Step 2:** Are there any sub-regions you are specifically interested in looking at?
You can use this drop-down to select one or more sub-regions (arranged by continent) to view the average suicide rate by year.
You can hover over each line to see the exact suicide rate for that sub-region and year. The dashed line shows the worldwide average for each year.
[plot_1b](https://github.com/UBC-MDS/DSCI_532_Group102_No_Suicide_Squad/blob/master/img/plot_1b.png)

### Suicide Rate by Country ###
**Step 3:** Now that you’ve had a chance to explore the suicide rate by continent and subregion, are there any countries you’d like to look into more?
Use the drop-down to select one or more countries (arranged by continent) to view the average suicide rate by year.
You can hover over each line to see the exact suicide rate for that country and year. The dashed line shows the worldwide average for each year.

[plot_1c](https://github.com/UBC-MDS/DSCI_532_Group102_No_Suicide_Squad/blob/master/img/plot_1c.png)

### Suicide Rate by Demographic Groups ###
**Step 4:** You may be wondering what factors other than location affect the suicide rate.
Make sure you have at least one country selected above, and then this graph will automatically show the average suicide rates for 12 demographic groups (based on age and gender) over time.
If you have chosen multiple countries, it will display the average suicide rate for each of the 12 demographic groups of all selected countries.
You can hover over each line to see the exact suicide rate for that country/countries and demographic group. The dashed line shows the worldwide average for each year.

[plot_1d](https://github.com/UBC-MDS/DSCI_532_Group102_No_Suicide_Squad/blob/master/img/plot_1d.png)

#### Tab 2: Two Country Comparison
**Step 1:** Select 2 countries that you would like to compare. Select them in each dropdown (1 country per dropdown).
[plot_1a_dropdown](https://github.com/UBC-MDS/DSCI_532_Group102_No_Suicide_Squad/blob/master/img/plot_1a.png)

**Step 2:** Pick a range of years that you are interested in looking into. Use the slider to select this range.
The graph below will show the average suicide rate for the year range selected for each of the 2 countries.
[plot_2a](https://github.com/UBC-MDS/DSCI_532_Group102_No_Suicide_Squad/blob/master/img/plot_2a.png)

**Step 3:** You might be wondering about how the suicide rate for the 2 countries changes by demographic group.
You can select one or more demographic groups (gender and age) to see the different suicide rates by demographic group for your 2 chosen countries.

[plot_2b_dropdown](https://github.com/UBC-MDS/DSCI_532_Group102_No_Suicide_Squad/blob/master/img/plot_2b_dropdown.png)

[plot_2b](https://github.com/UBC-MDS/DSCI_532_Group102_No_Suicide_Squad/blob/master/img/plot_2b.png)

#### ORIGINAL PROPOSED APP SKETCHES
### Tab 1: Suicide Rates Over Time by Location
![Sketch of Tab 1](https://github.com/UBC-MDS/DSCI_532_Group102_No_Suicide_Squad/blob/master/img/Dashboard_Tab1_Sketch.png)

This tab shows 4 line graphs* representing suicide rates (y-axis) over time (x-axis):
1. 	Suicide Rates by Continent: Populated by default to show suicide rates of the 5 continents from which data is available.
2. 	Suicide Rates by Region (Blank by default): Using a checklist of regions, the graph is populated with suicide rates of selected regions over time.
3. 	Suicide Rates by Country (Blank by default): Using a checklist of countries, the graph is populated with suicide rates of selected countries over time.
4. 	Average Suicide Rates by Demographic Group in Selected Countries (Blank by default): Populated with the average suicide rates of the 12 demographic groups (listed below) for the countries previously selected. 
 
*A line representing the average suicide rate across all countries is shown in the first 3 graphs for reference. A vertical line is also present in all line graphs which users can move across time to show a tooltip with the changing values of the continent/region/country/demographic group represented in the graph.
 
### Tab 2: Two-Country Comparison of Suicide Rates by Demographic Group
![Sketch of Tab 2](https://github.com/UBC-MDS/DSCI_532_Group102_No_Suicide_Squad/blob/master/img/Dashboard_Tab2_Sketch.png)

This tab shows 2 identical drop-down menus where users can select 2 countries, and a RangeSlider where users can examine a specific time period. This tab also shows 2 bar graphs:
1. 	Average Total Suicide Rate by Country (Blank by default): After 2 countries are selected, the graph displays average suicide rates for all people in each country.
2. 	Suicide Rate by Demographic Group (Blank by default): After demographic groups are selected, the graph is populated with a pair of bars for each group. Each pair represents the suicide rates for the 2 previously selected countries.
 
### Demographic Groups:
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
