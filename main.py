import requests
from bs4 import BeautifulSoup
from time import sleep


headers = {'User-Agentf':
           'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5 (.NET CLR 3.5.30729)'}

def dowload(url):  # скачиваем img
    resp = requests.get(url, stream=True)
    r = open('C:\\Program\\PycharmProjects\\Parser\\im\\' + url.split('/')[-1], 'wb')  # путь для сохр. img
    for value in resp.iter_content(1048576):
        r.write(value)
    r.close()


def get_url():
    for count in range(1, 2):  # кол-во стр.
        url = f'https://scrapingclub.com/exercise/list_basic/?page={count}'
        responce = requests.get(url, headers=headers)
        soup = BeautifulSoup(responce.text, 'lxml')  #html.parser
        data = soup.find_all('div', class_='col-lg-4 col-md-6 mb-4')
        for i in data:
            card_url = 'https://scrapingclub.com' + i.find('a').get('href')
            yield card_url


def array():
    for card_url in get_url():
        responce = requests.get(card_url, headers=headers)
        sleep(1)
        soup = BeautifulSoup(responce.text, 'lxml')
        data = soup.find('div', class_="card mt-4 my-4")
        name = data.find('h3', class_="card-title").text
        price = data.find('h4').text
        text = data.find('p', class_="card-text").text
        url_img = 'https://scrapingclub.com' + data.find('img', class_="card-img-top img-fluid").get('src')
        dowload(url_img)
        yield name, price, text, url_img
