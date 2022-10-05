import requests
import re
import asyncio
from time import sleep
from bs4 import BeautifulSoup


async def parseKwork(data: list) -> None:
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
	# -----Kwork-----
	print("Зашёл парсить кворк")
	url_kwork = requests.get('https://kwork.ru/projects?c=41', headers=headers).text
	print(url_kwork)
	blocks_kwork = BeautifulSoup(url_kwork, 'lxml').find_all('div', class_=re.compile('wants-card__header-title first-letter breakwords pr250'))
	for block in blocks_kwork:
		data.append(block.find('a').get('href'))

async def parseData() -> list:
	# -----Данные-----
	data = []
	await parseKwork(data)
	return data

def start():
	new_data = asyncio.run(parseData())
	with open('data_url.txt', 'r+') as data_file:
		data = data_file.read().split('\n')
		if new_data != data:
			new_ads = list(set(new_data) - set(data))
			for item in new_ads:
				data_file.write(item + '\n')
				requests.post('https://api.telegram.org/bot5709615986:AAEFinXei7NX-4DR_E1-OqslYgBLueYTplU/sendMessage?chat_id=772328798&text=' + str(item))
	data_file.close()

def work():
	try:
		start()
		sleep(65)
	except Exception as e:
		requests.post('https://api.telegram.org/bot5709615986:AAEFinXei7NX-4DR_E1-OqslYgBLueYTplU/sendMessage?chat_id=772328798&text=' + str(e))
		work()

work()
