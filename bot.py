from telebot import TeleBot
from config import TOKEN
from telebot import types
import random 
from sqlighter import SQlighter
import time
from keyboards import *

bot = TeleBot(TOKEN)


@bot.message_handler(commands = ['start', 'Exit'])
def main(message):

    #Добавляем в БД айди юзера если его нет ранее
    database = SQlighter('sqlite.db')
    database.add_new_user(message.chat.id)

    bot.send_message(message.chat.id, """
Правила нашей игры очень простые: перед Вами появится некоторое количество яблок.
Вы и я будем по очереди съедать 1, 2 или 3 ягоды.
Тот, кто съест последнюю (испорченное) яблоко — проиграл!
Начнём?
""", parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types = ['text'])

def text_messages(message):
    if message.chat.type == 'private':
        if message.text == 'Начать игру':
            msg = bot.send_message(message.chat.id, 'С каким количеством яблок будем играть?\nВведите число от 20 до 100:', reply_markup=types.ReplyKeyboardRemove())
            bot.register_next_step_handler(msg, process_link_step)
        
        elif message.text == 'Создатель':
            bot.send_message(message.chat.id, 'Меня создал @Xeonio\nEсли будут проблемы пиши ему он по фиксит меня)')

        elif message.text == '🍎':
            process_game(message.chat.id, 1)

        elif message.text == '🍎🍎':
            process_game(message.chat.id, 2)
            
        elif message.text == '🍎🍎🍎':
            process_game(message.chat.id, 3)


        elif message.text == 'Моя статистика':
            database = SQlighter('sqlite.db')
            chat_id = message.chat.id

            wins = database.get_column(chat_id, 'wins')
            defeats = database.get_column(chat_id, 'defeats')
            giveups = database.get_column(chat_id, 'giveups')

            msg = f"Побед: {str(wins)}\nПоражений: {str(defeats)}\nВы сдались: {str(giveups)}"

            bot.send_message(message.chat.id, msg)

        elif message.text == 'Сдаться':
            database = SQlighter('sqlite.db')
            current_giveups = database.get_column(message.chat.id, 'giveups')
            database.update_column(message.chat.id, current_giveups + 1, 'giveups')
            bot.send_message(message.chat.id, 'Вы сдались:(\nНо почему бы не попробовать еще раз?', parse_mode='html', reply_markup=markup)
        
        elif message.text == 'Правила':
            bot.send_message(message.chat.id, """
Правила игры

— В самом начале игры я предложу Вам выбрать количество яблок, которое появится перед нами.
— Затем мы по очереди будем съедать 1, 2 или 3 яблок на выбор.
— Проигрывает тот, кто съест последнюю (испорченное) яблоко.

Сыграем?
""")
        else:
            bot.send_message(message.chat.id, 'Вы явно ошиблись при вводе...')

def process_link_step(message):
    try:
        chat_id = message.chat.id
        number = message.text

        database = SQlighter('sqlite.db')
        database.update_column(chat_id, int(number), 'apples')

        if int(number) < 20 or int(number) > 100:
            bot.send_message(chat_id, """
Вы ошиблись! Вам нужно было ввести число от 20 до 100. 
Попробуйте ещё раз нажав кнопку играть или для отмены нажмите /Exit
""")
        else:
            quantity = database.get_column(chat_id, 'apples')
            apples = '🍎' * quantity
            message = f'Итак, перед Вами {number} яблок: \n\n{apples} \n\nСъешьте 3, 2 или 1. Ваш ход:'

            bot.send_message(chat_id, message, parse_mode='html', reply_markup=apple_markup)    


    except Exception as e:
        bot.reply_to(message, """
Вы ошиблись! Вам нужно было ввести число от 20 до 100. 
Попробуйте ещё раз нажав кнопку играть или для отмены нажмите /Exit
""")

def process_game(chat_id, quantity_apple):
    database = SQlighter('sqlite.db')
    quantity = database.get_column(chat_id, 'apples')


    #Проверяем на победителя
    if quantity == 1 or 0:
        
        current_wins = database.get_column(chat_id, 'defeats')
        database.update_column(chat_id, current_wins + 1, 'defeats')

        bot.send_message(chat_id, 'Вы проиграли!\n\nПобеда за мной!(\nХотите отыграться?', reply_markup=markup, parse_mode='html')

    else:
        database.update_column(chat_id, quantity - quantity_apple, 'apples')
        quantity_after = database.get_column(chat_id, 'apples')
        apples = '🍎' * quantity_after

        msg = f"Отлично! Вы съели {str(quantity_apple)} яблоко.\nОставшиеся:\n\n{apples}\n\nТеперь мой ход!"
        bot.send_message(chat_id, msg, reply_markup=types.ReplyKeyboardRemove())

        time.sleep(0.5)

        if quantity_after == 1:
            current_wins = database.get_column(chat_id, 'wins')
            database.update_column(chat_id, current_wins + 1, 'wins')

            bot.send_message(chat_id, 'Вы выйграли!\n\nПобеда за вами!)\nХотите еще раз?', reply_markup=markup, parse_mode='html')

        else:
            if quantity_after == 0:
                
                current_wins = database.get_column(chat_id, 'defeats')
                database.update_column(chat_id, current_wins + 1, 'defeats')

                bot.send_message(chat_id, 'Вы проиграли!\n\nПобеда за мной!(\nХотите отыграться?', reply_markup=markup, parse_mode='html')
                
            else:
                random_int = random.randint(1,3)
                summ = quantity_after - random_int

                if summ > 0:
                    database.update_column(chat_id, summ, 'apples')
                    bot_quantity_after = database.get_column(chat_id, 'apples')
                    bot_apples = '🍎' * bot_quantity_after
                    
                    bot_msg = f'Я съедаю {random_int} яблок(о).\nОставшиеся:\n\n{bot_apples}\n\nТеперь Ваш ход!\nЕшьте яблоко:'
                    bot.send_message(chat_id, bot_msg, parse_mode='html', reply_markup=apple_markup)
                else:
                    current_wins = database.get_column(chat_id, 'wins')
                    database.update_column(chat_id, current_wins + 1, 'wins')

                    bot.send_message(chat_id, f'Я проиграл съев {random_int} яблок(о)\n\nПобеда за вами!)\nХотите еще раз?', reply_markup=markup, parse_mode='html')

if __name__ == '__main__':
    bot.polling(none_stop = True)