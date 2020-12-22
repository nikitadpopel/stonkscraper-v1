from bs4 import BeautifulSoup
import urllib.request, os, platform, time, csv, requests
from scraper import *

import matplotlib.pyplot as plt

def inputDate(dateprompt,command):
    dateloop = 1
    while dateloop == 1:
        userinput_date = input(dateprompt)
        if len(userinput_date) == 10:
            if userinput_date[4] == '-' and userinput_date[-3] == '-':
                try:
                    int(userinput_date[0:3])
                    int(userinput_date[5:6])
                    int(userinput_date[8:9])
                    command
                    dateloop = 0
                except:
                    print('Date Error: Make sure characters between Hyphens are integers!')
            else:
                print('Date Error: Make sure you format date using Hyphens!')
        else:
            print('Date Error: Character count too low; expected 10, but recieved', len(userinput_date))

def isDate(userinput_date):
    if len(userinput_date) == 10:
        if userinput_date[4] == '-' and userinput_date[-3] == '-':
            try:
                int(userinput_date[0:3])
                int(userinput_date[5:6])
                int(userinput_date[8:9])
                return True
            except:
                print('Date Error: Make sure characters between Hyphens are integers!')
        else:
            print('Date Error: Make sure you format date using Hyphens!')
    else:
        print('Date Error: Character count too low; expected 10, but recieved', len(userinput_date))

if __name__ == '__main__':
    prompt_inputstock = 'Enter the stock that you would like to look up: '
    userstocksymbol = input(f'\n*********************************\n* Welcome to the Stonk Scraper! *\n*********************************\n{prompt_inputstock}').upper()
    loop = 1
    while loop == 1:
        currstock = Stock(0,userstocksymbol)
        try:
            currentstate_line1 = 'Date: ' + str(currstock.getCurrent()[0]) + '\tOpening Price($): ' + str(round(float(currstock.getCurrent()[1]),2)) + '\tClosing Price($): ' + str(round(float(currstock.getCurrent()[4]),2)) + '\t|'
            currentstate_line2 = 'Daily Low($): ' + str(round(float(currstock.getCurrent()[3]),2)) + '\tDaily High($): ' + str(round(float(currstock.getCurrent()[2]),2)) + '\t\tDaily Volume: ' + str(round(float(currstock.getCurrent()[6]),2)) + '\t|'
            print('\n\t\t\t' + ('-' * (len(currstock.getName())+4))+'\n\t\t\t| '+ currstock.getName() + ' |')
            print(('-' * len(currentstate_line1)) + '\n' + currentstate_line1 + '\n' + currentstate_line2 + '\n' + ('-' * len(currentstate_line1)))


            plt.plot(currstock.getCloses())
            plt.show()
        except:
            pass
        userinput = input('What would you like to do next?\n[S]earch by Date\t[C]ompare over Time\t[N]ew Stock\t[Q]uit\n> ').upper()
        if userinput == 'S':
            """
            dateloop = 1
            while dateloop == 1:
                userinput_date = input('Input your desired date (Format: YYYY-MM-DD): ')
                if isDate(userinput_date) == True:
                    for i in currstock.getHistory():
                        if userinput_date in i[0]:
                            print(i)
                            dateloop = 0
            """
            dateprompt = 'Input your desired date (Format: YYYY-MM-DD): '
            userinput_date = input(dateprompt)
            inputDate(dateprompt,[print(i) for i in currstock.getHistory() if userinput_date in i[0]])

        elif userinput == 'C':
            print('Input the dates in chronological order')
            dateloop = 1
            while dateloop == 1:
                userinput_date1 = input('Date #1 (Format: YYYY-MM-DD): ')
                if isDate(userinput_date1) == True:
                    dateloop = 0
            dateloop = 1
            while dateloop == 1:
                userinput_date2 = input('Date #2 (Format: YYYY-MM-DD): ')
                if isDate(userinput_date2) == True:
                    dateloop = 0
            print(currstock.compareStock(userinput_date1,userinput_date2))
        elif userinput == 'N':
            userstocksymbol = input(prompt_inputstock).upper()
        elif userinput == 'Q':
            print('Quitting!')
            loop = 0
        else:
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n! Try Again. That was not one of the options! !\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
