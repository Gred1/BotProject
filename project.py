#! /usr/bin/env python
# -*- coding: utf-8 -*-

import vk_api
from time import sleep
import random
import requests
from bs4 import BeautifulSoup
from datetime import datetime, date, time
import json
import sys
import sqlite3 as sql



class GameProject():

	@staticmethod

	def getCityList():
		city = []

		handle = open("city.txt", "r", encoding='utf-8')
		data = handle.readlines()
		for i in data:
			city.append(i.replace('\n', ''))
		handle.close()
		return city

	def guessNumber(vk, i):
		messages = vk.method("messages.getConversations", {"offset": 0, "count": 20, "filter": "unread"})
		if messages["count"] >= 1:
			id = messages["items"][0]["last_message"]["from_id"]
			body = messages["items"][0]["last_message"]["text"]
			vk.method("messages.send", {"peer_id": id, "random_id": random.randrange(1,30000, 1), "message":'Это игра "Угадай число"\nВаша задача угадать число от 1 до 100 за '+ str(i) + ' попыток. Я буду подсказывать число больше или меньше.\nВведите "играть", чтобы начать игру или "выход", для того чтобы выйти из игры'})
		while True:
			messages = vk.method("messages.getConversations", {"offset": 0, "count": 20, "filter": "unread"})
			if messages["count"] >= 1:
				id = messages["items"][0]["last_message"]["from_id"]
				body = messages["items"][0]["last_message"]["text"]
				if "выход" in body.lower():
					break
				elif "играть" in body.lower():
					num_r = random.randrange(1, 100)
					vk.method("messages.send", {"peer_id": id, "random_id": random.randrange(1,30000, 1), "message":'Я загадал число. Попробуй угадать'})
					sleep(1)			
					while True:
						messages = vk.method("messages.getConversations", {"offset": 0, "count": 20, "filter": "unread"})
						if messages["count"] >= 1:
							body = messages["items"][0]["last_message"]["text"]
							if (body.lower().isdigit()):	

								if(int(num_r) == int(body.lower())):
									vk.method("messages.send", {"peer_id": id, "random_id": random.randrange(1,30000, 1), "message":'Поздравляю, ты угадал число'})
									break
								if(i == 0):
									vk.method("messages.send", {"peer_id": id, "random_id": random.randrange(1,30000, 1), "message":'К сожалению, вы не угадали число\nЧисло - '+str(num_r)})
									break
								elif(int(num_r) > int(body.lower()) and int(body.lower()) > 0 and int(body.lower()) < 100):
									vk.method("messages.send", {"peer_id": id, "random_id": random.randrange(1,30000, 1), "message":'Заданное число больше (введите "выход", чтобы выйти)\nОсталось ' + str(i) + ' попыток'})	
									i = i-1
								elif(int(num_r) < int(body.lower()) and int(body.lower()) > 0 and int(body.lower()) < 100):
									vk.method("messages.send", {"peer_id": id, "random_id": random.randrange(1,30000, 1), "message":'Заданное число меньше (введите "выход", чтобы выйти)\nОсталось ' + str(i) + ' попыток'})
									i = i-1
								else:
									vk.method("messages.send", {"peer_id": id, "random_id": random.randrange(1,30000, 1), "message":'Число должно быть от 1 до 100'})

								sleep(1)
							else:
								if(body.lower() == 'выход'):
									break
								else:
									vk.method("messages.send", {"peer_id": id, "random_id": random.randrange(1,30000, 1), "message":'Введите число или "выход", чтобы выйти'})	
					break	
				else:
					vk.method("messages.send", {"peer_id": id, "random_id": random.randrange(1,30000, 1), "message":'Не понимаю вас\nВведите "играть", чтобы начать игру или "выход", для того чтобы выйти из игры'})


	def cityGame(vk): # игра города
		messages = vk.method("messages.getConversations", {"offset": 0, "count": 20, "filter": "unread"})
		if messages["count"] >= 1:
			id = messages["items"][0]["last_message"]["from_id"]
			body = messages["items"][0]["last_message"]["text"]
			vk.method("messages.send", {"peer_id": id, "random_id": random.randrange(1,30000, 1), "message":'Это игра "города" с компьтером.\nВведите "город", чтобы начать игру или "выход", чтогбы выйти'})
		while True:
			messages = vk.method("messages.getConversations", {"offset": 0, "count": 20, "filter": "unread"})
			if messages["count"] >= 1:
				id = messages["items"][0]["last_message"]["from_id"]
				body = messages["items"][0]["last_message"]["text"]
				if "выход" in body.lower():
					break
				elif "город" in body.lower():
					num_r = random.randrange(1, 100)
					vk.method("messages.send", {"peer_id": id, "random_id": random.randrange(1,30000, 1), "message":'Начали'})

					#получаем массив городов
					city = GameProject.getCityList()

					#рандомный город
					num_r = random.randrange(1, 500)
					main_city = city[num_r]
					if(main_city == ''):
						main_city = city[num_r + 1]
					city.remove(main_city)
					random_city = main_city
					vk.method("messages.send", {"peer_id": id, "random_id": random.randrange(1,30000, 1), "message":random_city})

					while True:
						messages = vk.method("messages.getConversations", {"offset": 0, "count": 20, "filter": "unread"})
						if messages["count"] >= 1: # ход игрока
							body = messages["items"][0]["last_message"]["text"]
							# проверка на последнюю букву
							smech = -1
							if(main_city[-1] == 'ь' or main_city[-1] == 'ъ' or main_city[-1] == 'ы'):
								smech = -2

							if body.lower().title() in city and body.lower()[0] == main_city[smech]:

								main_city = body.lower()
								i3 = 0
								smech = -1
								city.remove(body.lower().title())
								# проверка на последнюю букву
								if(main_city[-1] == 'ь' or main_city[-1] == 'ъ' or main_city[-1] == 'ы'):
									smech = -2
								for i3 in range(len(city)):
									if(city[i3] == ''):
										continue
									elif(str(city[i3][0]) == str(main_city[smech]).title()):
										print('лох')
										rand_city = random.randrange(1, 15)
										main_city = city[i3+rand_city]
										while main_city == '':
											main_city = city[i3+rand_city+1]
										print(main_city)
										break


								vk.method("messages.send", {"peer_id": id, "random_id": random.randrange(1,30000, 1), "message":main_city})
								city.remove(main_city)

							elif "выход" in body.lower():
								break
							else:
								print(body.lower())
								vk.method("messages.send", {"peer_id": id, "random_id": random.randrange(1,30000, 1), "message":'Неверно'})
				else:
					vk.method("messages.send", {"peer_id": id, "random_id": random.randrange(1,30000, 1), "message":'Введите "город", чтобы играть или "выход", чтобы выйти'})

class Menu():
	@staticmethod
	def showMenu():
		menu_array = ['Список команд:', 'игра - Игра "Угадай число"',  'города - Игра "Города"', 'тв - узнать телепрограмму на сегодня']
		menu = ''
		for i in menu_array:
			menu = menu + i + '\n' 
		return menu

# показать tv программу
class showTVProgrammProject():

	def getNumTVFromUser(vk, url):
		messages = vk.method("messages.getConversations", {"offset": 0, "count": 20, "filter": "unread"})
		if messages["count"] >= 1:
			id = messages["items"][0]["last_message"]["from_id"]
			body = messages["items"][0]["last_message"]["text"]
			tv_name, html, num_max = showTVProgrammProject.getNamesTVProgramms()
			vk.method("messages.send", {"peer_id": id, "random_id": random.randrange(1,30000, 1), "message":'Введите нужную цифру:\n'+tv_name+'\nВведите "выход", чтобы выйти'})
			while True:
				min_num = 1
				messages = vk.method("messages.getConversations", {"offset": 0, "count": 20, "filter": "unread"})
				if messages["count"] >= 1:
					id = messages["items"][0]["last_message"]["from_id"]
					body = messages["items"][0]["last_message"]["text"]
					if (body.lower().isdigit()):
						if int(body.lower()) <= num_max and int(body.lower()) >= min_num:
							id = messages["items"][0]["last_message"]["from_id"]
							body = messages["items"][0]["last_message"]["text"]

							num = int(body.lower()) - 1
							tv = showTVProgrammProject.getTVProgramm(url, num, html)
							vk.method("messages.send", {"peer_id": id, "random_id": random.randrange(1,30000, 1), "message":tv+'\nВведите "выход", чтобы выйти'})
						else:
							vk.method("messages.send", {"peer_id": id, "random_id": random.randrange(1,30000, 1), "message":'Такого числа нет\nВведите правильное число или "выход", чтобы выйти'})
					elif(body.lower() == "выход"):
						break
					else:
						vk.method("messages.send", {"peer_id": id, "random_id": random.randrange(1,30000, 1), "message":'Введите число или "выход", чтобы выйти'})


	def getHtmlTVProgramm(url):
		client = requests.session()
		html = client.get(url)
		return html.text

	def getTVProgramm(url, num, html):
		soup = BeautifulSoup(html, 'lxml')
		tv = soup.find_all('div', {'class':'p-channels__item'})[num].find('div', {'class':'p-channels__item__info'}).find('div', {'class':'p-channels__item__info__title'}).find('a', {'class':'p-channels__item__info__title__link'}).contents[0]
		try:
			tv_block = soup.find_all('div', {'class':'p-channels__item'})[num].find('div', {'class':'p-programms__items'}).find_all('div', {'class':'p-programms__item'})
			tv_my_block = ''
			for i in tv_block:
				if(i == ''):
					tv_name = ' '
					tv_time = ' '
				else:
					tv_name = (i.find('div', {'class':'p-programms__item__inner'}).find('span', {'class':'p-programms__item__name'}).find('span', {'class':'p-programms__item__name__link'}).contents[0])
					tv_time = (i.find('div', {'class':'p-programms__item__inner'}).find('span', {'class':'p-programms__item__name'}).find('span', {'class':'p-programms__item__time'}).find('span', {'class':'p-programms__item__time__value'}).contents[0])
					tv_my_block = tv_my_block + tv_time + ' - ' + tv_name + '\n'
			tv_my_block_main = tv + '\n' + tv_my_block
			return tv_my_block_main
		except Exception:
			print('Нет')
			tv_my_block_main = ' '
			tv_my_block = ' '
			tv_name = ' '
			tv_time = ' '
			tv_my_block = tv_my_block + tv_time + ' - ' + tv_name + '\n'
			tv_my_block_main = tv + '\n' + tv_my_block
			return tv_my_block_main

	def getNamesTVProgramms():
		html = showTVProgrammProject.getHtmlTVProgramm(url)
		soup = BeautifulSoup(html, 'lxml')
		tv = soup.find_all('div', {'class':'p-channels__item'})
		i2 = 1
		list_channels = ''
		num = []
		for i in tv:
			tv_name = i.find('div', {'class':'p-channels__item__info'}).find('div', {'class':'p-channels__item__info__title'}).find('a', {'class':'p-channels__item__info__title__link'}).contents[0]
			list_channels = list_channels + str(i2)+' - '+tv_name+'\n'
			num.append(i2)
			i2 = i2 + 1 
		return list_channels, html, i2-1

def num_week(): # НОМЕР НЕДЕЛИ
	day_num = date.today().isocalendar()[1]
	if(day_week() == 'Суббота' or day_week() == 'Воскресенье'):
		day_num = day_num + 1

	return day_num



def day_week(): # ДЕНЬ НЕДЕЛИ
	day_of_week_array = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']

	day = date.today()
	day_of_week = datetime.weekday(day)

	if(day_of_week == 5 or day_of_week == 6):
		day_of_week = 0
	else:
		day_of_week = day_of_week + 1

	return day_of_week_array[day_of_week]




def loginweb(login, password, url, url2): # ПАРСИМ СТРАНИЧКУ
	client = requests.session()

	# Retrieve the CSRF token first
	client.get(url)  # sets cookie
	if 'csrftoken' in client.cookies:
	    # Django 1.6 and up
	    csrftoken = client.cookies['csrftoken']
	else:
	    # older versions
	    csrftoken = client.cookies['csrf']

	login_data = dict(username=login, password=password, csrfmiddlewaretoken=csrftoken, next='/')
	r = client.post(url, data=login_data, headers=dict(Referer=url))
	g = client.get(url2)
	return g.text




def get_dz(html, const, const1, const2, const3, const4):
	soup = BeautifulSoup(html, 'lxml')

		# Строчки (2, 8, 15)
		# Предмет (Если правая константа - 5, если правая не константа - 3, если левая константа - 1, если левая не константа - 0)
		# ДЗ(Если правая константа - 6, если правая не константа - 4, если левая константа - 2, если левая не константа - 1)
	num = soup.find('table').find_all('tr')[const].find('td').get('rowspan')
	num = int(num)
	text = ''
	for i in range(const, const+num):
		if(i == const):
			pages_sub = soup.find('table').find_all('tr')[i].find_all('td')[const1].contents
			if(pages_sub == ['\n'] or pages_sub == []):
				continue
			else:
				pages_sub = soup.find('table').find_all('tr')[i].find_all('td')[const1].find('a').find('b').contents
				pages_sub = str(pages_sub)
				pages_sub = pages_sub[20:]
				pages_sub = pages_sub[0:-16]

			dz = soup.find('table').find_all('tr')[i].find_all('td')[const3].contents
			if(dz != ['\n']):
				dz = dz = soup.find('table').find_all('tr')[i].find_all('td')[const3].find('a').contents
				dz = str(dz)
				dz = dz[3:]
				dz = dz[0:-4]
			else:
				dz = '-'



		else:
			pages_sub = soup.find('table').find_all('tr')[i].find_all('td')[const2].contents
			if(pages_sub == ['\n'] or pages_sub == []):
				continue
			else:
				pages_sub = soup.find('table').find_all('tr')[i].find_all('td')[const2].find('a').find('b').contents
				pages_sub = str(pages_sub)
				pages_sub = pages_sub[20:]
				pages_sub = pages_sub[0:-16]

			dz = soup.find('table').find_all('tr')[i].find_all('td')[const4].contents
			if(dz != ['\n']):
				dz = dz = soup.find('table').find_all('tr')[i].find_all('td')[const4].find('a').contents
				dz = str(dz)
				dz = dz[3:]
				dz = dz[0:-4]
			else:
				dz = '-'


		text = text + pages_sub + '  ' + dz + '\n'

	return text




now = date.today()

year = str(now.year)
num_of_week = str(num_week())

url2 = 'https://cabinet.ruobr.ru/child/studies/journal/?year='+year+'&week_num='+num_of_week
url = 'https://cabinet.ruobr.ru/login'

login = 'mamochkin'
password = 'Den67Ifb02'
html = loginweb(login, password, url, url2)


def get_dz_bot():
	if(day_week() == 'Понедельник'):
		return get_dz(html, 2, 1, 0, 2, 1)
	elif(day_week() == 'Вторник'):
		return get_dz(html, 8, 1, 0, 2, 1)
	elif(day_week() == 'Среда'):
		return get_dz(html, 15, 1, 0, 2, 1)
	elif(day_week() == 'Четверг'):
		return get_dz(html, 2, 5, 3, 6, 4)
	elif(day_week() == 'Пятница'):
		return get_dz(html, 8, 5, 3, 6, 4)
	elif(day_week() == 'Суббота'):
		return get_dz(html, 15, 5, 3, 6, 4)




vk = vk_api.VkApi(token="c1395815b2cdc88151901fe1fe1f50863fd89694dc593749bcb53217b89375ba6b2a50b724f528e9c29a7")

while True:
	try:
		messages = vk.method("messages.getConversations", {"offset": 0, "count": 20, "filter": "unread"})
		if messages["count"] >= 1:
			id = messages["items"][0]["last_message"]["from_id"]
			body = messages["items"][0]["last_message"]["text"]
			if "привет" in body.lower():
				vk.method("messages.send", {"peer_id": id, "random_id": random.randrange(1,30000, 1), "message":"Привет"})
			elif "бот дз" in body.lower():
				text_dz = get_dz_bot()
				vk.method("messages.send", {"peer_id": id, "random_id": random.randrange(1,30000, 1), "message":text_dz+'Не работает'})
			elif "игра" in body.lower():
				GameProject.guessNumber(vk, 6)
				vk.method("messages.send", {"peer_id": id, "random_id": random.randrange(1,30000, 1), "message":"Вы вышли"})
			elif "меню" in body.lower():
				menu = Menu.showMenu()
				vk.method("messages.send", {"peer_id": id, "random_id": random.randrange(1,30000, 1), "message":menu})
			elif "города" in body.lower():
				GameProject.cityGame(vk)
				vk.method("messages.send", {"peer_id": id, "random_id": random.randrange(1,30000, 1), "message":"Вы вышли"})
			elif "тв" in body.lower():
				url = "https://tv.mail.ru/kemerovo/"
				showTVProgrammProject.getNumTVFromUser(vk, url)
				vk.method("messages.send", {"peer_id": id, "random_id": random.randrange(1,30000, 1), "message":"Вы вышли"})
			else:
				vk.method("messages.send", {"peer_id": id, "random_id": random.randrange(1,30000, 1), "message":"Не понимаю тебя"})
		sleep(1)	
	except Exception as e:
		print("Ошибка")
		sleep(1)