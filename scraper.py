from bs4 import BeautifulSoup
import urllib.request, os, platform, time, csv, requests

# Below is the function that checks whether or not the stock symbol that the user
# inputted is a valid stock symbol recognized by the NASDAQ, NYSE, and other
# exchanges
"""
def checkexist(input):
    if:
        return True
    else:
        return False
"""

def



stockexchanges = ['nasdaq','nyse']
for n,i in enumerate(stockexchanges):
    stockexchanges[n] = [i, f'stocksymbols-{i}.csv']
# stockexchanges = [[exchange,filename],[exchange,filename]]

### danpos

platspecific = os.getcwd()
if platform.system().lower() == 'windows':
    platspecific += '\\'
elif platform.system().lower() == 'debian' or platform.system().lower() == 'linux':
    platspecific += '/'

"""
for exchange in stockexchanges:
    if os.path.exists(os.getcwd() + '/' + exchange[1]) == True:
        print(f'{exchange[1]} EXISTS')
    else:
        start = time.time()
        url = f'https://old.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange={exchange[0]}&render=download'
        samplelista = urllib.request.urlretrieve(url, platspecific + exchange[1])
        print(time.time() - start)
"""

userstocksymbol = input().upper()
csv_file = csv.reader(open(stockexchanges[1][1], "r"), delimiter = ',')
stockexists = False
for row in csv_file:
    if userstocksymbol == row[0]:
        stockexists = True
if stockexists == True:
    """
    currentstockurl = 'https://finance.yahoo.com/quote/' + userstocksymbol
    print(currentstockurl)
    currentpage = requests.get(currentstockurl)
    soup = BeautifulSoup(currentpage.content, 'html5lib')
    mydivs = soup.findAll('span', {'class': 'Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)'})
    temp1 = str(str(mydivs[0]).split('>')[1]).split('<')
    print(str(temp1[0]))
    """

    req = requests.get(f'https://query1.finance.yahoo.com/v7/finance/download/{userstocksymbol}?period1=0&period2=9999999999&interval=1d&events=history&includeAdjustedClose=true')
    price_table = req.content.decode('utf-8').split('\n')
    price_table = [i.split(',') for i in req.content.decode('utf-8').split('\n')]
    xtemp1 = 2002
    xtemp2 = 0
    price_table.pop(0)
    for i in price_table:
        print(i)
        xtemp2 = int(i[0][:4])
        if xtemp2 > xtemp1:
            xtemp1 = xtemp2
            print('\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n')
else:
    print('This shit does not exist, GTFO')
