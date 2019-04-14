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

 	 		# В методе выводим небольшую инструкцию пользователю. 
 	 		# Задача угадать число от 1 до 100 за n попыток. Бот будет подсказывать число больше или меньше.
 	 		# Необходимо написать "играть", чтобы начать игру или "выход", для того чтобы выйти из игры. 
			text = '''Это игра "Угадай число" 
					Ваша задача угадать число от 1 до 100 за '+ str(i) + ' попыток. Я буду подсказывать число больше или меньше.
					Введите "играть", чтобы начать игру или "выход", для того чтобы выйти из игры'''

			vk.method("messages.send", {"peer_id": id, "random_id": random.randrange(1,30000, 1), "message":text})
		while True:
			messages = vk.method("messages.getConversations", {"offset": 0, "count": 20, "filter": "unread"})
			if messages["count"] >= 1:
				id = messages["items"][0]["last_message"]["from_id"]
				body = messages["items"][0]["last_message"]["text"]

				# проверка текста сообщения
				# Прописываем условия. Если была введена команда “выход”, выходим из цикла и приводим бота в прежнее состояние. Если команда не известная – выводим ошибку.
				if "выход" in body.lower(): 
					break
				elif "играть" in body.lower():
					# Создаем случайное число от 1 до 100 и записываем в переменную num_r
					num_r = random.randrange(1, 100) # получаем рандомное число
					vk.method("messages.send", {"peer_id": id, "random_id": random.randrange(1,30000, 1), "message":'Я загадал число. Попробуй угадать'})
					sleep(1)			
					while True:
						messages = vk.method("messages.getConversations", {"offset": 0, "count": 20, "filter": "unread"})
						if messages["count"] >= 1:
							body = messages["items"][0]["last_message"]["text"]
							# Проверяем значение введенное пользователем на число. Если это не число – выводим ошибку, иначе делаем проверку.
							if (body.lower().isdigit()):
								#  Если пользователь угадал значение num_r – выводим поздравление и выходим из цикла 
								if(int(num_r) == int(body.lower())): # если пользователь угадал число
									text = 'Поздравляю, ты угадал число'
									vk.method("messages.send", {"peer_id": id, "random_id": random.randrange(1,30000, 1), "message":text})
									break

								# если пользователь не угадал число за n попыток - выходим из игры
								if(i == 0): 
									text = 'К сожалению, вы не угадали число\nЧисло - '+str(num_r)
									vk.method("messages.send", {"peer_id": id, "random_id": random.randrange(1,30000, 1), "message":text})
									break

								# если число больше или меньше и находится в диапазоне от 1 до 100 – выводим соответствующее сообщение.
								elif(int(num_r) > int(body.lower()) and int(body.lower()) > 0 and int(body.lower()) < 100): # если число больше
									text = 'Заданное число больше (введите "выход", чтобы выйти)\nОсталось ' + str(i) + ' попыток'
									vk.method("messages.send", {"peer_id": id, "random_id": random.randrange(1,30000, 1), "message":text})	
									i = i-1
								elif(int(num_r) < int(body.lower()) and int(body.lower()) > 0 and int(body.lower()) < 100): # если число меньше
									text = 'Заданное число меньше (введите "выход", чтобы выйти)\nОсталось ' + str(i) + ' попыток'
									vk.method("messages.send", {"peer_id": id, "random_id": random.randrange(1,30000, 1), "message":text})
									i = i-1

								else:
									text = 'Число должно быть от 1 до 100'
									vk.method("messages.send", {"peer_id": id, "random_id": random.randrange(1,30000, 1), "message":text})

								sleep(1)
							else:
								if(body.lower() == 'выход'):
									break
								else:
									text = 'Введите число или "выход", чтобы выйти'
									vk.method("messages.send", {"peer_id": id, "random_id": random.randrange(1,30000, 1), "message":text})	
					break	
				else:
					text = 'Не понимаю вас\nВведите "играть", чтобы начать игру или "выход", для того чтобы выйти из игры'
					vk.method("messages.send", {"peer_id": id, "random_id": random.randrange(1,30000, 1), "message":text})



	# ОСНОВНОЙ КОД ИГРЫ "ГОРОДА"
	def cityGame(vk): # игра города
		messages = vk.method("messages.getConversations", {"offset": 0, "count": 20, "filter": "unread"})
		if messages["count"] >= 1:
			id = messages["items"][0]["last_message"]["from_id"]
			body = messages["items"][0]["last_message"]["text"]

			# Выводим пользователю небольшую инструкцию и отправляемся в цикл.
			text = 'Это игра "города" с компьтером.\nВведите "город", чтобы начать игру или "выход", чтобы выйти'
			vk.method("messages.send", {"peer_id": id, "random_id": random.randrange(1,30000, 1), "message":text})
		while True:
			messages = vk.method("messages.getConversations", {"offset": 0, "count": 20, "filter": "unread"})
			if messages["count"] >= 1:
				id = messages["items"][0]["last_message"]["from_id"]
				body = messages["items"][0]["last_message"]["text"]

				# Далее проверяем на наличие команд “города” или “выход”.
				if "выход" in body.lower():
					break
				elif "город" in body.lower():
					num_r = random.randrange(1, 100)
					vk.method("messages.send", {"peer_id": id, "random_id": random.randrange(1,30000, 1), "message":'Начали'})

					# Первым делом нужно достать базу данных названия городов.
					# В Интернете я нашел список городов (~1500) и записал в текстовый блокнот под именем city.
					# Создадим функцию getCityList, которая будет возвращать массив с городами из текстового блокнота. 
					city = GameProject.getCityList()

					# из списка выбираем случайный город.
					num_r = random.randrange(1, 500)
					main_city = city[num_r]
					if(main_city == ''):
						main_city = city[num_r + 1]

					# Удаляем этот город из списка, чтобы компьютер не использовал его повторно.
					city.remove(main_city)
					random_city = main_city
					vk.method("messages.send", {"peer_id": id, "random_id": random.randrange(1,30000, 1), "message":random_city})

					while True:
						messages = vk.method("messages.getConversations", {"offset": 0, "count": 20, "filter": "unread"})
						if messages["count"] >= 1: # ход игрока
							body = messages["items"][0]["last_message"]["text"]
							# Делаем проверку на последнюю букву города, который записал пользователь. 
							smech = -1
							# Если это буквы ”ъ”,”ь” или “ы”, то берем букву, стоящую перед последней.
							if(main_city[-1] == 'ь' or main_city[-1] == 'ъ' or main_city[-1] == 'ы'):
								smech = -2

							# Проверяем наличие такого города в списке, если существует – удаляем и отправляем новый город.
							if body.lower().title() in city and body.lower()[0] == main_city[smech]:

								main_city = body.lower()
								i3 = 0
								smech = -1
								city.remove(body.lower().title())

								# проверка на последнюю букву
								# если последняя буква ь, ъ или ы - берем предпоследнюю букву
								if(main_city[-1] == 'ь' or main_city[-1] == 'ъ' or main_city[-1] == 'ы'):
									smech = -2

								# достаем город из списка
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
								# удаляем уже использованный город
								city.remove(main_city)

							elif "выход" in body.lower():
								break
							else:
								print(body.lower())
								vk.method("messages.send", {"peer_id": id, "random_id": random.randrange(1,30000, 1), "message":'Неверно'})
				else:
					text = 'Введите "город", чтобы играть или "выход", чтобы выйти'
					vk.method("messages.send", {"peer_id": id, "random_id": random.randrange(1,30000, 1), "message":text})




# КЛАСС МЕНЮ
class Menu():
	@staticmethod
	def showMenu():
		menu_array = ['Список команд:',
		 			'игра - Игра "Угадай число"',
		   			'города - Игра "Города"',
		   			'тв - узнать телепрограмму на сегодня']
		menu = ''
		for i in menu_array:
			menu = menu + i + '\n' 
		return menu




# КЛАСС ФУНКЦИИ ПОКАЗА TV ПРОГРАММ
class showTVProgrammProject():

	# ОСНОВНОЙ КОД ФУНКЦИИ ПОКАЗА TV ПРОГРАММ
	def getNumTVFromUser(vk, url):
		messages = vk.method("messages.getConversations", {"offset": 0, "count": 20, "filter": "unread"})
		if messages["count"] >= 1:
			id = messages["items"][0]["last_message"]["from_id"]
			body = messages["items"][0]["last_message"]["text"]

			# обращаемся к функции getNamesTVProgramms того же класса.
			# Функция возвращает название всех телепрограмм, html код, а также количество каналов. И входим в цикл. 
			tv_name, html, num_max = showTVProgrammProject.getNamesTVProgramms()

			# выводим инструкцию
			text = 'Введите нужную цифру:\n'+tv_name+'\nВведите "выход", чтобы выйти'
			vk.method("messages.send", {"peer_id": id, "random_id": random.randrange(1,30000, 1), "message":text})
			while True:
				min_num = 1
				messages = vk.method("messages.getConversations", {"offset": 0, "count": 20, "filter": "unread"})
				if messages["count"] >= 1:
					id = messages["items"][0]["last_message"]["from_id"]
					body = messages["items"][0]["last_message"]["text"]

					# Проверяем сообщение на число
					if (body.lower().isdigit()):

						# Проверяем на вход его в диапазон всех телеканалов. 
						if int(body.lower()) <= num_max and int(body.lower()) >= min_num:
							id = messages["items"][0]["last_message"]["from_id"]
							body = messages["items"][0]["last_message"]["text"]

							# Если все в порядке – запоминаем число в переменной num
							num = int(body.lower()) - 1

							# обращаемся к новой функции getTVProgramm, которая принимает три параметра.
							# Функция возвращает и отправляет расписание выбранного телеканала.
							tv = showTVProgrammProject.getTVProgramm(url, num, html)
							vk.method("messages.send", {"peer_id": id, "random_id": random.randrange(1,30000, 1), "message":tv+'\nВведите "выход", чтобы выйти'})
						else:
							text = 'Такого числа нет\nВведите правильное число или "выход", чтобы выйти'
							vk.method("messages.send", {"peer_id": id, "random_id": random.randrange(1,30000, 1), "message":text})
					elif(body.lower() == "выход"):
						break
					else:
						text = 'Введите число или "выход", чтобы выйти'
						vk.method("messages.send", {"peer_id": id, "random_id": random.randrange(1,30000, 1), "message":text})

	# ПОЛУЧИТЬ HTML КОД СТРАНИЦЫ С САЙТА TV ПРОГРАММ
	def getHtmlTVProgramm(url):
		client = requests.session()
		html = client.get(url)
		return html.text

	# ИЗЪЯТИЕ ИЗ HTML КОДА СТРАНИЦЫ РАСПИСАНИЯ ПЕРЕДАЧ
	def getTVProgramm(url, num, html):
		soup = BeautifulSoup(html, 'lxml')
		tv = soup.find_all('div', {'class':'p-channels__item'})[num]
		tv = tv.find('div', {'class':'p-channels__item__info'})
		tv = tv.find('div', {'class':'p-channels__item__info__title'})
		tv = tv.find('a', {'class':'p-channels__item__info__title__link'}).contents[0]
		try:
			tv_block = soup.find_all('div', {'class':'p-channels__item'})[num]
			tv_block = tv_block.find('div', {'class':'p-programms__items'})
			tv_block = tv_block.find_all('div', {'class':'p-programms__item'})
			tv_my_block = ''
			for i in tv_block:
				if(i == ''):
					tv_name = ' '
					tv_time = ' '
				else:
					tv_name = i.find('div', {'class':'p-programms__item__inner'})
					tv_name = tv_name.find('span', {'class':'p-programms__item__name'})
					tv_name = tv_name.find('span', {'class':'p-programms__item__name__link'}).contents[0]

					tv_time = i.find('div', {'class':'p-programms__item__inner'})
					tv_time = tv_time.find('span', {'class':'p-programms__item__name'})
					tv_time = tv_time.find('span', {'class':'p-programms__item__time'})
					tv_time = tv_time.find('span', {'class':'p-programms__item__time__value'}).contents[0]

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
			tv_name = i.find('div', {'class':'p-channels__item__info'})
			tv_name = tv_name.find('div', {'class':'p-channels__item__info__title'})
			tv_name = tv_name.find('a', {'class':'p-channels__item__info__title__link'}).contents[0]

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

			# игра - "Угадай число"
			# Для создания игры “Угадай число” нам потребуется в обработчике сообщений прописать проверку на команду “игра”. 
			# Код я буду писать в отдельном статическом методе guessNumber класса GameProject.
			# Функция guessNumber() принимает два значения – ответ от сервера и число попыток, за которое нужно угадать число (n).
			elif "игра" in body.lower():
				GameProject.guessNumber(vk, 6)
				vk.method("messages.send", {"peer_id": id, "random_id": random.randrange(1,30000, 1), "message":"Вы вышли"})

			# меню
			elif "меню" in body.lower():
				menu = Menu.showMenu()
				vk.method("messages.send", {"peer_id": id, "random_id": random.randrange(1,30000, 1), "message":menu})

			#	Добавляем в обработчик сообщений команду “города”. Обращаемся к методу cityGame класса GameProject, который принимает одно значение – ответ от сервера.
			elif "города" in body.lower():
				GameProject.cityGame(vk)
				vk.method("messages.send", {"peer_id": id, "random_id": random.randrange(1,30000, 1), "message":"Вы вышли"})

			# 	Добавляем в наш главный обработчик команду “тв”. 
			#	В переменную url записываем сайт с которого будем брать телепрограмму. В данном примере я беру информацию с сайта TVMail.  
			#	Обращаемся к методу getNumTVFromUser класса showTVProgrammProject, который принимает два значения – ответ от сервера и url страницы.
			elif "тв" in body.lower(): 
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