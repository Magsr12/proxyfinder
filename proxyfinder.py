#ProxyFinder is a tool to search and test free proxies around the web
#git: https://github.com/richardparker6103/proxyfinder/

__version__ = "1.0"

import requests
import sys
import datetime
import os
import time
import queue
import colorama
import argparse
import certifi
import threading
from bs4 import BeautifulSoup
from prettytable import PrettyTable

#HEADERS TO PREVIVE SOME ERRORS IN LOADING PAGE
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
'Accept-Encoding': 'none',
'Accept-Language': 'en-US,en;q=0.8',
'Connection': 'keep-alive'}

banner = """
██████╗░██████╗░░█████╗░██╗░░██╗██╗░░░██╗███████╗██╗███╗░░██╗██████╗░███████╗██████╗░
██╔══██╗██╔══██╗██╔══██╗╚██╗██╔╝╚██╗░██╔╝██╔════╝██║████╗░██║██╔══██╗██╔════╝██╔══██╗
██████╔╝██████╔╝██║░░██║░╚███╔╝░░╚████╔╝░█████╗░░██║██╔██╗██║██║░░██║█████╗░░██████╔╝
██╔═══╝░██╔══██╗██║░░██║░██╔██╗░░░╚██╔╝░░██╔══╝░░██║██║╚████║██║░░██║██╔══╝░░██╔══██╗
██║░░░░░██║░░██║╚█████╔╝██╔╝╚██╗░░░██║░░░██║░░░░░██║██║░╚███║██████╔╝███████╗██║░░██║
╚═╝░░░░░╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝░░░╚═╝░░░╚═╝░░░░░╚═╝╚═╝░░╚══╝╚═════╝░╚══════╝╚═╝░░╚═╝{}
""".format(__version__)

#Start colors 
colorama.init()
BOLD = '\033[1m'
CYAN = BOLD + '\033[36m'
NORMAL = '\033[0;39m '
YELLOW = BOLD + '\033[33m'
RED = BOLD + '\033[31m'
GREEN = BOLD + '\033[32m'

PROXIES_SITE = "https://www.freeproxy.world" #WHERE SEARCH FOR
#TESTING WEBSITE
URL = {
    'http': "http://testphp.vulnweb.com",
    'https': "https://expired.badssl.com",
    'socks4': "https://expired.badssl.com",
    'socks5': "https://expired.badssl.com"
}

# CREATE LISTS FOR FUTURE VALUES
IP_LIST = []
#VALUES FROM THE WEBSITE PROXIES
PROTOCOL_LIST = []
PORT_LIST = ['80', '8080', '3128', '8118']
ANON_LEVEL = ['4']
COUNTRY_LIST = []
IP_PORT = []
ANON_LIST = []
HTTP_ON = []
HTTPS_ON = []
SOCKS_ON = []


def multithreading(thread):
    print("Starting {} threads".format(thread))
    for x in range(THREAD_VALUE):
        t = threading.Thread(target=test_proxies, args=(protocol,))
        t.start()
        t.join()

def freeproxyworld():
    print("Starting Proxyfinder...")
    time.sleep(1)
    if len(PROTOCOL_LIST) == 0:
        print("You have not provide an proxy type (HTTP|HTTPS|SOCKS4|SOCKS5), setting HTTP by default")
        PROTOCOL_LIST.append("http")
        time.sleep(1)
    # CREATING AN TABLE TO SIMPLIFY READING
    print("Creating tables to retrieve page results...")
    time.sleep(1) 
    results = PrettyTable()
    results.field_names = ["COUNTRY", "IP", "Anonymity"]
    results.align["COUNTRY"] = "l"
    results.align["IP"] = "l" #ALIGN RESULTS TO THE LEFT SIDE
    results.align["ANONYMITY"] = "l"
    # HERE STARTS THE ENGINE
    for protocol in PROTOCOL_LIST:
        print("\nSearching for {} proxies in {} with {} timeout(ms)".format(protocol.upper(), PROXIES_SITE, TIME_OUT))
        #LETS START SEARCHING IN OUR SITES PORTS DEFINED IN PORT_LIST (ITS NECESSARY SET UP PORT IN PORT_LIST TO DISCOVER OR IT WILL NOT WORK)
        for port in PORT_LIST:
            for n in ANON_LEVEL:
                r = requests.get(PROXIES_SITE + "/?type=" + protocol + "&/?anonymity=" + n + "&/?port=" + port, headers=hdr)
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
            if dont_ask_input:
                print("\nProxyfinder has found {} {} proxies, proceeding to testing all of them...".format(x, protocol.upper()))                   
                test_proxies(protocol, TIME_OUT)    
            else:
                r = input("Proxyfinder has found {} {} proxies \nDo you want to test all of them ? [Y/n]".format(x, protocol.upper()))
                if r == "n":
                    pass
                else:
                    test_proxies(protocol, TIME_OUT)
        else:
            print(RED + "Proxyfinder was not found any results in ", PROXIES_SITE)
            exit()


def test_proxies(protocol, TIME_OUT):
    count = 0
    errors = 0
    for i in IP_PORT:
        try:
            count = count + 1
            # HERE SET THE PROXY IN DICTIONARY (YOU NEED SET THIS IN A DICT OR THIS WILL NOT WORKING)
            # DONT CHANGE THE ENTRY 'https': 'http://' <------here (even if it is not http)
            # I DIDN'T UNDERSTAND, BUT IF YOU ARE INTERESTED YOU MUST READ THIS 
            # https://urllib3.readthedocs.io/en/1.26.x/advanced-usage.html#https-proxy-error-http-proxy
            proxy = {
                'http': 'http://' + i,
                'https': 'http://' + i # DONT CHANGE THE 'http://' EVEN IF IT IS NOT HTTP 
            }
            print(BOLD + "\n{} of {} proxies tested | ({}://{}) -> {}\n".format(count, len(IP_PORT), protocol, i, URL[protocol]))
            requests.packages.urllib3.disable_warnings() # IGNORE SSL WARNINGS (FROM NO CERTIFICATE ERRORS)
            resp = requests.post(URL[protocol], proxies=proxy, headers=hdr, timeout=TIME_OUT, verify=False)    
            if resp.status_code == 200:
                print(GREEN + "{} is UP, received response <200> from {}".format(i, URL[protocol]) + NORMAL)
                if protocol == "http":
                    HTTP_ON.append(proxy[protocol])
                if protocol == "https":
                    HTTPS_ON.append(proxy[protocol])
                if protocol == "socks":
                    SOCKS_ON.append(proxy[protocol])
            else:
                print(RED + "{} is down, received response <{}> from {}".format(i, resp.status_code, URL[protocol])+ NORMAL)
        except Exception as f:
            errors = errors + 1
            if (len(IP_PORT) / 2) == errors:
                if dont_ask_input:
                    print(YELLOW + "Proxyfinder is not finding any expressive result, increasing timeout limit to {}".format(TIME_OUT + 1) + NORMAL)
                    time.sleep(2)
                    TIME_OUT = TIME_OUT + 1
                else:
                    ask = input(YELLOW + "Proxyfinder is not finding any expressive result, do you want to increase the timeout limit ? [Y/n]" + NORMAL)
                    if ask.lower() == "n":
                        pass
                    else:
                        TIME_OUT = TIME_OUT + 1
                        print("Increasing timeout limit to {}".format(TIME_OUT))
                        time.sleep(2)
            if verbose:
                print(RED, f, NORMAL)
            if TIME_OUT <= 5:
                print(RED + i + " connection timed out, consider to increase the time search value with" + YELLOW + " --force (MORE SLOW!)" + NORMAL)
            else:
                print(RED + i + " connection timed out, host seems not working" + NORMAL)
    #RETRIEVE THE LENGTH OF VALUES IN HTTP AND HTTPS LIST
    else:
        if len(PROTOCOL_LIST) > 1:
            print("\nProxyfinder finished.\n")
            for pr in PROTOCOL_LIST:
                if pr == "http":
                    for r in HTTP_ON:
                        print(GREEN + r + NORMAL + " Anonymity: 4 (Strong)\n")
                if pr == "https":
                    for h in HTTPS_ON:
                        print(GREEN + h + NORMAL + " Anonymity: 4 (Strong)\n")
                if pr == "socks":
                    for s in SOCKS_ON:
                        print(GREEN + s + NORMAL + " Anonymity: 4 (Strong)\n")
        else:
            if protocol == "http":
                print("\nFinished, ProxyFinder has found", len(list(HTTP_ON)), "http proxy servers online.\n")
                time.sleep(3)
                for r in HTTP_ON:
                    print(GREEN + r + NORMAL + " Anonymity: 4 (Strong)\n")
                if not len(HTTP_ON):
                    print(RED + "Appears to be empty results in this search, you must try rerun with --force" + NORMAL)
                    time.sleep(2)                

            if protocol == "https":
                print("\nQuery finished, proxyfinder has found", len(list(HTTPS_ON)), "HTTPS proxy servers online.\n")
                for r in HTTPS_ON:
                    print(GREEN + r + NORMAL + " Anonymity: 4 (Strong)")
                if not len(HTTPS_ON):
                    print(RED + "Appears to be empty results in this search, you must try rerun with --force" + NORMAL)
                    time.sleep(2)

parser = argparse.ArgumentParser(prog="ProxyFinder")
parser.add_argument('--fast', help='set the server response timeout to 0.5ms', action="store_true")
parser.add_argument('--force', dest="force", help='set the server response timeout to 5ms', action="store_true")
parser.add_argument('--http', help='only retrieve http proxies', action="store_true")
parser.add_argument('--https', help='only retrieve HTTPS proxies)', action="store_true")
parser.add_argument('--batch', action="store_true", dest="dont_ask_input", help='dont ask user input')
parser.add_argument('--socks', action="store_true", dest="socks", help="search for socks4 and socks5 proxies")
parser.add_argument('--all', dest='all', action='store_true', help='activate search for all types of proxies(SOCKS, HTTPS, HTTP)')
parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='turn verbosity on')
args = parser.parse_args()
fast = args.fast
all = args.all
dont_ask_input = args.dont_ask_input
force = args.force
http = args.http
https = args.https
socks = args.socks
verbose = args.verbose

if fast:
    TIME_OUT = 0.5
elif force:
    TIME_OUT = 5
else:
    TIME_OUT = 2
if fast and force:
    print("You cannot use --force with --fast!")
    exit()
if __name__ == "__main__":
    print(banner)
if all:
    ALL_PROTOCOLS = ['http', 'https', 'socks4', 'socks5']
    for _ in ALL_PROTOCOLS:
        PROTOCOL_LIST.append(_)
else:
    if http:
        PROTOCOL_LIST.append('http')
    if https:
        PROTOCOL_LIST.append('https')
    if socks:
        PROTOCOL_LIST.append('socks4')
        PROTOCOL_LIST.append('socks5')

freeproxyworld()

    

