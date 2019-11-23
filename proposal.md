# No-Suicide Squad: Python App Proposal (Milestone 1)

## Section 1: Motivation and Purpose

Suicide leads to multiple deaths every year. If we had a better idea of what factors (e.g. location/age/gender) might result in higher suicide rates, this could help with awareness and prevention efforts. 

Our proposed app can be used for informed decision making, as outlined in our research questions and example scenarios in Section 3. More specifically, our app would:
- Provide a thorough outline of how suicide rates have changed over time in terms of multiple factors such as location, age, and gender,
- Allow for the identification of high-risk-for-suicide groups (based on demographics) within a country, and
- Allow for the comparison of suicide rates between countries for these groups. 

## Section 2: Description of the Data

Each observation represents a country’s annual suicide count from 1985 to 2016. The observations are associated with different subsegments of each country’s population. The subsegments include: 
- Gender (Male / Female), and
- Age Group (5-14, 15-24, 25-34, 35-54, 55-74 and 75+)
In addition to the suicide count for each subsegment, we also have the country’s population for that subsegment, a suicide rate per 100k inhabitants, as well as additional information about that country.
In order to calculate summarized indicators at the continent and region level, we have additionally joined this dataset with another dataset that associates each country to a continent and to a sub-region (e.g. North, Central, South America).
[Link to original (suicide) dataset](https://www.kaggle.com/russellyates88/suicide-rates-overview-1985-to-2016#master.csv) <br/>
[Link to continent and subregion dataset](https://www.kaggle.com/statchaitya/country-to-continent/download) <br/>

## Section 3: Research Questions We Are Exploring

**Research Question 1: How does the suicide rate change over time, and what effect does continent, region, country, age, and gender have on this?** <br/>

Usage Scenario (Philanthropist):  <br/>
Riley is a philanthropist looking to open a new suicide awareness centre. To investigate which locations, age groups, and/or genders the centre should focus on reaching, he can use our app to [explore] and [analyze] suicide rates over time by location and demographic group to help inform his decision.
<br/> <br/>

**Research Question 2: Which demographic group in a country’s population currently shows the highest suicide rate?**

Usage Scenario (Government Institution): Manuel is a government official whose job is to allocate federal funds with the goal of reducing the suicide rate in his country. He wants to understand the demographics of the population who have had an increase in suicide rates through time in order to develop special suicide prevention programs. Using our app, he can [visualize] the suicide rate of different demographic groups in his country over time. 
<br/> <br/>

**Research Question 3: How does the suicide rate in one country compare against the suicide rate of another, similar country?**

Usage Scenario (Individual): Alice is a civilian whose friend has been expressing thoughts about self harm and she wants to know whether suicide rates for her friend’s age and gender are more/less common in another country that she thinks is similar to her own. Using our app, she can [compare] the suicide rate of her country against that of another country so she can [identify] which country has the lower suicide rate for her friend’s age and gender.
<br/> <br/>

When using our app, Riley, Manuel, and Alice can [explore] suicide rates over time for [selected] regions and countries *(Research Question 1)*, and [compare] the average suicide rates for different demographic groups in these locations *(Research Question 2)* on the same tab. On a second tab, they can further [compare] the suicide rates for two [specified] countries by a [selected] demographic groups and a [chosen] time period *(Research Question 3)*.
<br/>
In exploring the suicide rates by continent, region, country, age, and gender using our app, we hope that Riley, Manuel, Alice, and all other app users would be better able to answer their own research questions about suicide.
