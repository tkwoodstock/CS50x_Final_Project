import matplotlib.pyplot as plt
from matplotlib import colors
import os


#---------FUNCTIONS FOR USE IN APP--------


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


#Note: visualise() no longer used in countries web app, chart.js used instead to generate graphs
#      however, this function remains in this file for later reference if required

def visualise(countries: list, field):

    #no visualisation for alphabetical order metric
    if field == "Country":
        #print("\n--Countries sorted by name have no graphic visualisation, please choose another metric--")
        return False

    #get color scheme
    base_colors1 = ['#cceeff' , '#aaddff' , '#88ccff' , '#77bbff' , '#66aaff' , '#5599ff' , '#3388ff' , '#006aff' , '#0055cc' , '#004099'] #list of 10 blue shades for plot
    base_colors2 = ['#ffe6cc' , '#ffcc99' ,  '#ffbf80' , '#ffb366' , '#ffa64d' , '#ff9933' , '#ff8c1a' , '#ff8000' , '#e67300' , '#cc6600'] #list of 10 orange shades for plot
    select_colors = [] # add the number of colors required from the number of countries selected

    #for i in range(len(countries)):
        #select_colors.append(base_colors[i])


    #create list of names for x axis
    names_list = []
    for i in countries:
        names_list.append(i["Country"])

    x_axis = []
    num_tags = []
    for i , item in enumerate(names_list):
        name = ""
        if " " in item:
            temp = item.split()
            for word in temp:
                if word.lower() != "and":
                    name += word[0].upper()
        else:
            name = item
        x_axis.append(name)
        num_tags.append(i)


    #for life expectancy
    if field == "Life Expectancy":
        m_life_exp = []
        f_life_exp = []

        removed = 0
        for i , data in enumerate(countries):
            male = data[field]["Male"]
            female = data[field]["Female"]

            if male == "N/A" and female == "N/A":
                x_axis.remove(x_axis[i-removed])
                removed += 1
            else:
                if male == "N/A":
                    m_life_exp.append(None)
                else:
                    m_life_exp.append(male)

                if female == "N/A":
                    f_life_exp.append(None)
                else:
                    f_life_exp.append(female)

        plot_list = [m_life_exp , f_life_exp]

        #plot list is life expectancy in format: [male , female]

        plt.figure(figsize=(12,6))

        fig , ax = plt.subplots()

        ax.scatter(x_axis , plot_list[0] , color = "blue")
        ax.scatter(x_axis , plot_list[1] , color = "magenta")
        plt.title("Life Expectancy by Country")
        #plt.xlabel("Country")
        plt.ylabel("Years")
        plt.legend(["Male" , "Female"])
        plt.setp(ax.get_xticklabels(), rotation=20)
        plt.savefig(f"static/images/Life_Expectancy.png")
        #os.system("code Life_Expectancy.png")
        #pause = input("\nSee visual in file: 'Life_Expectancy.png'\nPress enter to continue.")
        #os.system("mv Life_Expectancy.png static/images")

        #If there is data, return True to generate a graph
        """
        for gender in plot_list:
            for data in gender:
                if data != None:
                    return True

        #Return False if all data in array is None (i.e., N/A)
        return False
        """
        if len(x_axis) > 0:
            return True
        else:
            return False


    #for population
    if field == "Population":

        plot_list = []
        removed = 0 # number of x axis elements that have been removed due to N/A fields

        for i , data in enumerate(countries):
            if data[field] == "N/A":
                #remove country from x axis list if no data available (so it is not plotted)
                x_axis.remove(x_axis[i-removed])
                removed += 1

            else:
                plot_list.append(data[field])

        plt.figure(figsize=(12,6))

        plt.bar(x_axis , plot_list , color = base_colors1)


        #plt.xlabel("Country")

        plt.title("Population by Country")
        plt.ylabel("Million People")

        plt.savefig(f"static/images/{field}.png")
        #os.system(f"code {field}.png")
        #pause = input(f"\nSee visual in file: '{field}.png'\nPress enter to continue.")
        #os.system(f"mv {field}.png static/images")

        #If there is data, return True to generate a graph, otherwise return False
        if len(x_axis) > 0:
            return True
        else:
            return False


    #for GDP and CO2
    else:
        plot_list = []
        subplot_list = []
        removed = 0 # number of x axis elements that have been removed due to N/A fields

        for i , data in enumerate(countries):
            if data[field] == "N/A":
                #append a zero for plotting purposes
                #plot_list.append(0)
                #subplot_list.append(0)
                x_axis.remove(x_axis[i-removed])
                removed += 1

            else:
                plot_list.append(data[field])
                if field == "GDP":
                    per_cap = data[field] / data["Population"]
                    subplot_list.append(per_cap)
                elif field == "CO2":
                    per_cap = data[field] / data["Population"]
                    subplot_list.append(per_cap)


        plt.figure()


        fig, axs = plt.subplots(2, figsize=(25,15))

        axs[0].bar(x_axis , plot_list , color=base_colors1)
        axs[1].bar(x_axis , subplot_list , color=base_colors2)
        axs[0].tick_params(labelsize = 18)
        axs[1].tick_params(labelsize = 18)


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


        plt.savefig(f"static/images/{field}.png")
        #os.system(f"code {field}.png")
        #pause = input(f"\nSee visual in file: '{field}.png'\nPress enter to continue.")
        #os.system(f"mv {field}.png static/images")


        #If there is data, return True to generate a graph, otherwise return False
        if len(x_axis) > 0:
            return True
        else:
            return False
