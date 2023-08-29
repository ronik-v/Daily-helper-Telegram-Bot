from abc import ABC, abstractmethod


class Parser(ABC):
	@classmethod
	@abstractmethod
	def get_data(cls) -> list[object]:
		pass

	@classmethod
	@abstractmethod
	def to_db(cls) -> None:
		pass

	@classmethod
	@abstractmethod
	def table_name(cls) -> str:
		pass


# Objects to insert in database...
class Rate:
	def __init__(self, rate_text: str, rate_symbol: str, sum_rub: float):
		self.rate_text = rate_text
		self.rate_symbol = rate_symbol
		self.sum_rub = sum_rub


class News:
	def __init__(self, title: str, text: str, url: str):
		self.title = title
		self.text = text
		self.url = url
