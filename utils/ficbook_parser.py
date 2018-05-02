import logging

import requests
from bs4 import BeautifulSoup
import re

url = 'https://ficbook.net/find?title=&fandom_filter=any&fandom_group_id=1&sizes%5B%5D=4&pages_min=&pages_max=&ratings%5B%5D=9&transl=&status=&directions%5B%5D=1&directions%5B%5D=2&directions%5B%5D=3&directions%5B%5D=4&directions%5B%5D=7&directions%5B%5D=6&warnings%5B%5D=27&warnings%5B%5D=14&warnings%5B%5D=13&warnings%5B%5D=28&warnings%5B%5D=26&warnings%5B%5D=60&likes_min=&likes_max=&sort=random&rnd=491794192&find=Найти%21#result'


def run(steps=700):
    for i in range(steps):
        r = requests.get(url)
        html = r.text
        soup = BeautifulSoup(html, 'html.parser')

        titles = soup.find_all('a', attrs={'class': 'visit-link'})
        for title in titles:
            link = title.attrs['href']

            fic_id = re.search(r'[0-9]{4,9}', link).group(0)
            logging.info(fic_id)
            fic = requests.get(f"https://ficbook.net/fanfic_download/txt/{fic_id}").text
            with open(f"../texts/{fic_id}", 'w') as f:
                f.write(fic)
