# Harvard CS50x final project: COUNTRIES (Web Version)

#### Video Demo:  <https://www.youtube.com/watch?v=8Qm-kIGWG2c>
#### Website link: <https://tkwoodstock.pythonanywhere.com/>

### Description:

#### See 'project' folder for Flask application scripts 
#### See 'resources' folder for data scraping scripts and the resulting csv database (which is used by the web app)

This is a web based adaption of my CS50 python final project:
- CS50p project Github Repo: https://github.com/tkwoodstock/cs50p_final_project/tree/main
- CS50p project Video: https://youtu.be/Dni5MiR7Or0

The web version (this project) uses Flask (in Python) to host a site consisting of HTML skeleton, CSS styling, and javascript functionality.

#### DATA USED IN THE APPLICATION IS NOT ACCURATE FOR YEAR OF PUBLISH (2023). THIS PROJECT IS DEMONSTRATIVE AND USES A DATASET OF COUNTRY METRICS FROM 2018. DATA MAY BE UPDATED TO 2023 IN FUTURE IF A SUITABLE DATA SOURCE (MUST BE ACCESSIBLE VIA HTTP REQUESTS AND PRESENTED IN JSON FOMRAT) IS FOUND FOR POPULATION, GDP, LIFE EXPECTANCY AND CO2 EMISSIONS.


### Contents of Project Folder:

#### 1. app.py (Python)
#### 2. templates (HTML, Javascript)
    2.1. index.html
    2.2. table.html
    2.3. visual.html
    2.4. receiver.html
#### 3. static (Python, CSS)
    3.1. python/functions
    3.2. style/styles.css


### 1. app.py (Python)

This python file contains the flask functionality, and renders the four html pages (see 2.1 - 2.4).

#### Data Source
Using the python requests library, a list of dictionaries containing country names and corresponding data metrics is obtained from within the project github repo (https://github.com/tkwoodstock/CS50x_Final_Project/tree/main/resources). This resources folder contains a file called 'data4app.csv', containing the names of 245 countries alongside their population, GDP, life expectancy, and annual CO2 emissions. The file is created and uploaded directly to Github by running adaptation of my CS50P python final project 'countries.py' file called 'adapted.py' (countries.py: https://github.com/tkwoodstock/cs50p_final_project/tree/main, adaptation: https://github.com/tkwoodstock/CS50x_Final_Project/tree/main/resources/data_writer). The request is sent to: https://api-ninjas.com/api/country. This address provides data metrics for each country in JSON format which are parsed by the python script.

The results are stored in the COUNTRIES_DATA list variable, the data source for the web app. When a user selects a list of countries in "index.html", their data is retreived directly from this python rendered list of 245 dictionaries.

This web application is for demonstrative purposes as a project submission for Harvard CS50x. The data taken from the api is from 2018, if the owner of API Ninjas updates their api data, this project website data can then also be updated. In future the data source may be changed to get more recent metrics (i.e., 2021+) however, at this time API Ninjas provided the most comprehensive data across all countries that was available in JSON compared to other considered sources. If the reader is aware of an online database of country data with more recent metrics (2021+) that is available and accessible via http requests, please contact me at tyler.k.woodstock@gmail.com and I will try update the website to present more recent data.

#### App Routes
The four routes in app.py correspond to the four html pages (see section 2).
1. The index route ("/"), calls the function index(), which renders the the home page ("index.html"), displayed when the page is first visited.
2. The table route ("/table") calls the function table(), which renders a page of all tabulated data ("table.html"), which can be visited from the home page.
3. The visual route ("/visual") calls the function visual(), renders the page of graphical data visualisation for the users selected countries; the country selection is updated in python after being received by the /receiver route.
4. The receiver route ("/receiver") calls the visual function which renders the graphical visualisation. This route, via ajax, receives from javascript in "index.html", a json formatted list of the users country selection which is then updated in python, and subsequently passed to "visual.html" via the /visual route.

### 2. Templates (HTML, Javascript)
The body of all pages contain design elements (e.g., background colour) from css styling in static/styles.css (see 3.2).

#### 2.1. index.html
The home page contains a form and a dropdown list. The list of countries in the dropdown is passed via flask from app.py, thus the list directly mirrors the countries column of the csv data file in the resources folder in the project github repository (https://github.com/tkwoodstock/CS50x_Final_Project/blob/main/resources/data4app.csv). The user can select up to 10 countries, however this value may be changed by the developer by changing the value of variable 'max' at the top of the script in "index.html" (line 24). Each time the user adds a country to the 'user_selection' array via 'user_selection.push(country_name)', each country in the list is displayed on the screen. When 'user_selection.length' is equal to 10, the user cannot add anymore countries to the array. The user can then proceed to graphical visualistion by clicking the 'proceed with selection', which is coloured in green using css styling. Alternatively, at any point (given the user has selected at least one country), the user may clear their choices to restart the country selection process by clicking the 'clear selection'  button, coloured red using css styling. The 'clear selection' button works by setting the 'user_selection' variable length to 0 (i.e., 'user_selection.length = 0').

There is also a link in the footer of the home page which directs to "table.html", a table of all data (see 2.2) used in the application. Finally links to the developers professional sites (linkedin, github) are provided at the very bottom of the page.

#### 2.2. table.html
This page displays a direct mirror of all the data in the csv file in the resources folder in the project github repository (https://github.com/tkwoodstock/CS50x_Final_Project/blob/main/resources/data4app.csv). If data is changed in the github repository, it will be reflected here (and in fact throughout the entire web application). Sorting arrows have been added to the headers in the form of buttons, formatted as hexadecimal characters (0x2191 for up arrow and 0x2193 for down arrow). The sorting function is implemented in javascript, each button has an id corresponding to its field, upon being clicked the data structure (list of dictionaries) is sorted by the metric corresponding to the id of the button clicked. Button colour changes using css styling when clicked, to help the user navigate the page and recognise by which field the column is currently sorted by. Additionally, the sorting algorithm always places "N/A" values at the bottom, regardless of whether sorting in ascending or descending order. This sorting table was manually hardcoded in javascript however, in future it may be considered to use predesigned sorting tables from bootstrap to shorten design time.

#### 2.3. visual.html
When the user clicks proceed in "index.html" (see 2.1), their list of countries goes through the following process:
    1. Converted to json format
    2. Sent to "/receiver" route (see 1 and 2.4)
    3. Parsed and recorded in python
    4. Matched to data in the 'COUNTRIES_DATA' list (list of dictionaries) to filter selected data rows
    5. Matches are recorded in a new list called 'user_data'
    6. 'user_data' is sorted by population to create 'choices'
    6. 'choices' is sent via Flask functionality to "visual.html" as a list of dictionaries containing population, GDP, life expectancy, and CO2 emissions ONLY for the countries the user selected

All graphs in "visual.html" are produced using chart.js (https://www.chartjs.org/). Originally ".png" images were created using matplotlib (python library) and placed in the static folder however, it was decided that chart.js was a better design choice as graphs are more dynamic, interactive, and communicate in javascript (which is the language in which "visual.html" is scripted). Moving forward from this experience, chart.js is certainly recommended over matplotlib for data visualisation on webpages or when using javascript and Flask.

Upon being rendered, "visual.html" displays a graph for population, with data sorted in descending order, accompanied by a table (also sorted in the same fashion). A dropdown list is available for users to change the metric, which has been programmed in javascript. Upon changing, the selected value in the dropdown list informs the script to render - using chart.js - a graph for the corresponding metric, which is again resorted to display in descending order. GDP and CO2 trigger a second HTML canvas tag for a per capita visualisation, when any other metric is clicked this second canvas is removed and the associated graph destroyed. Graph 1 and canvas 1 are simply updated upon each dropdown selection change, while graph 2 is created and destroyed, to maintain the formatting of the page so the tabulated data is placed appropriately on the page. Tabulated data also changes upon each change in the dropdown menu, displaying the same sorted data as the graph bu in tabulated numerical format.

Finally, a download button is avaiable at the bottom of the page, which downloads (in sorted order) the data (csv format) for whichever metric is selected in the dropdown menu. Functionality for download was taken from a stack overflow public discussion (https://stackoverflow.com/questions/14964035/how-to-export-javascript-array-info-to-csv-on-client-side), this functionality was not part of the CS50x curriculum and therefore, I do not exactly understand how it functions however, it has been succesfully implemented in the project and users may download sorted data for their selection.

#### 2.4. recevier.html
Via ajax, the javacsript array in "index.html" is sent to the Flask route "/recevier" in app.py. Like download functionality (see 2.3), this was not on the CS50x curriculum, and the technique was learnt from a youtube tutorial on sending variables javascript-to-python (https://www.youtube.com/watch?v=Ax_xwLybUME&list=WL&index=2&t=654s&ab_channel=DataAnalyticsIreland). Once in python, the user_choices list is intially cleared (from any previous use) and then the javascript json object is parsed into a python list, which is then avaiable for use by the "/visual" route (see 2.3).


### 3. static (Python, CSS)

#### 3.1. python/functions
The "python" folder contains a file called "functions.py". This file contains python functions used by "app.py". The first is a self-made significant figures rounding function, as I could only find decimal place rounding functions for python. The second is the old visualisation technique which used matplotlib to render graphs for each data metric to be displayed in "visual.html". In the end "chart.js" was used for data visualisation (see 2.3 for justification) however, it was decided to leave the original python visualisation function muted for backup and future reference.

#### 3.2. style/styles.css
The style folder contains the "styles.css" file which contains css styling for all the pages in templates. E.g., text alignment, table formatting, background colours, buttons/dropdown formatting, containers etc.


