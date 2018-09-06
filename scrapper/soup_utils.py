from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
import re

def get_soup( restaurant_url ):
    ua = UserAgent()
    req  = requests.get(restaurant_url, headers={'User-Agent': ua.chrome})
    soup = BeautifulSoup(req.text, 'html.parser')
    return soup