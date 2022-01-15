from bs4 import BeautifulSoup
import requests
from BotTypes import *
import hashlib
from urllib.request import urlopen, Request
import time
import re

class New:
    photo_path = ""
    title = ""
    text = "" 
    url = ""
    def __init__(self, _photo = None, _title = None, _text = None, _url = None):
        self.photo_path = _photo
        self.title = _title
        self.text = _text
        self.url = _url



class WebNewsParser:

    new = None
    __lastNew = []
    __lastHashs = []
    __firstFlag = True
    __lastUrl = ""
    __updated = False



    def __init__(self):
        for number in range(len(self.__urls)):
            self.__lastHashs.append(0)
            self.__lastNew.append(New())
        self.__checkUpdate()
        
    def __checkUpdate(self):
        while True:
            for number in range(len(self.__urls)):
                if self.__updated == False:                    
                    page = requests.get(self.__urls[number][0])

                    soup = BeautifulSoup(page.content, "html.parser")
                    # results = soup.find("div", class_='b-content b-content_catalog')

                    currHash = hashlib.md5(soup.text.encode()).hexdigest()

                    if currHash != self.__lastHashs[number]:

                        if self.__firstFlag == True:
                            self.firstFlag = False
                        else:
                            if self.__lastUrl != self.__urls[number]: #Проверяем, что предыдущая новость не с этого же сайта
                                self.__urls[number][1](self) #Получаем новость с выбранного сайта
                                if self.__lastNew[number] != self.new: #Проверяем, что последняя новость с этого сайта изменилась
                                    self.__postNews() #Выводим информацию в телеграм канал, если информация новая
                                    self.__lastNew[number] = self.new #Обновляем последнюю новость с этого сайта
                                    self.__updated = True # Указываем, что новость уже выложили, и дальше ничего проверять не нужно

                        self.__lastUrl = self.__urls[number] # Сохраняем последний URL новости
                    self.__lastHashs[number] = currHash # Обновляем последний хеш этого сайта

            time.sleep(60 * 60 * 5) #one hour
            self.__updated = False


    def __parseSite_izdotru(self):
        URL = "https://iz.ru/tag/iurist"
        page = requests.get(URL)

        soup = BeautifulSoup(page.content, "html.parser")

        results = soup.find("a", class_='lenta_news__day__list__item show_views_and_comments')
        title = results.find("div", class_='lenta_news__day__list__item__title')

        href = "https://iz.ru" + results['href']


        page = requests.get(href)

        soup = BeautifulSoup(page.content, "html.parser")

        photo = soup.find("div", class_='big_photo__img')
        if photo != None:
            photo = photo.find("img")
            if photo != None:
                photo = "https:" + photo['data-src']

        self.new = New(photo, title, None, URL)#"https://rg.ru" + title['href'])
        pass


    def __parseSite_alrfdotru(self):
        URL = "https://alrf.ru/news/"
        page = requests.get(URL)

        soup = BeautifulSoup(page.content, "html.parser")

        results = soup.find("div", class_='news-list__item')
        photo = results.find(class_="news-list__item_photo")
        if photo != None:
            photo = photo['style']
        result = re.search(r"\(([A-Za-z0-9_/.-]+)\)", photo).group(1)
        title = results.find(class_="news-list__item_title")
        text = results.find(class_="news-list__item_description")
        self.new = New("https://alrf.ru/" + result,title,text, URL)#"https://rg.ru" + title['href'])
        pass

    def __parseSite_rgdotru(self):
        URL = "https://rg.ru/tema/gos/pravo/"
        page = requests.get(URL)

        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find("div", class_='b-news-inner__list-item')
        photo = results.find(class_="b-news-inner__list-item-image")
        if photo != None:
            photo = photo['src']
        title = results.find(class_="b-link b-link_title")
        text = results.find(class_="b-news-inner__list-item-text")
        self.new = New("https:" + photo,title,text, URL)#"https://rg.ru" + title['href'])
        pass

    def __postNews(self,):
        if self.new.photo_path != None:
            if self.new.title != None:
                if self.new.text != None:
                    bot.send_photo(GROUPCHAT, caption=f"<b>{self.new.title.text}</b>\n{self.new.text.text}\n<i>Источник информации:</i> {self.new.url}",photo=self.new.photo_path, parse_mode= "html")
                else:
                    bot.send_message(GROUPCHAT,text=f"<b>{self.new.title.text}</b>\n<i>Источник информации:</i> {self.new.url}", parse_mode= "html")
            else:
                bot.send_message(GROUPCHAT,text=f"{self.new.text.text}\n<i>Источник информации:</i> {self.new.url}", parse_mode= "html")
        else:
            if self.new.title != None:
                if self.new.text != None:
                    bot.send_message(GROUPCHAT,text=f"<b>{self.new.title.text}</b>\n{self.new.text.text}\n<i>Источник информации:</i> {self.new.url}", parse_mode= "html")
                else:
                    bot.send_message(GROUPCHAT,text=f"<b>{self.new.title.text}</b>\n<i>Источник информации:</i> {self.new.url}", parse_mode= "html")
            else:
                bot.send_message(GROUPCHAT,text=f"{self.new.text.text}\n<i>Источник информации:</i> {self.new.url}", parse_mode= "html")
        pass
    
    
    __urls = [
        ( "https://rg.ru/tema/gos/pravo/" ,  __parseSite_rgdotru ),
        ( "https://alrf.ru/news/", __parseSite_alrfdotru),
        ( "https://iz.ru/tag/iurist", __parseSite_izdotru)
    ]