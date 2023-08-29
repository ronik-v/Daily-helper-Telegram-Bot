from bs4 import BeautifulSoup
from urllib.request import urlopen
from models import Parser, Rate, ABC
from create_connection import connection


def tag_to_string(obj):
    for pos in range(len(obj)):
        obj[pos] = str(obj[pos])
    return obj


class GetInfoAboutRate(Parser, ABC):
    URL = "https://www.cbr.ru/currency_base/daily/"  # Central bank website
    soup = BeautifulSoup(urlopen(URL).read(), "html.parser")

    @classmethod
    def get_data(cls) -> list[Rate]:
        all_cur: list[Rate] = []
        exchange_rates = cls.soup.find_all("tr")[1:]
        for rate in exchange_rates:
            cur_obj = tag_to_string(rate.find_all("td")[1:])
            cost = cur_obj[3][4:len(cur_obj[3]) - 5]
            cost = float(str(cost).replace(",", "."))
            val = int(cur_obj[1][4:len(cur_obj[1]) - 5])
            if val != 1:
                cost /= val
            cost = round(cost, 3)

            rate = Rate(
                rate_text=cur_obj[2][4:len(cur_obj[2]) - 5],
                rate_symbol=cur_obj[0][4:len(cur_obj[0]) - 5],
                sum_rub=cost
            )
            all_cur.append(rate)
        return all_cur

    @classmethod
    def to_db(cls) -> None:
        rates: list[Rate] = cls.get_data()
        conn = connection()
        cur = conn.cursor()
        for rate in rates:
            sql_request = f"INSERT INTO Rates(rate_text, rate_symbol, sum_rub) " \
                          f"VALUES('{rate.rate_text}', '{rate.rate_symbol}', {rate.sum_rub})"
            cur.execute(sql_request)
            conn.commit()
        conn.close()

    @classmethod
    def table_name(cls) -> str:
        return 'Rates'
