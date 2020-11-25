import requests as r
import parse
from bs4 import BeautifulSoup, element
from API.time import TimeISO

URL = "https://syndication.twitter.com/timeline/profile?screen_name=%s"

def GetTweets(usr, items):
    if "@" == usr[0]: usr = usr[1:]
        
    res = r.get(URL%usr)
    res = res.json()["body"]
    soup = BeautifulSoup(res, 'html.parser')
    tss = soup.find_all("p", {'class', 'timeline-Tweet-text'})

    res = []
    for ts in tss:
        text = []
        for t in ts.children:
            if isinstance(t, element.NavigableString):
                text.append(str(t))
            else:
                if t.name == 'br': text.append('/n')
                else:
                    text.extend(['\n', t.text])
    
        res.append(''.join(text))
    
    return res