#this file takes the data from the selected countries in countries.py and applies analysis/visualisation techniques
import csv
import os
import sys
import matplotlib.pyplot as plt

def main():
    #test data below:
    my_dict = [
            {'Country': 'Tonga', 'GDP': 0.504, 'Population': 0.106, 'Life Expectancy': {'Male': 68.8, 'Female': 72.7}, 'CO2': 'N/A'},
            {'Country': 'Iceland', 'GDP': 25.9, 'Population': 0.341, 'Life Expectancy': {'Male': 81.2, 'Female': 84.3}, 'CO2': 2.2},
            {'Country': 'Heard Island and McDonald Islands', 'GDP': 'N/A', 'Population': 'N/A', 'Life Expectancy': {'Male': 'N/A', 'Female': 'N/A'}, 'CO2': 'N/A'},
            {'Country': 'Peru', 'GDP': 222.0, 'Population': 33.0, 'Life Expectancy': {'Male': 73.7, 'Female': 79.2}, 'CO2': 49.7},
            {'Country': 'Nigeria', 'GDP': 422.0, 'Population': 206.0, 'Life Expectancy': {'Male': 53.3, 'Female': 55.1}, 'CO2': 86.0},
            {'Country': 'Morocco', 'GDP': 118.0, 'Population': 36.9, 'Life Expectancy': {'Male': 75.1, 'Female': 77.5}, 'CO2': 58.1},
            {'Country': 'Italy', 'GDP': 2080.0, 'Population': 60.5, 'Life Expectancy': {'Male': 81.0, 'Female': 85.4}, 'CO2': 321.5},
            {'Country': 'Cyprus', 'GDP': 25.0, 'Population': 1.21, 'Life Expectancy': {'Male': 78.6, 'Female': 82.8}, 'CO2': 6.4},
            {'Country': 'Uzbekistan', 'GDP': 50.5, 'Population': 33.5, 'Life Expectancy': {'Male': 69.4, 'Female': 73.6}, 'CO2': 81.2},
            {'Country': 'Vietnam', 'GDP': 245.0, 'Population': 97.3, 'Life Expectancy': {'Male': 71.2, 'Female': 79.4}, 'CO2': 191.2},
            ]

    analysis_countries(my_dict)



#countries.py directly calls from here:
def analysis_countries(data: list):
    if not os.path.isdir("user_data"):
        os.system("mkdir user_data")

    try:
        #Get user to choose which field they want to sort the data by
        #Given options 1 - n, where n is number of fields
        brk = False
        while brk == False:
            count = 0
            fields = []
            print()
            #print options with corresponding numbers 1 - n
            for i, field in enumerate(data[0]):
                fields.append(field)
                print(i+1 , field)
                count += 1

            #get user choice, only accept valid inputs
            choice = input("\nSort data by which metric? Enter number: ").strip()
            if not choice.isdigit():
                print("\nINPUT MUST BE A NUMBER\n")
                pass
            elif int(choice) <= 0 or int(choice) > count:
                print(f"\nNUMBER MUST BE WITHIN RANGE: (1 - {count})\n")
                pass
            else:
                choice = int(choice)
                print(f"\nSorted by {fields[choice-1]}:\n------------------------")

                #names of countries are sorted in alphabetical order, not reversed
                if fields[choice-1] == "Country":
                    new = sorted(data, key = lambda x:x[fields[choice-1]])
                    field = fields[choice-1]
                    for i in new:
                        print(i[fields[choice-1]])
                #sort by average life expectancy: (m+f)/2
                #sorted in reverse, from highest to lowest
                elif fields[choice-1] == "Life Expectancy":
                    #turn None values into 0 (cannot add none values, see lambda function below)
                    for i in data:
                        if i["Life Expectancy"]["Male"] == "N/A":
                            i["Life Expectancy"]["Male"] = 0
                        if i["Life Expectancy"]["Female"] == "N/A":
                            i["Life Expectancy"]["Female"] = 0

                    new = sorted(data, key = lambda x: (x[fields[choice-1]]["Male"] + x[fields[choice-1]]["Female"])/2, reverse = True)
                    field = fields[choice-1]
                    for i in new:
                        #restore None values in dictionary
                        if i["Life Expectancy"]["Male"] == 0:
                            i["Life Expectancy"]["Male"] = "N/A"
                        if i["Life Expectancy"]["Female"] == 0:
                            i["Life Expectancy"]["Female"] = "N/A"

                        #print result
                        print(f"{i['Country']}: {i['Life Expectancy']['Male']} years , {i['Life Expectancy']['Female']} years")
                    #as there are two values they have been averaged
                    print("(Sorted by male/female values averaged)\n")
                #print all other data fields in reverse sorted order (i.e., highest to lowest)
                else:
                    new = sorted(data, key = lambda x: (x[fields[choice-1]] != "N/A", x[fields[choice-1]]), reverse = True)
                    field = fields[choice-1]
                    for i in new:
                        if i[fields[choice-1]] == "N/A":
                            print(f"{i['Country']}: {i[fields[choice-1]]}")
                        else:
                            if field == "GDP":
                                print(f"{i['Country']}: ${i[fields[choice-1]]:.1f} billion")
                            elif field == "Population":
                                print(f"{i['Country']}: {i[fields[choice-1]]:.1f} million")
                            elif field == "CO2":
                                print(f"{i['Country']}: {i[fields[choice-1]]:.0f} million tonnes")


            #Ask if user wants to sort again
            #if yes, the function loops again, if no the function breaks and moves to the next step
            #if neither y or n, user is repromted
                print("--------------------")
                #brk and switch for breaking out of loops
                brk2 = False
                switch = 0
                while brk2 == False:
                    choice = input("\nRe-sort by different metric? Enter y or n: ").strip()
                    if choice.lower() == "y" or choice.lower() == "yes":
                        switch = 0
                        print()
                        break
                    elif switch == 1:
                        brk = True
                        brk2 = True
                        break
                    elif choice.lower() == "n" or choice.lower() == "no":
                        results = format(new)
                        while True:
                            subchoice = input("\nVisualise sorted data (y or n)? ").strip()
                            if subchoice.lower() == "y" or subchoice.lower() == "yes":
                                visualise(new, field)
                                switch = 1
                                break
                            elif subchoice.lower() == "n" or subchoice.lower() == "no":
                                brk = True
                                brk2 = True
                                break
                            else:
                                pass
                    else:
                        pass

        while True:
            choice = input("\nWrite data to csv file (y or n)? ").strip()
            if choice.lower() == "y" or choice.lower() == "yes":
                write_to_csv(results, field)
                break
            elif choice.lower() == "n" or choice.lower() == "no":
                break
            else:
                pass

        print("\nFIN\n")
        #return to user the sorted list?? write to csv? CSV can be used in excel?? user get can list of countries in order,
        #give option in main countries python file to sort by all countries rather than one by one
        #return to file

    except KeyboardInterrupt:
        os.system('clear')
        print("Program closed by user\n")
        sys.exit("Thank you for using my CS50p final project: 'Countries',\nby Tyler Woodstock\n")


def format(countries):
    temp = {}
    results = []
    for i in countries:
        temp = {
            "Country": i["Country"],
            "GDP": i["GDP"],
            "Population": i["Population"],
            "Male_Life_Expectancy": i["Life Expectancy"]["Male"],
            "Female_Life_Expectancy": i["Life Expectancy"]["Female"],
            "CO2": i["CO2"],
            }
        results.append(temp)

    return results


def visualise(countries: list, field):
    #no visualisation for alphabetical order metric
    if field == "Country":
        print("\n--Countries sorted by name have no graphic visualisation, please choose another metric--")
        return 0

    #create list of names for x axis
    names_list = []
    for i in countries:
        names_list.append(i["Country"])

    x_axis = []
    for item in names_list:
        name = ""
        if " " in item:
            temp = item.split()
            for word in temp:
                if word.lower() != "and":
                    name += word[0].upper()
        else:
            name = item
        x_axis.append(name)


    #for life expectancy
    if field == "Life Expectancy":
        m_life_exp = []
        f_life_exp = []
        for i in countries:
            if i[field]["Male"] == "N/A":
                m_life_exp.append(None)
            else:
                m_life_exp.append(i[field]["Male"])

            if i[field]["Female"] == "N/A":
                f_life_exp.append(None)
            else:
                f_life_exp.append(i[field]["Female"])

        plot_list = [m_life_exp , f_life_exp]

        #plot list is life expectancy in format: [male , female]

        plt.figure(figsize=(10,6))
        plt.scatter(x_axis , plot_list[0] , color = "blue")
        plt.scatter(x_axis , plot_list[1] , color = "magenta")
        plt.title("Life Expectancy by Country")
        plt.xlabel("Country")
        plt.ylabel("Years")
        plt.legend(["Male" , "Female"])
        plt.savefig(f"Life_Expectancy.png")
        os.system("code Life_Expectancy.png")
        pause = input("\nSee visual in file: 'Life_Expectancy.png'\nPress enter to continue.")
        os.system("mv Life_Expectancy.png user_data")
        return 0

    #for population
    if field == "Population":
        plot_list = []
        for i in countries:
            if i[field] == "N/A":
                #append a zero for plotting purposes
                plot_list.append(0)
            else:
                plot_list.append(i[field])

        plt.figure(figsize=(12,6))

        plt.bar(x_axis , plot_list)
        plt.xlabel("Country")

        plt.title("Population by Country")
        plt.ylabel("Million People")

        plt.savefig(f"{field}.png")
        os.system(f"code {field}.png")
        pause = input(f"\nSee visual in file: '{field}.png'\nPress enter to continue.")
        os.system(f"mv {field}.png user_data")
        return 0


    #for GDP and CO2
    else:
        plot_list = []
        subplot_list = []
        for i in countries:
            if i[field] == "N/A":
                #append a zero for plotting purposes
                plot_list.append(0)
                subplot_list.append(0)
            else:
                plot_list.append(i[field])
                if field == "GDP":
                    per_cap = i[field] / i["Population"]
                    subplot_list.append(per_cap)
                elif field == "CO2":
                    per_cap = i[field] / i["Population"]
                    subplot_list.append(per_cap)

        plt.figure()


        fig, axs = plt.subplots(2, figsize=(25,15))

        axs[0].bar(x_axis , plot_list)
        axs[1].bar(x_axis , subplot_list)
        axs[0].tick_params(labelsize = 18)
        axs[1].tick_params(labelsize = 18)

        #plt.xlabel("Country")


        if field == "GDP":
            axs[0].set_title("GDP by Country" , size = 28)
            axs[0].set_ylabel("Billion Dollars ($bn)" , size = 22)
            axs[1].set_title("GDP per Capita by Country" , size = 28)
            axs[1].set_ylabel("Thousand Dollars ($thousand)" , size = 22)
        elif field == "CO2":
            axs[0].set_title("CO2 Emissions by Country" , size = 28)
            axs[0].set_ylabel("Million Tonnes (Mt)" , size = 22)
            axs[1].set_title("CO2 Emissions per Capita by Country" , size = 28)
            axs[1].set_ylabel("Tonnes (t)" , size = 22)



        plt.savefig(f"{field}.png")
        os.system(f"code {field}.png")
        pause = input(f"\nSee visual in file: '{field}.png'\nPress enter to continue.")
        os.system(f"mv {field}.png user_data")
        return 0


def write_to_csv(countries, field):
    with open(f"user_country_data.csv" , "w") as file:
        ls = ["Country" , "GDP" , "Population" , "Male_Life_Expectancy" , "Female_Life_Expectancy" , "CO2"]
        writer = csv.DictWriter(file , fieldnames = ls)
        writer.writeheader()
        for i in countries:
            writer.writerow(i)

        """
        writer2 = csv.writer(file)
        file.write("\n")
        if field == "Life Expectancy":
            note = [f"#SORTED BY '{field}' (M-F average)"]
        else:
            note = [f"#SORTED BY '{field}'"]
        writer2.writerow(note)
        """

    os.system(f"mv user_country_data.csv user_data")
    return 0

#delete after
if __name__=="__main__":
    main()
