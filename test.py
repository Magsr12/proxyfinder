import requests
import os
import time
import colorama
from bs4 import BeautifulSoup
from prettytable import PrettyTable

#TEXT COLORS
colorama.init()

BOLD = '\033[1m'
CYAN = BOLD + '\033[36m'
NORMAL = BOLD + '\033[37m'
YELLOW = BOLD + '\033[33m'
RED = BOLD + '\033[31m'
GREEN = BOLD + '\033[32m'

# PAGE WHERE THE PROXIES SERVERS ARE
HTTP_PROXIES = "https://www.freeproxy.world/?port=80"

# HEADERS BELOW HERE TO PREVINE HTTP PAGE ERROR
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
'Accept-Encoding': 'none',
'Accept-Language': 'en-US,en;q=0.8',
'Connection': 'keep-alive'}


def main(verbose=False):
    results = PrettyTable()
    results.field_names = ["COUNTRY", "IP", "PORT"]
    results.align["IP"] = "l" #ALIGN RESULTS TO THE LEFT SIDE
    results.align["COUNTRY"] = "l"
    x = 0
    IP_LIST = []
    PORT_LIST = []
    COUNTRY_LIST =[]
    r = requests.get(HTTP_PROXIES, headers=hdr) #SELECT HEADERS TO PREVINE HTTP PAGE ERROR
    response = BeautifulSoup(r.content, 'lxml')
    for ip in response.find_all('td', {'class': 'show-ip-div'}): #RETRIEVE ONLY IP'S
        IP_LIST.append(ip.get_text().strip())
        if verbose: #SHOW ON SCREEN THE PROCESS
            print(IP_LIST[x])
            time.sleep(0.1)
            x += 1
    for port in response.find_all('a', {'href': '/?port=80'}):  #RETRIEVE TRUST HTTP PORTS(NOT ONLY RANDOM)
        PORT_LIST.append(port.get_text().strip())
    
    for country in response.find_all('span', {'class': 'table-country'}):
        COUNTRY_LIST.append(country.get_text().strip())

    for country_retrieved, ip_retrieved, port_retrieved in zip(COUNTRY_LIST, IP_LIST, PORT_LIST):
        results.add_row([country_retrieved, ip_retrieved, port_retrieved])
    
    print(results)
        

    #print(len(IP_LIST))
    #print(len(PORT_LIST))
    

main()

