import logging

import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote

url = 'http://lurkmore.to/Служебная:Random'


def run(steps=1000):
    for i in range(steps):
        r = requests.get(url)
        html = r.text
        soup = BeautifulSoup(html, 'html.parser')

        paragraphs = soup.find_all('p')
        article = []
        for p in paragraphs:
            text = p.get_text()
            article.append(text)

        text = '\n'.join(article)
        name = r.request.path_url[1:]
        name = unquote(name).replace('/', '|')

        with open(f"../texts/{name}", 'w') as f:
            logging.info(name)
            f.write(text)
