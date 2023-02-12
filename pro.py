#ProxyFinder is a tool to search free proxies around the web
#git: https://github.com/richardparker6103/proxyfinder/

import requests
import sys
import datetime
import os
import time
import colorama
from bs4 import BeautifulSoup
from threading import Thread
from prettytable import PrettyTable

#HEADERS TO PREVIVE SOME ERRORS IN LOADING PAGE
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
'Accept-Encoding': 'none',
'Accept-Language': 'en-US,en;q=0.8',
'Connection': 'keep-alive'}

colorama.init()

BOLD = '\033[1m'
CYAN = BOLD + '\033[36m'
NORMAL = BOLD + '\033[37m'
YELLOW = BOLD + '\033[33m'
RED = BOLD + '\033[31m'
GREEN = BOLD + '\033[32m'

PROXIES_SITE = "https://www.freeproxy.world" #WHERE SEARCH FOR
#TESTING WEBSITE
URL = {
    'http': "http://testphp.vulnweb.com",
    'https': "https://microsoft.com" 
}

# CREATE LISTS FOR FUTURE VALUES
IP_LIST = []
#VALUES FROM THE WEBSITE PROXIES
PORT_LIST = ['80', '8080', '3128']
ANON_LEVEL = ['4']
COUNTRY_LIST = []
IP_PORT = []
ANON_LIST = []
HTTP_ON = []
HTTPS_ON = []
SOCKS4_ON = []
SOCKS5_ON = []

def freeproxyworld(protocol, verbose):
    # CREATING AN TABLE TO SIMPLIFY READING
    results = PrettyTable()
    results.field_names = ["COUNTRY", "IP", "Anonymity"]
    results.align["COUNTRY"] = "l"
    results.align["IP"] = "l" #ALIGN RESULTS TO THE LEFT SIDE
    results.align["ANONYMITY"] = "l"
    # HERE STARTS THE ENGINE
    print("Starting Proxyfinder...")
    print("Searching for {} proxies in {} with {} timeout(ms)".format(protocol, PROXIES_SITE, TIME_OUT))
    time.sleep(5)
    # LETS START SEARCH WITH OUR PORTS DEFINED IN PORT_LIST
    for port in PORT_LIST:
        for n in ANON_LEVEL:
            r = requests.get(PROXIES_SITE + "/?anonymity=" + n + "&/?port=" + port, headers=hdr)
            response = BeautifulSoup(r.content, 'lxml')
            for ip in response.find_all('td', {'class': 'show-ip-div'}): #RETRIEVE ONLY IP'S FROM
                if n == "1":
                    ANON_LIST.append("Weak")
                if n == "4":
                    ANON_LIST.append("Strong") 
                IP_LIST.append(ip.get_text().strip())
                formatted_ip = ip.get_text().strip() + ":" + port    #FORMAT ENTRY TO ALIGN IP:PORT
                IP_PORT.append(formatted_ip)
            for country in response.find_all('span', {'class': 'table-country'}):
                COUNTRY_LIST.append(country.get_text().strip()) #DONT NEED FORMAT BECAUSE IT'S ONLY COUNTRY VALUE
    for x, y, z in zip(COUNTRY_LIST, IP_PORT, ANON_LIST):
        results.add_row([x, y, z])
    if IP_PORT:
        x = 0
        print(results)
        for x in range(int(len(IP_PORT))):
            x = x + 1
        r = input("Proxyfinder has found {} values\nDo you want to test all of them ? [Y/n]".format(x))
        if r == "n":
            exit()
        else:
            test_proxies(protocol)
    else:
        print(RED + "Proxyfinder was not found any results in ", PROXIES_SITE)
        exit()


def test_proxies(protocol):
    if protocol == "http":
        now = datetime.datetime.now()
        #print("\nProxyfinder starting at: ", now.hour, ":", now.minute, ":", now.second)
        print("Opening connections with {} through {} proxies servers.".format(URL['http'], len(IP_PORT)))
        print("Current timeout: {}".format(TIME_OUT))
        time.sleep(5)
        for i in IP_PORT:
            try:
                # HERE SET THE PROXY IN DICTIONARY (YOU NEED SET THIS VALUE OR IT IS NOT WORKING)  
                proxy = {
                    "http": "http://" + i
                }
                resp = requests.post(URL['http'], proxies=proxy, headers=hdr, timeout=TIME_OUT)
                if resp.status_code == 200:
                    print(GREEN + "{} is UP, received response <200> from {}".format(i, URL['http']) + NORMAL)
                    HTTP_ON.append(proxy['http'])
                else:
                    print(RED + "{} is down.".format(i)+ NORMAL)
            except Exception as f:
                if verbose == True:
                    print(RED, f, NORMAL)
                else:
                    print(RED + "" + i + " connection timed out , try " + YELLOW + "--verbose" + RED + """ to see it or increase the time search value with""" + YELLOW + " --force (MORE SLOW!)" + NORMAL)

        print("\nFound", len(HTTP_ON), "proxy servers online.\n")        
        for r in HTTP_ON:
            print(GREEN + r + NORMAL)
        if (len(HTTP_ON)) == 0:
            print(RED + "Appears to be empty results in this search, you must try rerun with --force" + NORMAL)
            time.sleep(2)
            exit()
    if protocol == "https":
        print("Opening connections with {} through {} proxies servers.".format(URL['https'], len(IP_PORT)))
        time.sleep(2)


if ("-v" or "--verbose") in sys.argv:
    verbose = True
else:
    verbose = False

if "--force" in sys.argv:
    TIME_OUT = 5
if "--faster" in sys.argv:
    TIME_OUT = 0.5
if "--fast" in sys.argv:
    TIME_OUT = 1
else:
    TIME_OUT = 2

    
freeproxyworld("http", verbose)