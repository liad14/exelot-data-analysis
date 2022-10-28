from matplotlib import pyplot as plt
import numpy as np
from tabulate import tabulate
import pandas
from unicodedata import category
from math import ceil
from re import T
from sys import displayhook
from tkinter import tix
from tkinter.constants import *
from tkinter.tix import COLUMN, Select
root = tix.Tk()


data = pandas.read_csv("C:\\Users\\liadc\\Desktop\\GettingStarted\\parcelsDeliveredPerDayBySource_2022-09-16_21-05-19.csv",
                       header=0, names=("Year", "Month", "Day", "Partner", "Number of parcels"))

# for sum number of parcels, cast these pandas objects to int
data.astype({'Number of parcels': 'int32'}).dtypes
# counters for months and weeks
numOfMonths = 1
numOfWeeks = 1

# count the num of weeks and months of data
dayInThisWeek = 0
currDay = 0
nextDay = 0

for index, row in data[::-1].iterrows():
    nextDay = row['Day']

    # update the day
    if currDay != nextDay:
        currDay = nextDay
        dayInThisWeek = dayInThisWeek + 1
        # if needed - update the weeks number
        if dayInThisWeek > 7:
            numOfWeeks = numOfWeeks + 1
            dayInThisWeek = 1
        # if needed - update the months number
        if currDay == 1:
            numOfMonths = numOfMonths + 1

# an empty dictionary that will contain partners as keys,
# and an array of number of parcels per week as a value
partnersPerWeek = {}
# an familiar dictionary, for each partner will some per calendary month
partnersPerMonth = {}

datesOfWeeks = [""] * (numOfWeeks + 1)
# will contain the dates of each week for the output file
datesOfWeeks[0] = "Partner"
firstDate = len(data['Day']) - 1
startDateOfWeek = str(data['Day'][firstDate]) + \
    '.' + str(data['Month'][firstDate])
endDateOfWeek = ""

monthsOfData = [0] * (numOfMonths + 1)
monthsOfData[0] = "Partner"

# counter of weeks, (as 20-26/8/2022 is week #0 in the first tested file)
weekCounter = 0

# counter of months
monthCounter = 0

# counter the days for each week
dayInThisWeek = 0
currDay = 0
nextDay = 0
totalParcels = 0

# for each partner, sum the number of parcels per week and per month, and total:
# this for loop iterate the data file,
# where each row represents data about the number of parcels
# that a specific partner made in a specific day
for index, row in data[::-1].iterrows():
    nextDay = row['Day']

    # update the day
    if currDay != nextDay:
        currDay = nextDay
        dayInThisWeek = dayInThisWeek + 1

        # update the dates of this week
        if dayInThisWeek == 7:
            endDateOfWeek = str(row['Day']) + '.' + str(row['Month'])
            datesOfThisWeek = startDateOfWeek + " - " + endDateOfWeek
            datesOfWeeks[weekCounter + 1] = datesOfThisWeek

        elif dayInThisWeek == 8:
            weekCounter = weekCounter + 1
            dayInThisWeek = 1
            startDateOfWeek = str(row['Day']) + '.' + str(row['Month'])

        # update the month
        if nextDay == 1:  # then it's a new month - update it
            monthCounter = monthCounter + 1
            if monthsOfData[monthCounter] == 0:
                monthsOfData[monthCounter] = row['Month'] - 1
            monthsOfData[monthCounter + 1] = row['Month']

    currPartner = row['Partner']
    if not currPartner in partnersPerWeek:
       # add this new partner to weeks dictionary
        weeksNewPartnerArray = [0] * numOfWeeks
        partnersPerWeek.update({currPartner: weeksNewPartnerArray})
       # do so to month dictionary
        monthNewPartnerArray = [0] * numOfMonths
        partnersPerMonth.update({currPartner: monthNewPartnerArray})

    # sum the number of parcels of this day to the corresponding value for this partner
    # in both week and month dictionaries
    parcelsToAdd = row["Number of parcels"]
    partnersPerWeek[currPartner][weekCounter] = partnersPerWeek[currPartner][weekCounter] + \
        parcelsToAdd
    partnersPerMonth[currPartner][monthCounter] = partnersPerMonth[currPartner][monthCounter] + \
        parcelsToAdd
    # sum this day number of parcels to total for this partner
    totalParcels = totalParcels + parcelsToAdd

# end of for loop

# create and sort a total array
numOfPartners = len(partnersPerMonth)
totalPerPartner = [0] * numOfPartners

index = 0
# sum the total number of parcels for each partner (by sum the months nums)
for partner in partnersPerMonth:
    totalThisPartner = 0
    for month in range(len(partnersPerMonth[partner])):
        totalThisPartner = totalThisPartner + partnersPerMonth[partner][month]
    # calculate the percent of this partner total num of the general total
    totalPercent = "{:.2f}".format((totalThisPartner / totalParcels) * 100)
    totalPerPartner[index] = [partner, totalThisPartner, "%" + totalPercent]
    index = index + 1

# sort the partners array accrding to total num of parcels
totalPerPartner.sort(key=lambda row: (row[1],), reverse=True)
# print(totalPerPartner)

# sort the per week data by inserting each row from the 'per week dictionary'
# to a new array by the 'total' array which is sorted
perWeekOutput = [0] * numOfPartners
for index in range(len(perWeekOutput)):
    partnerToAdd = totalPerPartner[index][0]
    parcelsPerWeek = partnersPerWeek[totalPerPartner[index][0]]
    perWeekOutput[index] = [partnerToAdd, * parcelsPerWeek]

# sort the per month data by inserting each row from the 'per month dictionary'
# to a new array by the 'total' array which is sorted
perMonthOutput = [0] * numOfPartners
for index in range(len(perMonthOutput)):
    partnerToAdd = totalPerPartner[index][0]
    parcelsPerMonth = partnersPerMonth[totalPerPartner[index][0]]
    perMonthOutput[index] = [partnerToAdd, * parcelsPerMonth]

# create a csv file with data for each partner per week
outputPerWeek = pandas.DataFrame(perWeekOutput)
# add the months as headline for presentation
weekColumns = {}
index = 0
for COLUMN in outputPerWeek:
    weekColumns[COLUMN] = datesOfWeeks[index]
    index += 1
outputPerWeek.rename(columns=weekColumns, inplace=True)

outputPerWeek.to_csv(
    "C:\\Users\\liadc\\Desktop\\GettingStarted\\outputPerWeek.csv", index=None)


# create a csv file with data for each partner per month
outputPerMonth = pandas.DataFrame(perMonthOutput)
# add the months as headline for presentation
monthColumns = {}
index = 0
for COLUMN in outputPerMonth:
    monthColumns[COLUMN] = monthsOfData[index]
    index += 1
outputPerMonth.rename(columns=monthColumns, inplace=True)

outputPerMonth.to_csv(
    "C:\\Users\\liadc\\Desktop\\GettingStarted\\outputPerMonth.csv", index=None)

# create a csv file with data of the total amount and percentage for each partner
outputTotal = pandas.DataFrame(totalPerPartner)
# add the corresponding headlines for presentation
totalColumns = {0: "Partner", 1: "Total Parcels", 2: "Percent"}
outputTotal.rename(columns=totalColumns, inplace=True)

outputTotal.to_csv(
    "C:\\Users\\liadc\\Desktop\\GettingStarted\\dataTotal.csv", index=None)

outputTotal.groupby(['Partner']).sum().plot(
    kind='pie', y='Total Parcels', autopct='%1.0f%%')


plt.pie(outputTotal['Total Parcels'],
        labels=outputTotal['Partner'], shadow=True)
plt.get_legend().remove()

plt.show()
# outputTotal = outputTotal.reset_index(drop = True)

# dataFrame_to_pie = pandas.DataFrame(outputTotal['Total Parcels'], index = outputTotal['Partner'])

# plot = outputTotal.plot.pie(y = outputTotal['Total Parcels'], figsize=(5, 5))


# def plotPie(partnersTotalDictionary): {
#     print(totalPerPartner.keys())
# }

# plotPie(totalPerPartner)
