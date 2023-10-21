import telebot
from telebot import custom_filters
from telebot import StateMemoryStorage
from telebot.handler_backends import StatesGroup, State

state_storage = StateMemoryStorage()
# Вставить свой токет или оставить как есть, тогда мы создадим его сами
bot = telebot.TeleBot("6414309276:AAFy7C0Iaf_RjccKnfq_4th088AheEM_OAk",
                      state_storage=state_storage, parse_mode='Markdown')


class PollState(StatesGroup):
    name = State()
    age = State()

nameUser = ""
ageUser = 0
class HelpState(StatesGroup):
    wait_text = State()


text_poll = "Регистрация пользователя"  # Можно менять текст
text_button_1 = "Выведи мои данные"  # Можно менять текст
text_button_2 = "Чей это шаблон?)"  # Можно менять текст
text_button_3 = "Скажи мне пока"  # Можно менять текст

menu_keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_poll,
    )
)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_1,
    )
)

menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_2,
    ),
    telebot.types.KeyboardButton(
        text_button_3,
    )
)


@bot.message_handler(state="*", commands=['start'])
def start_ex(message):
    bot.send_message(
        message.chat.id,
        'Привет!Мои возможности представлены ниже',  # Можно менять текст
        reply_markup=menu_keyboard)


@bot.message_handler(func=lambda message: text_poll == message.text)
def first(message):
    bot.send_message(message.chat.id, 'Супер! *Ваше* _имя_?')  # Можно менять текст
    bot.set_state(message.from_user.id, PollState.name, message.chat.id)

@bot.message_handler(state=PollState.name)
def name(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text
    global nameUser
    nameUser = message.text
    bot.send_message(message.chat.id, 'Супер! [Ваш](https://www.example.com/) `возраст?`')  # Можно менять текст
    bot.set_state(message.from_user.id, PollState.age, message.chat.id)


@bot.message_handler(state=PollState.age)
def age(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['age'] = message.text

    global ageUser
    ageUser = int(message.text)
    bot.send_message(message.chat.id, 'Спасибо за регистрацию!\nВаши данные сохранены', reply_markup=menu_keyboard)  # Можно менять текст
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(func=lambda message: text_button_1 == message.text)
def help_command(message):

    if(nameUser!="" and ageUser!=0):
        bot.send_message(message.chat.id, f"Ваше имя - {nameUser}\nВаш возраст - {ageUser}", reply_markup=menu_keyboard)  # Можно менять текст
    else:
        bot.send_message(message.chat.id,f"А сначала надо зарегестироваться!",reply_markup=menu_keyboard)

@bot.message_handler(func=lambda message: text_button_2 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "Этот шаблон нам дали [Умскул](https://umschool.net/)", reply_markup=menu_keyboard)  # Можно менять текст


@bot.message_handler(func=lambda message: text_button_3 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "[Ну пока](https://i.gifer.com/embedded/download/MZUg.gif)", reply_markup=menu_keyboard)  # Можно менять текст


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.TextMatchFilter())

bot.infinity_polling()