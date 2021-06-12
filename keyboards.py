from telebot import types

# Main Keyboard
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
item1 = types.KeyboardButton("Начать игру")
item2 = types.KeyboardButton("Правила")
item3 = types.KeyboardButton("Моя статистика")
item4 = types.KeyboardButton("Создатель")

markup.add(item1, item2, item3, item4)

# Apple Keyboard
apple_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
item1 = types.KeyboardButton("🍎")
item2 = types.KeyboardButton("🍎🍎")
item3 = types.KeyboardButton("🍎🍎🍎")
item4 = types.KeyboardButton("Сдаться")

apple_markup.add(item1, item2, item3, item4)