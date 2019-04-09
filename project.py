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


# КЛАСС С ИГРАМИ
class GameProject():

	@staticmethod
	# ПОЛУЧИТЬ ГОРОДА ИЗ ТЕКСТОВОГО БЛОКНОТА В МАССИВЕ
	def getCityList():
		city = []

		handle = open("city.txt", "r", encoding='utf-8')
		data = handle.readlines()
		for i in data:
			city.append(i.replace('\n', ''))
		handle.close()
		return city


		#ОСНОВНОЙ КОД ИГРЫ "УГАДАЙ ЧИСЛО"
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
							if (body.lower().isdigit()):	# проверка на число

								if(int(num_r) == int(body.lower())):
									text = 'Поздравляю, ты угадал число'
									vk.method("messages.send", {"peer_id": id, "random_id": random.randrange(1,30000, 1), "message":text})
									break
								if(i == 0):
									text = 'К сожалению, вы не угадали число\nЧисло - '+str(num_r)
									vk.method("messages.send", {"peer_id": id, "random_id": random.randrange(1,30000, 1), "message":text})
									break
								elif(int(num_r) > int(body.lower()) and int(body.lower()) > 0 and int(body.lower()) < 100):
									text = 'Заданное число больше (введите "выход", чтобы выйти)\nОсталось ' + str(i) + ' попыток'
									vk.method("messages.send", {"peer_id": id, "random_id": random.randrange(1,30000, 1), "message":text})	
									i = i-1
								elif(int(num_r) < int(body.lower()) and int(body.lower()) > 0 and int(body.lower()) < 100):
									text = 'Заданное число меньше (введите "выход", чтобы выйти)\nОсталось ' + str(i) + ' попыток'
									vk.method("messages.send", {"peer_id": id, "random_id": random.randrange(1,30000, 1), "message":text})
									i = i-1
								else:
									text = 'Число должно быть от 1 до 100'
									vk.method("messages.send", {"peer_id": id, "random_id": random.randrange(1,30000, 1), "message":text})

								sleep(1)
							else:# если сообщение не число - выводим ошибку
								if(body.lower() == 'выход'):
									break
								else:
									vk.method("messages.send", {"peer_id": id, "random_id": random.randrange(1,30000, 1), "message":'Введите число или "выход", чтобы выйти'})	
					break	
				else:
					vk.method("messages.send", {"peer_id": id, "random_id": random.randrange(1,30000, 1), "message":'Не понимаю вас\nВведите "играть", чтобы начать игру или "выход", для того чтобы выйти из игры'})

	# ОСНОВНОЙ КОД ИГРЫ "ГОРОДА"
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

# КЛАСС МЕНЮ
class Menu():
	@staticmethod
	def showMenu():
		menu_array = ['Список команд:', 'игра - Игра "Угадай число"',  'города - Игра "Города"', 'тв - узнать телепрограмму на сегодня']
		menu = ''
		for i in menu_array:
			menu = menu + i + '\n' 
		return menu

# КЛАСС ФУНКЦИИ ПОКАЗА TV ПРОГРАММ
class showTVProgrammProject():

	#ОСНОВНОЙ КОД ФУНКЦИИ ПОКАЗА TV ПРОГРАММ
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

	# ПОЛУЧИТЬ HTML КОД СТРАНИЦЫ С САЙТА TV ПРОГРАММ
	def getHtmlTVProgramm(url):
		client = requests.session()
		html = client.get(url)
		return html.text

	# ИЗЪЯТИЕ ИЗ HTML КОДА СТРАНИЦЫ РАСПИСАНИЯ ПЕРЕДАЧ
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
					tv_name = i.find('div', {'class':'p-programms__item__inner'}).find('span', {'class':'p-programms__item__name'}).find('span', {'class':'p-programms__item__name__link'}).contents[0]
					tv_time = i.find('div', {'class':'p-programms__item__inner'}).find('span', {'class':'p-programms__item__name'}).find('span', {'class':'p-programms__item__time'}).find('span', {'class':'p-programms__item__time__value'}).contents[0]
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

	# ПОЛУЧЕНИЕ НАЗВАНИЯ ВСЕХ TV ПРОГРАММ
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



# ОСНОВНОЙ КОД БОТА
vk = vk_api.VkApi(token="c1395815b2cdc88151901fe1fe1f50863fd89694dc593749bcb53217b89375ba6b2a50b724f528e9c29a7")

while True:
	try:
		messages = vk.method("messages.getConversations", {"offset": 0, "count": 20, "filter": "unread"})
		if messages["count"] >= 1:
			id = messages["items"][0]["last_message"]["from_id"]
			body = messages["items"][0]["last_message"]["text"]
			if "привет" in body.lower():
				vk.method("messages.send", {"peer_id": id, "random_id": random.randrange(1,30000, 1), "message":"Привет"})
			elif "/игра" in body.lower():
				GameProject.guessNumber(vk, 6)
				vk.method("messages.send", {"peer_id": id, "random_id": random.randrange(1,30000, 1), "message":"Вы вышли"})
			elif "/меню" in body.lower():
				menu = Menu.showMenu()
				vk.method("messages.send", {"peer_id": id, "random_id": random.randrange(1,30000, 1), "message":menu})
			elif "/города" in body.lower():
				GameProject.cityGame(vk)
				vk.method("messages.send", {"peer_id": id, "random_id": random.randrange(1,30000, 1), "message":"Вы вышли"})
			elif "/тв" in body.lower():
				url = "https://tv.mail.ru/kemerovo/"
				showTVProgrammProject.getNumTVFromUser(vk, url)
				vk.method("messages.send", {"peer_id": id, "random_id": random.randrange(1,30000, 1), "message":"Вы вышли"})
			else:
				text = "Не понимаю тебя"
				vk.method("messages.send", {"peer_id": id, "random_id": random.randrange(1,30000, 1), "message":text})
		sleep(1)	
	except Exception as e:
		print("Ошибка")
		sleep(1)