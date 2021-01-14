from tkinter import messagebox
from urllib.parse import urlparse
import validators
import requests
from bs4 import BeautifulSoup

def invalid_url_error():
    messagebox.showinfo('Invalid URL', 'Enter a Nexus mod URL')
    
class ParseURL():
    
    def parse_nexus_url(url):
        if len(url)==0:
            invalid_url_error()
            return None
        elif validators.url(url) != True:
            invalid_url_error()
            return None
        parsed_url = urlparse(url)
        hostsite = parsed_url.netloc
        protoc = parsed_url.scheme
        try:
            category = parsed_url.path.split('/')[2]
        except:
            invalid_url_error()
            return None
        if protoc not in ['https','http']:
            messagebox.showinfo('Invalid URL', '"https://" or "http://" is required at at the beginning of the URL.')
            return None
        elif hostsite not in ['nexusmods.com','www.nexusmods.com']:
            invalid_url_error()
            return None
        elif category != 'mods':
            invalid_url_error()
            return None
        else:
            #parse inserted URL
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            title_soup = soup.find('meta', property='og:title')
            if title_soup is None or title_soup['content'] == 'Mod unavailable':
                messagebox.showinfo('Error', 'No valid mod data found.')
                return None
            #retrieve desired information and insert into information list
            info = []
            info.append(url.split('?')[0])
            info.append(title_soup['content'])
            info.append(soup.find('meta', property='og:site_name')['content'][14:])
            info.append(soup.find('meta', property='og:description')['content'])
            info.append(soup.find('meta', property='twitter:data1')['content'])
        info.append('Nexus')
        return info
