# Team Reflection - Understanding Suicide Rates App

Note: This reflection was originally submitted as part of Milestone 2, but has been updated to include peer and TA feedback received with Milestone 3. 

## What It Does Well 

- Our app answers our 2 major research questions in what we believe is an organized and easy-to-follow fashion. It also allows for interactivity, and the tooltips display individual numerical values.

- The visualizations are separated into 2 tabs by research question, which reduces cluttering and allows for better organization.

- There is a clear overall purpose and general instructions for the app listed at the top. There are also step-by-step instructions for each plot which guides the user through a narrative.

- The ‘worldwide average’ dashed line in tab 1 allows the user to visually compare how their selected region/country/demographic group to the rest of the world. 

## Addressing Peer Feedback

#### Summary of Feedback Received
- It was recommended that we remove the regions without data in the ‘regions’ plot in tab 1, as, when users chose these regions, the graphs would not update. 

- Most of our peers also suggested reducing the amount of text in the app because it was overwhelming and often left unread. 

- The demographics plot in tab 1 seemed to cause some confusion. It was suggested that we should make clear that it is automatically updated based off the ‘country’ plot (plot 1c). It was also suggested that we de-clutter this plot by only plotting the average suicide rates for males and females rather than separating it by sex and age. 

- There were also a variety of aesthetics-related suggestions. Namely: (i) decreasing the opacity of our line graphs so it is easier to see the tool-tip numbers, (ii) moving the plots to the center of the app, (iii) making Tab 1 a ‘default’ tab, and (iv) changing the default colour scheme to avoid issues like yellow lines on white plots.

#### Reflection on Feedback Received
- Generally, it was easy for our peers to use our app. They seemed to understand the purpose of the app and how to navigate it.

- All 3 of our peer feedback groups had users mention that our instructions were too long and that the demographics chart on Tab 1 was overwhelming. It was also interesting that all 3 of our groups did understand the general purpose and features of the app. 

- From the feedback we received, we decided to modify the items that we could change with the time constraints we were working with. We decided to focus on the main usability features/bugs in our code and app (docstrings, missing data, the rangeslider not working for 2 years, length of instructions). 

- For the more aesthetic-related issues (the demographics plot being cluttered, increasing opacities, making Tab1 a default tab, changing colour schemes and plot widths), we decided to forgo these changes in our Python app, but will look into incorporating these in our R app next week. This decision was made mainly due to time constraints.

- Overall, the “fly-on-the-wall” experience was very valuable, and was perhaps the most valuable part of the peer feedback process. At times, it was frustrating when our peers had a question about the app but we could not answer it until the ‘teaching’ period, but it helped us understand the gaps and limitations of our app. For example, none of our peers read the instructions before each graph (they all later mentioned that it was too long), so we cut down the instructions to shorter/more basic sentences in an attempt to avoid overwhelming the users of our app. 

- Lastly, it was suggested that we could filter the ‘countries’ drop-down in Tab 1 based off the ‘regions’ that were selected in the previous graph. This suggestion has not been implemented due to time constraints.


## Addressing TA Feedback

#### Milestone 2 Feedback 

**TA Feedback**: *It’s great that you included a narrative for the app, but the information for each graph is at times a bit much, and could probably be reduced to one sentence per graph. Users can explore the app themselves to discover the various interactive features.*
- **Response**: We reduced the instructions for each graph to just the minimum amount of information required. 
<br/>
**TA Feedback**: *It would be good to have a default already selected for the graphs on the first tab.*
- **Response**: We considered adding default selections for the Region and Country, but are still undecided about whether to do this because we’d like users to play around themselves without being influenced by our default selections. The reason why we included defaults for Tab 2 is so the charts wouldn’t appear blank when the tab is opened. In Tab 1, the charts don’t appear blank by default because the worldwide average appears by default.
<br/>
**TA Feedback**: *Some of the options don't seem to work on the first tab graphs, such as "Western Africa".*
- **Response**: We removed the options for the graphs on first tab that did not have data (e.g. Western Africa). 
<br/>
**TA Feedback**: *The slider in Tab 2 doesn’t seem to work when there is only a range of 2 years selected.*
- **Response**: We fixed the error in our code that resulted in this issue.
<br/>
**TA Feedback**: *Another idea would be the option to group the demographic groups more broadly, such as females vs. males for a selected country. (Lower priority)*
- **Response**: We chose not to group the demographic groups into more broad categories due to time limitations, but we plan to incorporate this for our R app. 

## Summary of Changes Made

#### Overall
- We added docstrings in PEP8 style to all our functions to help those who may be unfamiliar with our data better understand our code.

- We shortened the instructions before each graph so users don’t feel overwhelmed with the amount of information presented.

- We improved code readability by refactoring our code so that ‘Country’ and ‘Region’ dropdowns refer to lists of countries and regions rather than having them listed within the `dcc.Dropdown` sections.

#### Tab 1
- We removed regions that did not have data so that they cannot be selected using the dropdown.

- We clarified the text to make it clear that both charts 1c and 1d are updated using the ‘Country’ dropdown.


### Tab 2
- We fixed the error in our code that prevented users from selecting a range of only 2 years.  

- We added more space between the year slider and plot 2a to prevent the ‘Year’ slider from appearing over the plot on certain screens.


## Limitations That Remain / Possible Future Fixes

#### Tab 1
- Plots 1a-d: The ‘hover’ feature has not been enabled on the ‘worldwide average’ line.

- Plots 1b-d: There are missing data for specific demographics and years for some countries, so if a user selects these location/demographic/time combinations, the charts may look as though only parts of the plots have been updated, which can cause confusion.


#### Tab 2
- Year Slider: If the user does not open the graph in a full-screen window, the year range slider does not change in size, and as a result, appears squished.

- Plot 2b: There is no option to “select all” demographic groups with one click; if the user wants to see all groups, they need to manually check each box.


