#ProxyFinder is a tool to search free proxies around the web
#git: https://github.com/richardparker6103/proxyfinder/

import requests
import os
import time
import colorama
from bs4 import BeautifulSoup
from prettytable import PrettyTable

#HEADERS TO PREVIVE SOME ERRORS IN LOADING PAGE
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
'Accept-Encoding': 'none',
'Accept-Language': 'en-US,en;q=0.8',
'Connection': 'keep-alive'}

PROXIES_SITE = "https://www.freeproxy.world" #WHERE SEARCH FOR
#TESTING WEBSITE
URL = {
    'http': "http://testphp.vulnweb.com",
    'https': "https://microsoft.com" 
}

def search(protocol, page):
    # CREATING AN TABLE TO SIMPLIFY READING
    results = PrettyTable()
    results.field_names = ["COUNTRY", "IP"]
    results.align["COUNTRY"] = "l"
    results.align["IP"] = "l" #ALIGN RESULTS TO THE LEFT SIDE

    # CREATE LISTS FOR FUTURE VALUES
    IP_LIST = []
    PORT_LIST = ['80', '3128', '8000', '8080', '8181', '9002', '9001', '20201', '20000']
    COUNTRY_LIST = []
    IP_PORT = []
    # HERE STARTS THE ENGINE
    # LETS START SEARCH WITH OUR PORTS DEFINED IN PORT_LIST
    for port in PORT_LIST:
        r = requests.get(PROXIES_SITE + "/?port=" + port, headers=hdr)
        response = BeautifulSoup(r.content, 'lxml')
        for ip in response.find_all('td', {'class': 'show-ip-div'}): #RETRIEVE ONLY IP'S FROM 
            IP_LIST.append(ip.get_text().strip())
            formatted_ip = ip.get_text().strip() + ":" + port    #FORMAT ENTRY TO ALIGN IP:PORT
            IP_PORT.append(formatted_ip)
        for country in response.find_all('span', {'class': 'table-country'}):
            COUNTRY_LIST.append(country.get_text().strip()) #DONT NEED FORMAT BECAUSE IT'S ONLY COUNTRY VALUE

    for x, y in zip(COUNTRY_LIST, IP_PORT):
        results.add_row([x, y])
    print(results)

search(True, True)

    

