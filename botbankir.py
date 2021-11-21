import telebot
from telebot import time
import sqlite3
import time
import math

bot = telebot.TeleBot("2115057659:AAFa1zmH5Nhh2lUjJ7EQNC1J1KPU0dWzBwo")

conn = sqlite3.connect('/home/arkady/Рабочий стол/taxdb', check_same_thread=False,timeout=7)
cursor = conn.cursor()

def is_number(s):
        try:
                float(s)
                return True
        except ValueError:
                return False

@bot.message_handler(commands=['yaoplatil'])
def name_party(message):
	msg=bot.send_message(message.chat.id, 'Введите название вечеринки, на которой вы зареганы')
	bot.register_next_step_handler(msg,indb)

def indb(message):
	global name
	name=message.text
	sql3="SELECT Name FROM Party WHERE Name='{}' ".format(name)
	cursor.execute(sql3)
	result2 = cursor.fetchall()
	conn.commit()
	if (result2[0][0]!=None):
		if result2[0][0]==name:
			msg4=bot.send_message(message.chat.id, 'Введите ваш тег. Например, @lol')
			bot.register_next_step_handler(msg4,indb1)
		else:
			bot.send_message(message.chat.id, 'Чёт не то')

def indb1(message):
	global tag
	tag=message.text
	sql4="SELECT tags FROM Party WHERE Name='{}'".format(name)
	cursor.execute(sql4)
	result3 = cursor.fetchall()
	conn.commit()
	#bot.send_message(message.chat.id, str(tag) in str(result3[0][0]))
	if result3[0][0]!=None:
		if str(tag) in str(result3[0][0]):
			msg4=bot.send_message(message.chat.id, 'Введите сумму, которую вы скинули')
			bot.register_next_step_handler(msg4,indb2)
			'''kek="INSERT INTO V(id) Values ('{}')".format(tag)
			cursor.execute(kek)
			res = cursor.fetchall()
			conn.commit()'''

def indb2(message):
	sum=message.text
	kek="INSERT INTO V VALUES ('{}','{}',{})".format(name,tag,int(sum))
	#kek="INSERT INTO V(id) Values ('{}') WHERE id='{}'".format(int(sum),tag)
	cursor.execute(kek)
	res = cursor.fetchall()
	conn.commit()
	bot.send_message(message.chat.id, 'Успех!')

@bot.message_handler(commands=['mmm'])
def mmm1(message):
	msge=bot.send_message(message.chat.id, 'Введите название вечеринки, чтобы посмотреть кто кому должен и кому должны)')
	bot.register_next_step_handler(msge,indbe)


def indbe(message):
	party=message.text
	cursor.execute("SELECT * FROM V WHERE name_party='{}'".format(party))
	result2 = cursor.fetchall()
	conn.commit()
	n=0

	for i in range(len(result2)):
        	n+=result2[i][2]

	cursor.execute("SELECT * FROM Party WHERE Name='{}'".format(party))
	result3 = cursor.fetchall()
	conn.commit()
	k=len(result3[0][1].split(','))

	c=math.ceil(n/k)

	V=len(result2)
	D=k-V

	K=result3[0][1].split(',') #все in party
	print(K)

	vkinul=[]

	for i in range(len(result2)):
        	vkinul.append(result2[i][1])

	print(list(set(K) - set(vkinul))) #ничего не вкинули

	for i in range(len(result2)):
        	#TEBE
        	if result2[i][2]>c:
                	m=int(result2[i][2])-int(c)
                	cursor.execute("INSERT INTO Tebe VALUES('{}','{}')".format(result2[i][1],m))
                	resultet = cursor.fetchall()
                	conn.commit()
        	elif result2[i][2]<c:
                	m1=int(int(c)-result2[i][2])
                	cursor.execute("INSERT INTO Dolg VALUES('{}','{}')".format(result2[i][1],m1))
                	resultet1 = cursor.fetchall()
                	conn.commit()

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
