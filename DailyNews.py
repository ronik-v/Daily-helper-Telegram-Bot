from bs4 import BeautifulSoup
from urllib.request import urlopen


class DailyNews:
    def __init__(self):
        self.URL = "https://www.rbc.ru/short_news"
        self.soup = BeautifulSoup(urlopen(self.URL).read(), "html.parser")
        self.news_with_urls = dict()

    def __call__(self) -> dict:
        news_list, news_url_list = self.soup.find_all("span", attrs={"class": "item__title rm-cm-item-text"}), \
                                   self.soup.find_all("a", attrs={"class": "item__link"})
        for news, url in zip(news_list, news_url_list):
            news = str(news)
            self.news_with_urls[news[42 + 68:len(news) - 68]] = url.get("href")
        return self.news_with_urls
