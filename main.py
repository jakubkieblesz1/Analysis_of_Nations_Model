import csv
import matplotlib.pyplot as plt
import numpy as np

# Variables are set here.
total_literacy = 0
total_phones = 0
counter_1 = 0
counter_2 = 0
country_data = []
line_count = 0

countryIndex = 0
populationIndex = 1
gdpCapitaIndex = 2
gdpIndex = 3
literacyRateIndex = 4
phonesPerThousandIndex = 5

countryList = []
populationList = []
literacyList = []
literacyRateList = []
gdpList = []
gdpCapitaList = []
phonesPerThou = []
phonesPersonList = []
phonesRateList = []


# This is the function that was written for the purpose of creating all the scatter plots that we need, and we have given it arguments to allow us to customise all the scatter plots individually.
def scatterPlot(w, log_scale, line):
    lists = [[literacyList, gdpList], [phonesPersonList, gdpCapitaList], [literacyRateList, phonesRateList]]
    x = np.array(lists[w][0])
    y = np.array(lists[w][1])

    color = ["royalblue", "seagreen", "blueviolet"]
    labels = [["Literate People", "GDP"], ["Phones per Person", "GDP per Capita"],
              ["Literacy Rate", "Phone Ownership Rate"]]
    savefigList = ["Literate People Vs GDP.png", "Phones per person Vs GDP per capita.png",
                   "Literacy rate Vs Phone ownership rate.png"]
    titleList = ["Literate People Vs GDP", "Phones per Person Vs GDP per Capita",
                 "Literacy Rate Vs Phone Ownership Rate"]

    # Logarithmic scales for the x and y-axis are set for the one graph that needs them.
    if log_scale == True:
        plt.xscale("log")
        plt.yscale("log")

    # Approximate line of best fit for log scales.
    if line == "log":
        x1 = [min(literacyList), max(literacyList)]
        y1 = [min(gdpList), max(gdpList)]
        plt.plot(x1, y1, "ro-", linewidth=2)

    # Actual line of best fit for normal scales.
    elif line == "best":
        a, b = np.polyfit(x, y, 1)
        plt.plot(x, a * x + b, color="red", linewidth=2)

    # The scatter plots are created, customised, and saved.
    plt.scatter(x, y, c=color[w])
    plt.title(titleList[w])
    plt.xlabel(labels[w][0])
    plt.ylabel(labels[w][1])
    plt.tight_layout()
    plt.grid()
    plt.savefig(savefigList[w])
    plt.show()


# Below is the function that creates all the pie charts, it has multiple arguments which allows us to customise each pie chart individually.
def pieChart(d):
    dataIndices = [populationIndex, gdpIndex, phonesPerThousandIndex]
    dataSets = [populationList, gdpList, phonesPerThou]
    titleList = ["Top 10 - Population", "Top 10 - GDP", "Top 10 - Phones per 1000"]
    savefigList = ["Top 10 - Population.png", "Top 10 - GDP.png", "Top 10 - Phones per 1000.png"]
    dataPieList = []
    rankingList = []
    my_explode = (0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    my_colors = [
        ['orchid', 'royalblue', 'lightcyan', 'darkblue', 'cornflowerblue', 'mediumpurple', 'violet', 'lightsteelblue',
         'indigo', 'slateblue'],
        ['olive', 'orange', 'olivedrab', 'darkgoldenrod', 'peru', 'greenyellow', 'gold', 'darkorange', 'darkolivegreen',
         'yellow'],
        ['darkred', 'palevioletred', 'lightpink', 'brown', 'hotpink', 'indianred', 'mistyrose', 'mediumvioletred',
         'lightcoral', 'crimson']]

    # Here, the top 10 countries for the corresponding lists are set and added to the two empty lists.
    print()
    dataSets[d].sort(reverse=True)
    for i in range(0, 10):
        ranking = dataSets[d][i]
        for row in range(len(country_data)):
            if ranking == float(country_data[row][dataIndices[d]]):
                print(i + 1, ".", countryList[row], "-", ranking)
                dataPieList.append(str(countryList[row]))
                rankingList.append(ranking)

    # The pie charts are created, customised, and saved.
    plt.pie(rankingList, labels=dataPieList, startangle=90, shadow=True, explode=my_explode, colors=my_colors[d],
            wedgeprops={"edgecolor": "black", 'linewidth': 1, 'antialiased': True})
    plt.title(titleList[d])
    plt.axis('equal')
    plt.savefig(savefigList[d])
    plt.show()


# File is opened and the useful data is stored in a big list called country_data.
with open("countries of the world.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")

    for row in csv_reader:
        if line_count != 0 and line_count != 224:  # removes categories & Western Sahara
            country = row[0]
            population = row[2]
            gdp_capita = row[8]
            literacy = row[9]
            literacy = literacy.replace(',', '.')  # replaces comma with decimal
            phones = row[10]
            phones = phones.replace(',', '.')  # replaces comma with decimal
            gdp = int(gdp_capita) * int(population)  # overall gdp is calculated
            rowEntry = [country, population, gdp_capita, gdp, literacy, phones]
            country_data.append(rowEntry)
        line_count += 1

    # The corresponding totals and averages are found.
    for row in country_data:
        if (row[4] != ''):
            total_literacy += float(row[4])
            counter_1 += 1

        if (row[5] != ''):
            total_phones += float(row[5])
            counter_2 += 1

    average_literacy = round(total_literacy / counter_1, 1)
    average_phones = round(total_phones / counter_2, 1)

    # The missing data points are filled in with averages.
    for row in country_data:
        if (row[4] == ''):
            row[4] = average_literacy

        if (row[5] == ''):
            row[5] = average_phones

# Here the new cleaned version of the csv file is opened and written to.
filename = "countries_cleaned.csv"
with open(filename, "w") as outfile:
    for i in range(len(country_data)):
        rowStr = str(country_data[i][0]) + ", " + str(country_data[i][1]) + " , " + str(
            country_data[i][2]) + " , " + str(country_data[i][3]) + " , " + str(country_data[i][4]) + " , " + str(
            country_data[i][5])
        outfile.write(rowStr)
        outfile.write("\n")


# This is how the file, countries_cleaned, is structured:
# [country, population, GDP ($ per capita), GDP ($), literacy rate (%), phones per 1000]

# Analysis of cleaned data set
# Below is all the code that will allow users to select which data they want see.

# This is the menu that the user is presented with when the code is run.
def showMenu():
    print("***********************************************************")
    print("**                                                       **")
    print("**   Welcome to the Country Data Grapher                 **")
    print("**                                                       **")
    print("**   What Do You Want to Know?                           **")
    print("**   [Choose 1 - 7]                                      **")
    print("**   (1) Top 10 countries by population:                 **")
    print("**   (2) Top 10 countries by GDP                         **")
    print("**   (3) Top 10 countries by phones per 1000             **")
    print("**   (4) Literate People Vs GDP Graph:                   **")
    print("**   (5) Phones per Person Vs GDP per Capita Graph:      **")
    print("**   (6) Literacy Rate Vs Phone Ownership Rate Graph:    **")
    print("**   (7) Exit:                                           **")
    print("**                                                       **")
    print("***********************************************************")


# Here, all the necessary lists are created for the final analysis.
for i in range(len(country_data)):
    countryList.append(country_data[i][countryIndex])
    populationList.append(int(country_data[i][populationIndex]))
    literacyList.append((float(country_data[i][literacyRateIndex]) / 100) * float(country_data[i][populationIndex]))
    literacyRateList.append(float(country_data[i][literacyRateIndex]))
    gdpList.append(int(country_data[i][gdpIndex]))
    gdpCapitaList.append(int(country_data[i][gdpCapitaIndex]))
    phonesPerThou.append(float(country_data[i][phonesPerThousandIndex]))
    phonesPersonList.append(round(float(phonesPerThou[i]) / 1000, 4))
    phonesRateList.append(round(float(phonesPerThou[i]) / 10, 2))

# This code directs the user through the menu.
key = 0
while key != "7":
    showMenu()
    key = input("\nPlease enter specified number: ")
    if key == "1":
        # Analysing the top 10 countries with relation to population.
        pieChart(0)

    elif key == "2":
        # Analysing the top 10 countries with relation to GDP.
        pieChart(1)

    elif key == "3":
        # Analysing the top 10 countries with relation to phones per 1000.
        pieChart(2)

    elif key == "4":
        # Analysing the correlation between literate population and GDP, (comparing totals).
        scatterPlot(0, True, "log")

    elif key == "5":
        # Analysing the correletion between phones per person and GDP per capita, (comparing 1 to 1).
        scatterPlot(1, False, "best")

    elif key == "6":
        # Analysing the correlation between literacy rate and phone ownership rate, (comparing percentages).
        scatterPlot(2, False, "best")

    elif key == "7":
        # The while loop is ended as the user selected the option to exit.
        break

    else:
        # All other numbers that are not options on the menu screen are just said to be "not an option".
        print("Not an option.")
