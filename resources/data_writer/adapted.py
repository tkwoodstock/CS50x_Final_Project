#file writes list of countries data to github repository
#data includes country name, population, GDP, life expectancy, CO2 emissions
#github repo is accessed by my cs50x final project website (programmed as a python flask application)

import os

from functions.project import get_data
from functions.project import read_countries
from functions.analysis import write_to_csv
from functions.analysis import format
from github import Github


def main():

    #create user data folder
    if not os.path.isdir("user_data"):
        os.system("mkdir user_data")

    #read list of countries into python variable
    countries = read_countries()

    #put sorted countries list into folder
    if not os.path.isdir("user_data/sorted_countries.txt"):
        os.system(f"mv sorted_countries.txt user_data")


    #unblock to print countries list:
    #for i in countries:
        #print(i)


    #get data from api ninjas website
    data_countries = []

    for country in countries:
        data_countries.append(get_data(country))

    #create list of dictionary of country data
    formatted_data = format(data_countries)


    #write dicitonary list to csv
    write_to_csv(formatted_data, "Country")


    #upload to github ---------------
    with open("tok/tok.txt") as file:
        token = file.read()

    g = Github(token)

    repo = g.get_repo('tkwoodstock/CS50x_Final_Project')
    f = repo.get_contents("resources/data4app.csv")

    with open("user_data/user_country_data.csv") as file:
        data = file.read()

    repo.update_file('resources/data4app.csv' , 'upload csv' , data , f.sha)
    #end of github upload ---------------------------

if __name__ == "__main__":
    main()
