# This was created by Danila Popel and Nikita Popel. This project was originally created on December 20th, 2020.

from bs4 import BeautifulSoup
import urllib.request, os, platform, time, csv, requests
from datetime import datetime, timedelta
from scraper import *

if __name__ == '__main__':
    prompt_inputstock = 'Enter the stock that you would like to look up?\n> '
    print('\n*********************************\n* Welcome to the Stonk Scraper! *\n*********************************')
    introloop = 1
    while introloop == 1:
        userstocksymbol = input(prompt_inputstock).upper()
        if checkExist(userstocksymbol) == True:
            introloop = 0
        else:
            print('You entry is not a valid stock symbol.')
    mainloop = 1
    while mainloop == 1:
        currstock = Stock(0,userstocksymbol)
        try:
            date_string = 'Date: ' + str(currstock.getCurrent()[0]) + ' ' * (40 - len('Date: ' + str(currstock.getCurrent()[0])))
            opening_string = 'Opening Price($): ' + str(round(float(currstock.getCurrent()[1]),2)) + ' ' * (40 - len('Opening Price($): ' + str(round(float(currstock.getCurrent()[1]),2))))
            closing_string = 'Closing Price($): ' + str(round(float(currstock.getCurrent()[4]),2)) + ' ' * (40 - len('Closing Price($): ' + str(round(float(currstock.getCurrent()[4]),2))))
            low_string = 'Daily Low($): ' + str(round(float(currstock.getCurrent()[3]),2)) + ' ' * (40 - len('Daily Low($): ' + str(round(float(currstock.getCurrent()[3]),2))))
            high_string = 'Daily High($): ' + str(round(float(currstock.getCurrent()[2]),2)) + ' ' * (40 - len('Daily High($): ' + str(round(float(currstock.getCurrent()[2]),2))))
            volume_string = 'Daily Volume: ' + str(round(float(currstock.getCurrent()[6]),2)) + ' ' * (40 - len('Daily Volume: ' + str(round(float(currstock.getCurrent()[6]),2))))
            name_string = '| ' + currstock.getName() + ' |'
            out_line1 = '| ' + date_string + opening_string + closing_string + ' |'
            out_line2 = '| ' + low_string + high_string + volume_string + ' |'
            namelen = len(currstock.getName())
            print('\n' + (' ' * int((120 - namelen) / 2)) + '+' + ('-' * (namelen + 2)) + '+\n' + (' ' * int((120 - namelen) / 2)) + name_string)
            print('+' + ('-' * (int((120 - namelen) / 2)-1)) + '+' + ('-' * (namelen + 2)) + '+' + ('-' * (120 - (int((120 - namelen) / 2) - 1) - (namelen + 2))) + '+\n' + out_line1 + '\n' + out_line2 + '\n+' + ('-' * (len(out_line1)-2)) + '+')
        except:
            pass
        stockloop = 1
        while stockloop == 1:
            userinput = input('\nWhat would you like to do next?\n[S]earch by Date\t[C]ompare over Time\t[N]ew Stock\t[Q]uit\n> ').upper()
            if userinput == 'S':
                dateloop = 1
                while dateloop == 1:
                    userinput_date = input('Input your desired date (Format: YYYY-MM-DD): ')
                    if isDate(userinput_date) == True:
                        print(currstock.fixDate(userinput_date))
                        dateloop = 0
            elif userinput == 'C':
                print('Input the dates in chronological order (Start Date first, then more Latest Date).')
                dateloop = 1
                while dateloop == 1:
                    userinput_date1 = input('Start Date (Format: YYYY-MM-DD): ')
                    if isDate(userinput_date1) == True:
                        userinput_date1 = currstock.fixDate(userinput_date1)[0]
                        dateloop = 0
                        """
                        if isDate(userinput_date1) == True:
                            dateloop = 0
                            """
                dateloop = 1
                while dateloop == 1:
                    userinput_date2 = input('Latest Date (Format: YYYY-MM-DD): ')
                    if isDate(userinput_date2) == True:
                        userinput_date2 = currstock.fixDate(userinput_date2)[0]
                        dateloop = 0
                        """
                        if isDate(userinput_date2) == True:
                            dateloop = 0
                            """
                print(currstock.compareStock(userinput_date1,userinput_date2))
            elif userinput == 'N':
                userstocksymbol = input(prompt_inputstock).upper()
                stockloop = 0
            elif userinput == 'Q':
                print('Quitting!')
                stockloop = 0
            else:
                print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n! Try Again. That was not one of the options! !\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        if userinput == 'Q':
            mainloop = 0
