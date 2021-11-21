import telebot
from telebot import time
import sqlite3
import time

bot = telebot.TeleBot("2077947303:AAF-9cMGFbWwjr-CEts2g2xPk9XLREb4b5s")

conn = sqlite3.connect('/home/arkady/Рабочий стол/taxdb', check_same_thread=False,timeout=7)
cursor = conn.cursor()

def is_number(s):
	try:
		float(s)
		return True
	except ValueError:
		return False

@bot.message_handler(commands=['create_party'])
def name_party(message):
	global keyboard
	bot.send_message(message.chat.id, 'Сейчас в чате должно быть написано только название вечеринки!')
	time.sleep(1.5)
	msg=bot.send_message(message.chat.id, 'Введите название вечеринки')
	bot.register_next_step_handler(msg,indb)

def indb(message):
	global al
	al=message.text
	sql1="INSERT INTO Party(Name) Values ('{}')".format(al)
	cursor.execute(sql1)
	result1 = cursor.fetchall()
	conn.commit()
	bot.send_message(message.chat.id, 'Создана пати {}'.format(al))
	time.sleep(1)
	msg1=bot.send_message(message.chat.id, 'Теперь введите участников пати через запятую. Например: @lol, @lol1,@lol2')
	bot.register_next_step_handler(msg1,indb1)

def indb1(message):
	al1=message.text
	sql2="UPDATE Party SET tags='{}' WHERE Name='{}'".format(al1,al)
	cursor.execute(sql2)
	result1 = cursor.fetchall()
	conn.commit()
	time.sleep(1)
	bot.send_message(message.chat.id, 'Участники пати добавлены. Теперь перейдите в @BankirTax_bot и совершите вкид на общак')

@bot.message_handler(commands=['list'])
def name_party(message):
        sql3="SELECT * FROM Tebe"
        cursor.execute(sql3)
        res = cursor.fetchall()
        conn.commit()
        bot.send_message(message.chat.id, "Им должны денег  '{}'".format(res))

        sql2="SELECT * FROM Tebe"
        cursor.execute(sql2)
        res1 = cursor.fetchall()
        conn.commit()
        bot.send_message(message.chat.id, "Они должны денег '{}'".format(res1))


bot.polling()
