# ProxyFinder

**Proxyfinder** is a tool to search some proxies around the web, it can fetch this values and test one by one.

## Dependencies
requests
lxml
datetime
colorama
argparse
bs4
prettytable
requests[socks]

You can run the pip to install all of them with:

**pip3 install -r requirements.txt**

## Usage:
**Retrieve simple only HTTP proxies**

 ``python3 proxyfinder.py`` 
 
 **You can use multiples arguments in this script like:*
 ``python3 proxyfinder.py --socks --https --http --batch --force -v``
 
 **Used arguments:**
 
 --https: Retrieve HTTPS proxies
 --http: Retrieve HTTP proxies
 --socks: Retrieve SOCKS4/SOCKS5 proxies
 --batch: Don't ask user input
 --force: Force the timeout limit, this will increase the time of search ( SLOW )
 --fast: Decrease the timeout limit, run more fast but less results ( FAST )
 --all: Search for all types of proxies 
 
button in the file explorer. You can also create folders by clicking the **New folder** button.
