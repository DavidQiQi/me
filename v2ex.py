#-*-coding:utf-8-*-
# Author: david.qi 
# mail: davis.ying@gmail.com

import requests
from bs4 import BeautifulSoup as bs
import re

s = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0',
    'Host': 'v2ex.com',
    'Referer': 'http://v2ex.com/signin',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
}


r = s.get('http://v2ex.com/signin')
if r.status_code == 200:

    soup = bs(r.text, 'html.parser')
    once = soup.findAll(name='input', attrs={'name': 'once'})[0]['value']
    print once

    names = soup.findAll(name='input', attrs={'class':'sl'})
    user = names[0]['name']
    pwd = names[1]['name']

    login_data = {user: '', pwd: '', 'once': once, 'next': '/'}

    s.post('http://v2ex.com/signin', data=login_data, headers=headers)
    f = s.get('http://v2ex.com/', headers=headers)


    url2 = 'http://v2ex.com/mission/daily'
    headers['Referer'] = 'http://v2ex.com'
    result = s.get(url2, headers=headers).content
    balance = "location.href = '/balance'"

    if balance not in result:
        soup = bs(result, 'html.parser')
        misurl = soup.findAll(name='input', attrs={'class': 'super normal button'})[0]['onclick']
        #print type(missurl.encode('UTF-8'))
        ree = re.compile('/\w+/\w+/\w+\?\w+=\d+')
        #print type(headers['Referer'])
        missurl = re.findall(ree, misurl.encode('UTF-8'))
        #print missurl
        logurl = headers['Referer'] + missurl[0]
        #print logurl
        headers['Referer'] = url2
        result = s.get(logurl, headers=headers).content
        soup1 = bs(result, 'html.parser')
        print soup1.findAll(name='div', attrs={'class': 'message'})[0]
    else:
        soup = bs(result, 'html.parser')
        for i in soup.findAll(name='span', attrs={'class': 'gray'})[0].strings:
            print i
else:
    print r.status_code