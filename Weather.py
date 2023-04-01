from config import open_weather_token
import datetime
import requests


class GetWeather:
    def __init__(self, city):
        self.city = city
        self.result = []

    def __call__(self) -> list:
        code_to_smile = {
            "Clear": "Ясно \U00002600",
            "Clouds": "Облачно \U00002601",
            "Rain": "Дождь \U00002614",
            "Drizzle": "Дождь \U00002614",
            "Thunderstorm": "Гроза \U000026A1",
            "Snow": "Снег \U0001F328",
            "Mist": "Туман \U0001F32B"
        }
        try:
            r = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={open_weather_token}&units=metric")
            data = r.json()
            city = data["name"]
            cur_weather = data["main"]["temp"]
            weather_description = data["weather"][0]["main"]
            if weather_description in code_to_smile:
                wd = code_to_smile[weather_description]
            else:
                wd = "Не могу определить погоду."

            humidity = data["main"]["humidity"]
            pressure = data["main"]["pressure"]
            wind = data["wind"]["speed"]
            sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
            sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
            length_of_the_day = datetime.datetime.fromtimestamp(
                data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
                data["sys"]["sunrise"])
            self.result.append(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
            self.result.append(f"Погода в городе: {city}")
            self.result.append(f"Температура: {cur_weather}C {wd}")
            self.result.append(f"Влажность: {humidity}%")
            self.result.append(f"Давление: {pressure} мм.рт.ст")
            self.result.append(f"Ветер: {wind} м/с")
            self.result.append(f"Восход солнца: {sunrise_timestamp}")
            self.result.append(f"Закат солнца: {sunset_timestamp}")
            self.result.append(f"Продолжительность светового дня: {length_of_the_day}")
            return self.result
        except BaseException:
            return [f"Пожалуйста, проверьте корректность названия вашего города. Вы ввели - {self.city}"]
