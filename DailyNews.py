from bs4 import BeautifulSoup
from urllib.request import urlopen
from models import Parser, News, ABC
from create_connection import connection


class DailyNews(Parser, ABC):
    URL = "https://www.rbc.ru/short_news"
    soup = BeautifulSoup(urlopen(URL).read(), "html.parser")

    @classmethod
    def get_news_text_exception(cls, url: str, _class: str) -> str:
        text_soup = BeautifulSoup(urlopen(url).read(), "html.parser")
        try:
            article_title = text_soup.find("div", attrs={"class": _class})
            result = article_title.find("span").text.replace("\n", "")
            if len(result) < 150:
                return " "
            return result
        except AttributeError:
            return " "

    @classmethod
    def get_news_text(cls, url: str) -> str:
        _class = ["article__text article__text_free", "article__text__overview"]
        first_title, second_title = cls.get_news_text_exception(url, _class[0]), cls.get_news_text_exception(url, _class[1])
        if first_title == second_title:
            return first_title
        if first_title == str():
            return second_title
        return first_title

    @classmethod
    def get_data(cls) -> list[News]:
        all_news: list[News] = []
        news_list, news_url_list = cls.soup.find_all("span", attrs={"class": "item__title rm-cm-item-text "
                                                                             "js-rm-central-column-item-text"}), \
            cls.soup.find_all("a", attrs={"class": "item__link rm-cm-item-link js-rm-central-column-item-link"})
        for news, url in zip(news_list, news_url_list):
            news = str(news)
            news_obj = News(
                title=news[42 + 68:len(news) - 68],
                text=cls.get_news_text(url.get("href")),
                url=url.get("href")
            )
            all_news.append(news_obj)
        return all_news

    @classmethod
    def to_db(cls) -> None:
        news: list[News] = cls.get_data()
        conn = connection()
        cur = conn.cursor()
        for news_obj in news:
            sql_request = f"INSERT INTO FinNews(title, text, url) " \
                          f"VALUES('{news_obj.title}', '{news_obj.text}', '{news_obj.url}')"
            cur.execute(sql_request)
            conn.commit()
        conn.close()

    @classmethod
    def table_name(cls) -> str:
        return 'FinNews'
