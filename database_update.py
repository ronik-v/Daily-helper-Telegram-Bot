from Finance import GetInfoAboutRate
from DailyNews import DailyNews
from create_connection import connection
from threading import Timer


def update() -> None:
	conn = connection()
	cur = conn.cursor()
	cur.execute(f'DELETE FROM {GetInfoAboutRate.table_name()}')
	cur.execute(f'DELETE FROM {DailyNews.table_name()}')
	conn.close()
	GetInfoAboutRate.to_db(); DailyNews.to_db()
	Timer(900, update).start()


if __name__ == '__main__':
	update()
