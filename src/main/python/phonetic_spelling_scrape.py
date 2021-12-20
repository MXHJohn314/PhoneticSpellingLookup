import requests
from bs4 import BeautifulSoup

WORD_URL = 'https://www.dictionary.com/browse/bottom'
req = requests.get(WORD_URL)
soup = BeautifulSoup(req.content, 'html.parser')
print(soup.find(class_='pron-spell-content').text[1:-1].strip().split('-'))