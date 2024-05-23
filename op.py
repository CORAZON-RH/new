import telebot
import types
bot = telebot.TeleBot('6544968719:AAGld_xCgjA0uOEq7BxFpDYNqNMlqYFaxlM')
ti = set()
@bot.message_handler(commands=['start'])
def start(message):
	id = message.from_user.id
	if str(id) in ti:
		bot.send_message(chat_id=message.chat.id,text='نرحبا يمكنك استخدام لبوت')
	else:
		bot.send_message(chat_id=message.chat.id,text='لا يمكنك استخدام لبوت')
@bot.message_handler(func=lambda message:message.chat.id ==5813081202)
def admin(message):
     global id
     if 'تفعيل' in message.text:
        ud=message.text.replace('تفعيل:','')
        if ud in ti:
        	bot.reply_to(message,'تم تفعيله من قبل')
        else:
        	ti.add(ud)
        	bot.send_message(chat_id='5813081202',text='تم تفعيل')
     elif 'حذف'in message.text:
        xd=message.text.replace('حذف:','')
     else:
       pass


bot.infinity_polling(none_stop=True)       
        	
        
