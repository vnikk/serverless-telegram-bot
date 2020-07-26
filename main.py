import os
import requests
import datetime
import telegram
import sys, traceback

bot = telegram.Bot(token=os.environ["TELEGRAM_TOKEN"])


def basketbot(request):
    days = ['пн', 'вт', "ср", "чт", "пт", "сб", "вс"]
    try:
        if request.method != "POST":
            return "ok"
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        if update.channel_post:
            print('Channel post')
            msg = update.channel_post
        elif update.message:
            print('Regular message')
            msg = update.message
        else:
            print('Unrecognized type:', update)
        print('Chat id: ', msg.chat.id)
        if msg.chat.id not in map(int, os.environ['TELEGRAM_IDS'].split()):
            reason = 'Wrong caller!'
            print(reason)
            raise RuntimeError(reason)
        text = msg.text
        if '/weather' in text:
            if len(text.split()) == 1:
                reply = 'команда: /weather@{} пн|вт|ср|чт|пт|сб|вс'.format(os.environ['TELEGRAM_BOT_NAME'])
            else:
                arg = text.split()[1].lower()
                requested_day = days.index(arg)
                weather_resp = requests.get('https://api.openweathermap.org/data/2.5/forecast?q=Prague&appid={}&lang=ru&units=metric'.format(os.environ['OPENWEATHER_TOKEN'])).json()
                reply = days[requested_day] + ':\n'
                for el in weather_resp['list']:
                    timestamp = datetime.datetime.fromtimestamp(el['dt'])
                    if timestamp.weekday() == requested_day and timestamp.hour > 11 and timestamp.hour < 21:
                        reply += el['dt_txt'] + '\n'
                        reply += str(el['weather']) + '\n'
            bot.sendMessage(chat_id=msg.chat.id, text=reply)
        else:
            print('unknown command')
    except AttributeError as e:
        traceback.print_exc(file=sys.stdout)
        print(e)
        print(update)
        print(update.to_dict())
        print(dir(update))
        raise
    except Exception as e:
        print(e)
        print(update)
        print(update.to_dict())
        raise
    return "ok"
