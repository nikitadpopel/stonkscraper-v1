# This was created by Danila Popel and Nikita Popel. This project was originally created on December 20th, 2020.

from bs4 import BeautifulSoup
import urllib.request, os, platform, time, csv, requests
from datetime import datetime, timedelta

# Below is the function that checks whether or not the stock symbol that the user
# inputted is a valid stock symbol recognized by the NASDAQ, NYSE, and other
# exchanges

def checkExist(userstocksymbol):
    #tickersymbols = [i[1] for i in [i.split('|') for i in ''.join([i.decode('utf-8') for i in urllib.request.urlopen('ftp://ftp.nasdaqtrader.com/symboldirectory/nasdaqtraded.txt')]).split('\n')][1:-2]]
    tickersymbols = []
    for i in urllib.request.urlopen('ftp://ftp.nasdaqtrader.com/symboldirectory/nasdaqtraded.txt'):
        tickersymbols.append(''.join(i.decode('utf-8').split('\n')).split('|')[1])
    if userstocksymbol in tickersymbols[1:-1]:
        return True
    else:
        return False

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
def decrementDate(userinput_date):
    return (datetime.strptime(userinput_date, '%Y-%m-%d') - timedelta(days=1)).strftime('%Y-%m-%d')
# Below is the definition of our stock class
class Stock:
    # This is the instantiation of our Stock
    def __init__(self, history, userstocksymbol):
        self.symbol = userstocksymbol
        #if checkExist(self.symbol) == True:
        req = requests.get(f'https://query1.finance.yahoo.com/v7/finance/download/{userstocksymbol}?period1=0&period2=9999999999&interval=1d&events=history&includeAdjustedClose=true')
        self.history = req.content.decode('utf-8').split('\n')
        self.history = [i.split(',') for i in req.content.decode('utf-8').split('\n')][1:]
        currentstockurl = 'https://finance.yahoo.com/quote/' + self.symbol
        currentpage = requests.get(currentstockurl)
        soup = BeautifulSoup(currentpage.content, 'html5lib')
        mydivs = soup.findAll('h1', {'data-reactid' : '7'})
        self.name = str(str(mydivs[0]).split('>')[1]).split('<')[0]
        """else:
            print('You entry is not a valid stock symbol.')"""
    def getHistory(self):
        return self.history
    def getSymbol(self):
        return self.symbol
    def getCurrent(self):
        return self.history[-1]
    def setExchange(self):
        currentstockurl = 'https://finance.yahoo.com/quote/' + self.symbol
        currentpage = requests.get(currentstockurl)
        soup = BeautifulSoup(currentpage.content, 'html5lib')
        mydivs = soup.findAll('span', {'data-reactid' : '9'})
        exchange = str(str(mydivs[0]).split('>')[1]).split(' -')
        return str(exchange[0])
    def getName(self):
        return self.name
    def getDates(self):
        return [i[0] for i in self.history]
    def getCloses(self):
        return [float(i[4]) for i in self.history]
    def compareStock(self, date1, date2):
        for n,i in enumerate(self.history):
            if date1 in i[0]:
                date1_index = n
            if date2 in i[0]:
                date2_index = n

        if float(self.history[date1_index][4]) < float(self.history[date2_index][4]):
            isGain = True
            output = 'the percentage change since ' + str(date1) + ' is +'
        else:
            isGain = False
            output = 'the percentage change since ' + str(date1) + ' is -'
        percentage_change = ((float(self.history[date1_index][4]) - float(self.history[date2_index][4])) / float(self.history[date1_index][4])) * (-100)
        output += str(round(percentage_change, 2)) + '%'
        return output
    def checkDate(self, userinput_date):
        for i in self.getHistory():
            if userinput_date in i:
                return True
        return False
    def fixDate(self, userinput_date):
        #currstock.fixDate()
        fixloop = 1
        datechanged = 0
        while fixloop == 1:
            if self.checkDate(userinput_date) == True:
                fixloop = 0
            elif self.checkDate(userinput_date) == False:
                userinput_date = decrementDate(userinput_date)
                #userinput_date = f'{userinput_date[0:8]}{int(userinput_date[8:10])-1}'
                datechanged = 1
        if datechanged == 1:
            print('Using results for closest date (' + userinput_date + ').')
        return [i for i in self.getHistory() if userinput_date in i][0]
