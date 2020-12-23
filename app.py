# This was created by Danila Popel and Nikita Popel. This project was originally created on December 20th, 2020.

from bs4 import BeautifulSoup
import urllib.request, os, platform, time, csv, requests
from datetime import datetime, timedelta
from scraper import *

if __name__ == '__main__':
    # Welcome to the StonkScraper V1 (terminal)!
    prompt_inputstock = 'Enter the stock that you would like to look up?\n> '
    print('\n*********************************\n* Welcome to the Stonk Scraper! *\n*********************************')
    introloop = 1
    while introloop == 1:
        userstocksymbol = input(prompt_inputstock).upper()

        # If the 'userstocksymbol' exists in 'tickersymbols' stock symbol directory within 'checkExist()' on 'scraper.py'
        # After the 'userstocksymbol' input above, run 'checkExist()' from 'scraper.py' to check if the stock exists and return a bool value that allows the variable to pass into 'mainloop' wihle loop.
        # But if the 'userstocksymbol' does not pass 'checkExist()', the user is notified that their stock does not exist and 'introloop' while loop reruns to reprompt the user for a new input.
        if checkExist(userstocksymbol) == True:
            mainloop = 1
            while mainloop == 1:
                currstock = Stock(0,userstocksymbol)
                date_string = 'Date: ' + str(currstock.getCurrent()[0]) + ' ' * (40 - len('Date: ' + str(currstock.getCurrent()[0])))
                opening_string = 'Opening Price($): ' + str(round(float(currstock.getCurrent()[1]),2)) + ' ' * (40 - len('Opening Price($): ' + str(round(float(currstock.getCurrent()[1]),2))))
                closing_string = 'Closing Price($): ' + str(round(float(currstock.getCurrent()[4]),2)) + ' ' * (40 - len('Closing Price($): ' + str(round(float(currstock.getCurrent()[4]),2))))
                low_string = 'Daily Low($): ' + str(round(float(currstock.getCurrent()[3]),2)) + ' ' * (40 - len('Daily Low($): ' + str(round(float(currstock.getCurrent()[3]),2))))
                high_string = 'Daily High($): ' + str(round(float(currstock.getCurrent()[2]),2)) + ' ' * (40 - len('Daily High($): ' + str(round(float(currstock.getCurrent()[2]),2))))
                volume_string = 'Daily Volume: ' + str(round(float(currstock.getCurrent()[6]),2)) + ' ' * (40 - len('Daily Volume: ' + str(round(float(currstock.getCurrent()[6]),2))))
                name_string = '| ' + currstock.getName() + ' |\tExchange: ' + currstock.getExchange()
                out_line1 = '| ' + date_string + opening_string + closing_string + ' |'
                out_line2 = '| ' + low_string + high_string + volume_string + ' |'
                namelen = len(currstock.getName())
                print('\n' + (' ' * int((120 - namelen) / 2)) + '+' + ('-' * (namelen + 2)) + '+\n' + (' ' * int((120 - namelen) / 2)) + name_string)
                print('+' + ('-' * (int((120 - namelen) / 2)-1)) + '+' + ('-' * (namelen + 2)) + '+' + ('-' * (120 - (int((120 - namelen) / 2) - 1) - (namelen + 2))) + '+\n' + out_line1 + '\n' + out_line2 + '\n+' + ('-' * (len(out_line1)-2)) + '+')

                # 'stockloop' while loop is to prevent the user from wasting time continuously requesting info from the scraper using the 'Stock()'(currstock) from 'scraper.py'.
                # 'stockloop' asks for the 'userinput' input to retrieve content from stock.
                stockloop = 1
                while stockloop == 1:
                    userinput = input('\nWhat would you like to do next?\n[S]earch by Date\t[C]ompare over Time\t[N]ew Stock\t[Q]uit\n> ').upper()

                    # userinput Input: [S]earch by Date
                    # Search by Date asks for YYYY-MM-DD formatted date, checks for correct formatting.
                    # If the market was closed on the user's given day, the day's value will subtract until it reaches a market open day.
                    # As an output, the item in currstock.getHistory() with a matching date will be printed.
                    if userinput == 'S':
                        dateloop = 1
                        while dateloop == 1:
                            userinput_date = input('Input your desired date (Format: YYYY-MM-DD): ')
                            if isDate(userinput_date) == True:
                                print(currstock.fixDate(userinput_date))
                                dateloop = 0

                    # userinput Input: [C]ompare over Time
                    # Same checking process as in '[S]earch by Date' but for two user inputted values: date1(old date) & date2(new date)
                    # As an output, the percent return of the 'current price' between the date1(old date) and date2(new date) will be printed
                    elif userinput == 'C':
                        print('Input the dates in chronological order (Start Date first, then more Latest Date).')
                        dateloop = 1
                        while dateloop == 1:
                            userinput_date1 = input('Start Date (Format: YYYY-MM-DD): ')
                            if isDate(userinput_date1) == True:
                                userinput_date1 = currstock.fixDate(userinput_date1)[0]
                                dateloop = 0
                        dateloop = 1
                        while dateloop == 1:
                            userinput_date2 = input('Latest Date (Format: YYYY-MM-DD): ')
                            if isDate(userinput_date2) == True:
                                userinput_date2 = currstock.fixDate(userinput_date2)[0]
                                dateloop = 0
                        print(currstock.compareStock(userinput_date1,userinput_date2))

                    # userinput Input: [N]ew Stock
                    # Close the 'stockloop' while loop, reprompt user with 'mainloop' while loop
                    # In 'mainloop', if userinput is 'N', close 'mainloop', reprompt user with 'introloop' while loop
                    # In 'introloop', user is reprompted with 'userstocksymbol' input to select a new stock symbol to rerun the program.
                    elif userinput == 'N':
                        stockloop = 0

                    # userinput Input: [Q]uit
                    # Quit the program.
                    elif userinput == 'Q':
                        print('Quitting Program!')
                        quit()
                    else:
                        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n! Try Again. That was not one of the options! !\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

                # Continuation of 'stockloop' "if userinput == 'N'" statement!
                # If the 'stockloop' while loop is closed, the if statement below is prompted.
                # If the 'userinput' from 'stockloop' is 'N', close 'mainloop', reprompt user with 'introloop' while loop
                # In 'introloop', user is reprompted with 'userstocksymbol' input to select a new stock symbol to rerun the program.
                if userinput == 'N':
                    mainloop = 0
        else:
            print('You entry is not a valid stock symbol.')
