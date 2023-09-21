import os
import re
import requests
import art
import sys
from countries_writer import write_countries
from analysis import analysis_countries

max = 10 # maximum number of countries for analysis, can be changed accordingly

def main():

    try: # allow user to exit program at any time using
        countries = read_countries()

        #print introductory message
        print(art.text2art("Welcome  to  COUNTRIES :" , font="small"))

        print(f"\nThis program allows users inspect and compare data from UP TO {max} countries")
        print("To exit the program at any time, press keys: 'ctrl' and 'c'\n")


        #create list of data on countries the user has selected
        countries_data = []

        brk = False #break from loop when brk is changed to True
        while brk == False: #infinite loop until user has selected all the countries they wish to get data for

            #first, get user to input a country they want information on
            country = check_countries(countries)

            #second, get data about the country
            country_data = get_data(country) # country data is a dict of info for each country

            #append the data of the selected country to the countries_data list
            if country_data in countries_data:
                pass
            else:
                countries_data.append(country_data)

            # once the list has data for the maximum allowed n.o countries, the list is full
            if len(countries_data) == max:
                break

            #tell user which countries are currently selected
            print(f"\nYou have currently selected {len(countries_data)}/{max} countries: " , end = "")
            for i in countries_data:
                print(f"[{i['Country']}] " , end = "")

            #ask user if they want to add another country to their list of selected countries
            #only accept 'y' or 'n', any other input will result in reprompt
            while True:
                choice = input("\n\nWould you like data for another country (y or n)? ")
                if choice.lower().strip() == "y" or choice.lower().strip() == "yes":
                    print()
                    break
                elif choice.lower().strip() == "n" or choice.lower().strip() == "no":
                    brk = True
                    break
                else:
                    pass

        #User has now selected their countries (from 1 country to maximum number specified above)

        #confirm countries data is correct, user can add or swap countries
        countries_data = confirm_selection(countries_data , countries)

        #all checks complete, print dictionaries of data
        print(f"\nYou have selected the following as your final list for analysis:")
        print("-------------------------------------------------------------------")
        for i, cont in enumerate(countries_data):
            #print(f"[{i['Country']}] " , end = "") #print this to just see country names
            print(cont)                         #print this to see dictionary for each country
            if i < len(countries_data) - 1:
                print()

        #data analysis (create separate python file)
        print("-------------------------------------------------------------------")
        trash = input("\nYou may now sort selected countries by the data above. Press enter to continue.")
        analysis_countries(countries_data)


    except KeyboardInterrupt:
        os.system('clear')
        print("Program closed by user\n")
        sys.exit("Thank you for using my CS50p final project: 'Countries',\nby Tyler Woodstock\n")


# END OF MAIN()

#------------- functions -------------------

#exact or near matches
def near_match(input, list):

    for value in list:
        #see if user input contains country
        matches1 = re.search(rf"({input})", value , re.IGNORECASE)
            #matches 1 checks if the input string can be found inside the value (e.g., country name)
        matches2 = re.search(rf"({value})([^a-zÀ-ÖØ-öø-ÿ]|$)", input , re.IGNORECASE)
            #matches 2 checks if the value (e.g., country name) can be found inside the input string (e.g., my country is egypt)
            #matches 2 must have a space after the match, so that the value is not simply be inside a longer input word
                #e.g., so that nigeria doesn't match with niger
        if matches1:
            match = matches1.group(1)
        if matches2:
            match = matches2.group(1)

        #if the input can be found inside value and it is missing 1 letter:
        if matches1 and len(value) - 1 <= len(match):
            return value
        #if the value is inside the input string
        elif matches2 and len(match) == len(value):
            return value
    #return empty string if no match found
    return ""



#MISSPELL MATCH FUNCTION:
def misspell_match(input , list):
    #error represents both:
        #permitted percentage of letters in word that can be mispelled
        #permitted percentage error in length of word
    error = 0.2

    #iterate over each item in the list and check if every in the input can be found in the item
    for item in list:
        #store found letters in array
        found = []
        copy = item
        misspellings = 0
        #compare letters (converted to lower case) to see if they are in both input and list item
        for c in input:
            if c.lower() not in copy.lower():
                misspellings += 1
                if misspellings > error*len(item): # only allow error% (currently 20%) of letters to be misspelled
                    break
                pass
            else:
                #if letter is found, remove that letter from comparison string (so user cannot input 'snnnn' for spain)
                copy = copy.replace(c , "" , 1)
                found.append(c)

        #if every letter typed is found in the word, (they are within 20% similarity in length),
        # and start with the same letter
        if (1 - error <= len(found)/len(item) <= 1 + error) and (found[0].lower() == item[0].lower()): # and found[len(found)-1].lower() == item[len(item)-1].lower()):
            return item

    #return empty string if no match
    return ""





#returns a match if input is an abbreviation of an item in the list
#e.g., US will match united states, uae will match united arab emirates
#the word and is excluded from the abbreviation:
#e.g., HIMI matches: Heard Island and McDonald Islands (HIAMI will not match)
def abbreviate_match(input , list):
    for value in list:
        #cannot find abbreviates in a single word values (e.g., colombia cannot be c)
        #there must be a space in the value (e.g., united states)
        if " " not in value:
            pass
        else:
            #split country in list into abbreviation (e.g., united states -> us)
            items = [*value.split()]
            abbreviation = ""
            for i in items:
                if i.lower() != "and":
                    abbreviation += i[0]
            #return true if user has input an abbreviation of the value
            if abbreviation.lower() == input.lower():
                #print("abbreviation match")
                return value

    #return empty string if no match is found
    return ""



#read from sorted countries file (add population and other info into this file and turn into csv)
def read_countries():
    #if there isn't a sorted counrties file then use function to write the file
    if not os.path.isfile("sorted_countries.txt"):
        write_countries()

    with open("sorted_countries.txt") as file:
        reader = file.read()
        countries = []
        country = ""
        for i in reader:
            if i == "\n":
                countries.append(country)
                country = ""
            else:
                country += i

        return countries



#prompt for input until user enters something in the provided list
def check_countries(countries):
    while True:
        user_country = input("Enter country of interest: ").strip()
        country = ""

        #assume input is string, if it fails the checks below, this value becomes false
        is_string = True

        #Format check 1
        #Do not accept if user presses space bar without entering text
        if not user_country:
            is_string = False

        #Format Check 2
        #search for grammar in input (only letters/foreign letters, spaces and appostraphes are allowed)
        matches = re.findall("([^a-zÀ-ÖØ-öø-ÿ])" , user_country , re.IGNORECASE)
        for match in matches:
            #only allow spaces and apostraphes for non-alphabetical characters
            if match != " " and match != "'":
                is_string = False
                print("Only enter alphabetical characters, do not enter punctuation or numbers\n")

        #only compare the input against countries if it has passed the format checks above (see format checks 1 and 2)
        if is_string:
            #hard coding uk countries as they are not in international country json object:
            if user_country.lower() == "england" or user_country.lower() == "scotland" or user_country.lower() == "wales" or user_country.lower == "northern ireland":
                user_country = "United Kingdom"

            #Run spelling check functions

            #Spelling Check 1:
            country = near_match(user_country , countries)
            #Spelling Check 2:
            if not country:
                country = misspell_match(user_country , countries)
            #Spelling Check 3:
            if not country:
                country = abbreviate_match(user_country , countries)
            #end of checks

            #if not found in any checks: post all countries in list starting with first letter they entered
            if not country:
                print("\ncountry NOT found\n")
                #call function to provide recommendations based on the first letter of their input
                recommend_options(user_country , countries)
                print() # formatting for readability

            #if country exists and has been found, double check user wants this value and return the value
            else:
                #Get user to confirm their country, only accept 'y' or 'n', any other value will reprompt
                brk = False
                while brk == False:
                    choice = input(f"\nConfirm: {country} (y or n): ")
                    if choice.lower().strip() == "y" or choice.lower().strip() == "yes":
                        return country
                    elif choice.lower().strip() == "n" or choice.lower().strip() == "no":
                        break
                    else:
                        pass




def recommend_options(user_input , list):
    #find first letter of user input
    for char in user_input.lower():
        if 96 < ord(char) < 123:
            first_letter = char.upper()
            break

    recommendations = []
    for item in list:
        if item[0] == first_letter:
            recommendations.append(item)

    print("-------------")
    for item in recommendations:
        print(f"{item}")
    print("-------------")

    print(f"\nInput value not recognised, you entered: '{user_input}'\nDid you mean one of the options above? (you may copy and paste)")

    return


def get_data(country):

    #data from: https://api-ninjas.com/api/country

    api_url = f'https://api.api-ninjas.com/v1/country?name={country}'
    response = requests.get(api_url, headers={'X-Api-Key': '434QJ8M+Oj4BY/VWSYo6Hg==O8cWcvVMXb5GZqFE'})
    object = response.json()

    print(f"\nSome information (from 2018) about selected country, {country.upper()}:\n-------------------------------------")

    try:
        GDP = round_sig_figs(object[0]['gdp'] , 3) / 1000
        print(f"-GDP: ${GDP:.1f} billion")
    except (KeyError, IndexError, TypeError):
        print("-Total GDP data not available")
        GDP = "N/A"


    #convert population to 3 significant figures (API returns population divided by 1000, so must be undone)
    try:
        population = round_sig_figs(object[0]['population'] , 3) / 1000
        print(f"-Approximate population: {population:,.2f} million")
    except (KeyError, IndexError, TypeError):
        print("-Total population data not available")
        population = "N/A"

    try:
        life_expectancy = {"Male": object[0]['life_expectancy_male'], "Female": object[0]['life_expectancy_female']}
        print("-Life expectancy:")

        print(f"    Male: {life_expectancy['Male']} years")
        print(f"    Female: {life_expectancy['Female']} years")
    except (KeyError, IndexError, TypeError):
        print("-Life expectancy data not available")
        life_expectancy = {"Male": "N/A", "Female": "N/A"}

    #MAYBE GET CO2 EMISSIONS FROM ANOTHER SOURCE
    try:
        CO2 = round(object[0]['co2_emissions'] , 3)
        print(f"-CO2 emissions: {CO2:,.0f} million tonnes")
    except (KeyError, IndexError, TypeError):
        print("-CO2 emission data not available")
        CO2 = "N/A"

    print("-------------------------------------")

    return {"Country": country, "GDP": GDP, "Population": population, "Life Expectancy": life_expectancy, "CO2": CO2}


#round a number (n) to a chosen number of significant figures (figs)
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
        result = to_int*10**(count-figs)
        return result

    elif copy < 1:
        while copy < 1:
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

def confirm_selection(countries_data , countries):
    global max
    brk = False
    while brk == False:

        #print current selection
        print(f"\n\nYou have selected the following for analysis:")
        for i in countries_data:
            print(f"[{i['Country']}] " , end = "")

        #ask if user wants to change their selection
        choice = input("\nProceed with the above selection? (y or n): ").strip()
        if choice.lower() == "y" or choice.lower() == "yes":
            break
        elif choice.lower() == "n" or choice.lower() == "no":
            while True:
                print()
                for i in range(max):
                    if i+1 <= len(countries_data):
                        print(f"{i+1}: {countries_data[i]['Country']}")
                    else:
                        print(f"{i+1}: -")
                subchoice = input("Which country would you like to change? Enter number: ")
                if not subchoice.isdigit():
                    print("\nERROR: Enter number")
                    pass
                elif int(subchoice) > max or int(subchoice) <= 0:
                    print("\nERROR: Enter number within range")
                else:
                    for i in range(max):
                        if int(subchoice) == (i+1):
                            replace = i
                    break
            print(f"CHANGING COUNTRY: {replace+1}\n")
            new_country = check_countries(countries)
            new_country_data = get_data(new_country)
            if new_country_data not in countries_data:
                if replace + 1 <= len(countries_data):
                    countries_data[replace] = new_country_data
                elif replace + 1 > len(countries_data):
                    countries_data.append(new_country_data)
            else:
                pass

        else:
            #if user does not enter y or no, repromt
            pass

    return countries_data


# ----------------- end of functions ----------------------


if __name__=="__main__":
    main()
