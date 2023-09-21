# Harvard CS50x final project: COUNTRIES (Web Version)

#### Video Demo:  <InsertURL>

#### Description:

This is a web based adaption of my CS50 python final project:
- CS50p project Github Repo: https://github.com/tkwoodstock/cs50p_final_project/tree/main
- CS50p project Video: https://youtu.be/Dni5MiR7Or0

The web version (this project) uses the Flask (in Python) to host a site consisting of HTML skeleton, CSS styling, and javascript functionality.


### Contents:

#### 1. app.py
#### 2. templates
    2.1. index.html
    2.2. table.html
    2.3. visual.html
    2.4. receiver.html
#### 3. static
    3.1. python
    3.2. style


### 1. app.py

This python file contains the flask functionality, and renders the four html pages (see 2.1 - 2.4).

#### Data Source
Using the python requests library, a list of dictionaries containing country names and corresponding data metrics is obtained from within the project github repo (https://github.com/tkwoodstock/CS50x_Final_Project/tree/main/resources). This resources file contains a file called 'data4app.csv', containingthe names of 245 countries alongside their population, GDP, life expectancy, and annual CO2 emissions. The file is created and uploaded directly to Github using an adaptation of my CS50P python final project countries.py file (countries.py: https://github.com/tkwoodstock/cs50p_final_project/tree/main, adaptaion: ????). The request is sent to: https://api-ninjas.com/api/country. This address provides data metrics for each country in JSON format which are parsed by the python script.

The results are stored in the COUNTRIES_DATA list variable, the data source for the web app. When a user selects a list of countries in "index.html", their data is retreived directly from this python rendered list of 245 dictionaries.

This web application is for demonstrative purposes as a project submission for Harvard CS50x. The data taken from the api is from 2018, if the owner of API Ninjas updates their api data, this project website data can then also be updated. In future the data source may be changed to get more recent metrics (i.e., 2021+) however, at this time API Ninjas provided the most comprehensive data across all countries that was available in JSON compared to other considered sources. If the reader is aware of an online database of country data with more recent metrics (2021+) that is available and accessible via http requests, please contact me at tyler.k.woodstock@gmail.com and I will try update the website to present more recent data.

#### App Routes





