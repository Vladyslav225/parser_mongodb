import requests
from bs4 import BeautifulSoup

from mongoengine import *


class BotWords(Document):
    all_words = StringField(required=True, unique=True)

url = 'https://slovnyk.ua/index.php'
    
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

get_div_class_letter = soup.find_all('div', {'class': 'letter'})

for tag_a in get_div_class_letter:
    get_tag_a = tag_a.find_all('a')

    for text in get_tag_a:
        get_text = f'Слова на букву {text.text}'

    for href in get_tag_a:
        get_href = 'https://slovnyk.ua/' + href.get('href')

        response = requests.get(get_href)
        soup = BeautifulSoup(response.text, 'html.parser')

        for tag_a_class_cont_link in soup.find_all('a', {'class': 'cont_link'}):
            get_tag_a_class_cont_link = 'https://slovnyk.ua/' + tag_a_class_cont_link['href']
            
            response = requests.get(get_tag_a_class_cont_link)
            soup = BeautifulSoup(response.text, 'html.parser')
                    
            for words in soup.find_all('a', {'class': 'cont_link'}):
                get_words = words.text

                if len(get_words) <= 2:
                    continue

                try:

                    connect('db_words_bot_and_users')
                    a = BotWords(all_words = get_words)
                    a.save()

                except:
                    print(f'This word is in the database: {get_words}')
