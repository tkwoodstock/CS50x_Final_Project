import os
import requests

#raw countries file: https://github.com/google/dspl/blob/master/samples/google/canonical/countries.csv

def main():
    write_countries()


#creates a file of sorted countries
def write_countries():

    #if there isn't a file of sorted countries, open the csv of countries, read into memory and write a sorted list
    if not os.path.isfile("sorted_countries.txt"):

        #get a file that contains 246 countries from github repository:
        response = requests.get("https://github.com/google/dspl/blob/master/samples/google/canonical/countries.csv")
        object = response.json()

        #print(json.dumps(object['payload']['blob']['csv'] , indent=1)) # print this to see json info from link
        #read from json object ['csv'], countries found in column 4 (see: item[3])
        country_info = object['payload']['blob']['csv']
        countries = []
        for item in country_info[1:]:
            #new (delete comment)---
            string = ""
            for c in item[3]:
                #dont add words with additional info e.g., Falkland Islands [Islas Malvinas] becomes: Falkland Islands
                if c == "[":
                    break
                else:
                    string += c

            #new (delete comment) ---
            countries.append(string.strip())

        #create the missing file of countries sorted in alphabetical order and return True (action completed)
        with open("sorted_countries.txt" , "w") as file:
            for c in sorted(countries):
                file.write(f"{c}\n")
            return True
    else:
        #return False if the sorted countries file already exists
        #print("'countries_sorted' file already exists") # optionally print the file already exists
        return False


if __name__=="__main__":
    main()
