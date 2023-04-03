from bs4 import BeautifulSoup
from urllib.request import urlopen


class GetInfoAboutRate:
    def __init__(self):
        self.URL = "https://www.cbr.ru/currency_base/daily/"  # Сайт ЦБ РФ
        self.soup = BeautifulSoup(urlopen(self.URL).read(), "html.parser")
        self.all_cur = list()

    def tag_to_string(self, obj):
        for pos in range(len(obj)):
            obj[pos] = str(obj[pos])
        return obj

    def __call__(self) -> list:
        exchange_rates = self.soup.find_all("tr")[1:]
        for rate in exchange_rates:
            cur_obj = self.tag_to_string(rate.find_all("td")[1:])
            cost = cur_obj[3][4:len(cur_obj[3]) - 5]
            cost = float(cost[:2] + "." + cost[3:])
            val = int(cur_obj[1][4:len(cur_obj[1]) - 5])
            if val != 1:
                cost /= val
            cost = round(cost, 2)
            add_to_all_cur = f"{cur_obj[2][4:len(cur_obj[2]) - 5]} ({cur_obj[0][4:len(cur_obj[0]) - 5]}) --- {cost} RUB"
            self.all_cur.append(add_to_all_cur)
        return self.all_cur
