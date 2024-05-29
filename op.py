import telebot
from telebot import types
import requests
import json

bot = telebot.TeleBot('7002296370:AAF81Z6z7ixQEMfniY5MHIHU3zXWb6DrRyg')
ti = set()

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if str(user_id) in ti:
        bot.send_message(chat_id=message.chat.id, text='مرحبا، يمكنك استخدام البوت.')
    else:
        bot.send_message(chat_id=message.chat.id, text='لا يمكنك استخدام البوت.')

@bot.message_handler(func=lambda message: message.chat.id == 5813081202)
def admin(message):
    global ti
    if 'تفعيل' in message.text:
        ud = message.text.replace('تفعيل:', '').strip()
        if ud in ti:
            bot.reply_to(message, 'تم تفعيله من قبل.')
        else:
            ti.add(ud)
            bot.send_message(chat_id=message.chat.id, text='تم تفعيل المستخدم.')
    elif 'حذف' in message.text:
        xd = message.text.replace('حذف:', '').strip()
        if xd in ti:
            ti.remove(xd)
            bot.reply_to(message, 'تم حذف المستخدم.')
        else:
            bot.reply_to(message, 'المستخدم غير موجود في القائمة.')
    else:
        pass

@bot.message_handler(func=lambda message: str(message.from_user.id) in ti)
def zik(message):
    global aa
    aa = message.text
    try:
        if '05' in aa:
            data = {
                'client_id': 'ibiza-app',
                'grant_type': 'password',
                'mobile-number': aa,
                'language': 'EN'
            }
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            ress = requests.post('https://ibiza.ooredoo.dz/auth/realms/ibiza/protocol/openid-connect/token', data=data, headers=headers).text
            if 'ROOGY' in ress:
                msg = bot.reply_to(message, 'تم ارسال الرمز')
                bot.register_next_step_handler(msg, otp_c)
            else:
                bot.reply_to(message, 'فشل ارسال الرمز')
    except Exception as e:
        bot.reply_to(message, f'حدث خطأ: {str(e)}')

def otp_c(call):
    global token, aa
    me = call.text
    try:
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data2 = {
            'client_id': 'ibiza-app',
            'otp': me,
            'grant_type': 'password',
            'mobile-number': aa,
            'language': 'EN'
        }
        res2 = requests.post('https://ibiza.ooredoo.dz/auth/realms/ibiza/protocol/openid-connect/token', data=data2, headers=headers).json()
        token = res2.get('access_token')
        
        if token:
            bot.send_message(chat_id=call.chat.id, text='انتظر...')
            headers = {
                "Authorization": f"Bearer {token}",
                "language": "EN",
                "request-id": "14a32040-b8e8-4831-a255-8a7dce786dca",
                "flavour-type": "gms",
                "Content-Type": "application/json; charset=utf-8",
                "Content-Length": "50",
                "Host": "ibiza.ooredoo.dz",
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip",
                "User-Agent": "okhttp/4.9.3"
            }
            balance_response = requests.get('https://ibiza.ooredoo.dz/api/v1/mobile-bff/users/balance', headers=headers).json()
            value = balance_response['accounts'][1]['value']
            
            jo = types.InlineKeyboardButton(text='تعبئة', callback_data='ta')
            jam = types.InlineKeyboardMarkup(row_width=1)
            jam.add(jo)
            bot.send_message(chat_id=call.chat.id, text=f'رصيدك الحالي: {value}. هل تريد التعبئة؟', reply_markup=jam)
        else:
            bot.reply_to(call, 'عملية فاشلة. لم يتم الحصول على الرمز.')
    except Exception as e:
        bot.reply_to(call, f'رمز ايرور: {str(e)}')

@bot.callback_query_handler(func=lambda call: call.data == 'ta')
def handle_callback(call):
    global token
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "language": "EN",
            "request-id": "14a32040-b8e8-4831-a255-8a7dce786dca",
            "flavour-type": "gms",
            "Content-Type": "application/json; charset=utf-8",
            "Content-Length": "50",
            "Host": "ibiza.ooredoo.dz",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/4.9.3"
        }
        json_data = {"mgmValue": "ABC"}
        
        for _ in range(4):
            response = requests.post('https://ibiza.ooredoo.dz/api/v1/mobile-bff/users/mgm/info/apply', headers=headers, json=json_data).text
        
        balance_response = requests.get('https://ibiza.ooredoo.dz/api/v1/mobile-bff/users/balance', headers=headers).json()
        value = balance_response['accounts'][1]['value']
        bot.reply_to(call.message, f'رصيدك الان هو: {value}')
    except Exception as e:
        bot.reply_to(call.message, f'عملية فاشلة: {str(e)}')

bot.infinity_polling(none_stop=True)
