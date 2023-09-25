from flask import Flask, render_template, request, redirect, url_for, session
import requests
import json
from static.python.functions import round_sig_figs

app = Flask(__name__)


#store countries list -------------
#Create empty array
COUNTRIES = []

#store country data list -------------
#Create empty array
COUNTRIES_DATA = []


#send request to github for data list
url = "https://github.com/tkwoodstock/CS50x_Final_Project/blob/main/resources/data4app.csv"
response = requests.get(url)
object = response.json()
data = object['payload']['blob']['csv'] #filter for list of countries


#parse header row
headers = data[0]

#populate list of country names
for row in data[1:]:
    for i , heading in enumerate(headers):
        if heading == "Country":
            COUNTRIES.append(row[i])


#Get data for each country
#populate list with dictionary for each row, using data corresponding to each header
for row in data[1:]:
    dict = {}
    for i,heading in enumerate(headers):
        dict[heading] = row[i]
    COUNTRIES_DATA.append(dict)


#Format COUNTRIES_DATA ARRAY into strings and floats (json object has all string type values, must be converted)
for i , data in enumerate(COUNTRIES_DATA):
    dict = {}
    for j in headers:
        if j == "Country":
            pass
        elif type(data[j] == str) and data[j].strip() != "N/A":
            COUNTRIES_DATA[i][j] = float(data[j])
        else:
            COUNTRIES_DATA[i][j] = data[j].strip() # ensure N/A is formatted with no spaces either side
                                                   # (it is used in javascript conditions e.g., if x == "N/A" , white space must be removed for this to work)


#store user choices in this array (starts empty and is populated upon user clicking 'proceed in selection.html')
user_choices = []
#------------------------------


#Flask functions -----------------
@app.route("/")
def index():
    user_choices.clear()
    return render_template("index.html" , c=COUNTRIES , dat=COUNTRIES_DATA)


@app.route("/visual")
def visual():

    #Create array of data for user chosen countries
    user_data = []
    for i in COUNTRIES_DATA:
        if i["Country"] in user_choices:
            dict = {} #each loop create empty dict and populate with data for country in user country selection
            le_dict = {} # dictionary for life expectancy

            dict["Country"] = i["Country"]

            dict["GDP"] = i["GDP"]

            dict["Population"] = i["Population"]

            #Format male and female life expectancy into one dictionary for 'visualise' function
            le_dict["Male"] = i["Male_Life_Expectancy"]
            le_dict["Female"] = i["Female_Life_Expectancy"]
            dict["Life Expectancy"] = le_dict # add life expectancy sub dictionary into dictionary

            dict["CO2"] = i["CO2"]

            if i["GDP"] != "N/A":
                dict["GDP_percap"] = round_sig_figs(i["GDP"] / i["Population"] , 2)
            else:
                dict["GDP_percap"] = "N/A"

            if i["CO2"] != "N/A":
                dict["CO2_percap"] = round_sig_figs(i["CO2"] / i["Population"] , 2)
            else:
                dict["CO2_percap"] = "N/A"

            #append formatted dictionary to list of data for user selection
            user_data.append(dict)

    #sort user data by population in descending order, store in variable called choices, which is passed to "visual.html"
    choices = sorted(user_data, key= lambda x: (x["Population"] != "N/A", x["Population"]), reverse = True)

    return render_template("visual.html" , data = choices)


@app.route("/table")
def table():

    return render_template("table.html" , count=COUNTRIES_DATA)



@app.route("/receiver" , methods=["POST"])
def tester():

    #Receive array of users chosen countries

    #First clear old data
    user_choices.clear()

    #Receive array in json format
    output = request.get_json()
    result = json.loads(output)


    #Append received data to user_choices array
    object = result["user_selection"]
    for i in object:
        if i in COUNTRIES:
            user_choices.append(i)

    return render_template("receiver.html")



#-----------------------------

"""
def round_sig_figs(n , figs):
    #copy number
    copy = float(n)
    count = 0

    #find number of digits in number
    if copy > 1:
        while copy > 1:
            copy = copy/10
            count += 1

        #round copy now less than zero to specific sig figs
        rounded_as_decimal = round(copy , figs)
        #reinstate order of number (multiply by 10^(n_digits)) in two steps to avoid rounding errors
        to_int = int(rounded_as_decimal*10**figs)
        result = to_int/(10**(figs-count))
        return result

    elif copy < 0.1:
        while copy < 0.1:
            copy = copy*10
            count += 1

        #round copy now less than zero to specific sig figs
        rounded_as_decimal = round(copy , figs-1)
        #reinstate order of number (multiply by 10^(n_digits))
        str_num = str(rounded_as_decimal/(10**(count)))
        result = ""
        for i in range(figs+2):
            result += str_num[i]
        return float(result)

    else:
        return round(n , figs)

"""


if __name__=="__main__":
    app.run()

