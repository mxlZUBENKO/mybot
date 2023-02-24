from datetime import date
from emoji import emojize
import ephem
from glob import glob
import logging
from random import randint, choice
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import settings

logging.basicConfig(filename='bot.log', level=logging.INFO)

def greet_user(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    smile = context.user_data['emoji']
    update.message.reply_text(f'Здравствуй пользователь! {smile}')

def talk_to_me(update, context):
    text = update.message.text
    context.user_data['emoji'] = get_smile(context.user_data)
    smile = context.user_data['emoji']
    update.message.reply_text(f"{text} {smile}")

def get_smile(user_data):
    if 'emoji' not in user_data:
        smile = choice(settings.USER_EMOJI)
        return emojize(smile, use_aliases=True)
    return user_data['emoji']


def planetary_constellation(update, context):
    current_date = date.today()
    planet_name = update.message.text.split()[-1].capitalize()
    planet = getattr(ephem, planet_name)(current_date)
    constellation = ephem.constellation(planet)
    update.message.reply_text(f'Планета {planet_name} находиться в созвездии: {constellation[-1]}')

def play_random_numbers(user_number):
    bot_number = randint(user_number-10, user_number+10)
    if user_number > bot_number:
        message = f"Ваше число {user_number}, моё {bot_number}, вы выиграли"
    elif user_number == bot_number:
        message = f"Ваше число {user_number}, моё {bot_number}, ничья"
    else:
        message = f"Ваше число {user_number}, моё {bot_number}, вы проиграли"
    return message

def guess_number(update, context):
    if context.args:
        try:
            user_number = int(context.args[0])
            message = play_random_numbers(user_number)
        except (TypeError, ValueError):
            message = "Введите целое число"
    else:
        message = "Введите число"
    update.message.reply_text(message)

def send_cat_picture(update, context):
    cat_photo_list = glob('images/cat*.jp*g')
    cat_photo_filename = choice(cat_photo_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(cat_photo_filename, 'rb'))

def main():
    mybot = Updater(settings.API_KEY, use_context=True)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("planet", planetary_constellation))
    dp.add_handler(CommandHandler("guess", guess_number))
    dp.add_handler(CommandHandler("cat", send_cat_picture))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info('bot started')
    mybot.start_polling()
    mybot.idle()

if __name__ == '__main__':
    main()