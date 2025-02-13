import telebot
import users
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime, timedelta
from telebot.types import BotCommand

# Инициализация бота
bot = telebot.TeleBot('8080525686:AAE0Ye8eY6pMb4OIHnsN8Pr2YsdWfdQdp4k')

# Класс для хранения данных пользователя
class User:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.language = "ru"
        self.current_appointment = None

    def set_language(self, language):
        self.language = language

    def get_language(self):
        return self.language

    def set_appointment(self, appointment):
        self.current_appointment = appointment

    def get_appointment(self):
        return self.current_appointment

    def cancel_appointment(self):
        self.current_appointment = None


# Класс для хранения данных о записи
class Appointment:
    def __init__(self, service, master, date, time):
        self.service = service
        self.master = master
        self.date = date
        self.time = time

    def __str__(self):
        return f"Service: {self.service}, Master: {self.master}, Date: {self.date}, Time: {self.time}"

# Класс для хранения данных об услуге
class Service:
    def __init__(self, name, price):
        self.name = name
        self.price = price

# Класс для хранения данных о мастере
class Master:
    def __init__(self, name, services):
        self.name = name
        self.services = services


bot.set_my_commands([

    BotCommand("start", "Перезапустить бота"),
    BotCommand("settings", "Настройки"),
    BotCommand("main_menu", "Главное меню")
])

# Глобальные переменные
LANGUAGES = {
    "Русский": "ru",
    "English": "eng",
    "Қазақ тілі": "kz"
}

# Глобальный словарь для хранения пользователей
user_language = {}
user_data={ }
APPOINTMENTS = {}
users = {}

SERVICES = {
    "ru": "Маникюр (гель покрытие) - 7000 тенге \n"
          "Маникюр (наращивание) - 13000 тенге \n"
          "Педикюр - 9000 тенге \n"
          "Ламинирование ресниц - 8000 тенге \n"
          "Наращивание ресниц - 11000 тенге \n"
          "Ламинирование бровей - 7000 тенге \n"
          "Стрижка - 7000 тенге",

    "eng": "Manicure (gel polish) - 7000 tenge \n"
           "Manicure (extensions) - 13000 tenge \n"
           "Pedicure - 9000 tenge \n"
           "Eyelash lamination - 8000 tenge \n"
           "Eyelash extensions - 11000 tenge \n"
           "Eyebrow lamination - 7000 tenge \n"
           "Haircut - 7000 tenge",

    "kz": "Маникюр (гель жабыны) - 7000 теңге \n"
          "Маникюр (кеңейту) - 13000 теңге \n"
          "Педикюр - 9000 теңге \n"
          "Кірпік ламинациясы - 8000 теңге \n"
          "Кірпік ұзарту - 11000 теңге \n"
          "Қас ламинациясы - 7000 теңге \n"
          "Шаш қию - 7000 теңге"
}


MASTERS = {
    "ru": { "Маникюр (гель покрытие)": ["Аружан", "Сания", "Айымжан"],
    "Маникюр (наращивание)": ["Маржан", "Еркежан" , "Назерке"],
    "Педикюр": ["Асылжан", "Мадина"],
    "Ламинирование ресниц": ["Алина", "Айша", "София"],
    "Наращивание ресниц": ["Алина", "Полина", "Айымжан"],
    "Ламинирование бровей": ["Галина", "Марина"],
    "Стрижка": ["Виталий", "Адема","Анна"]
          },
    "eng": {
        "Manicure (gel polish)": ["Aruzhan", "Saniya", "Aymyzhan"],
        "Manicure (extensions)": ["Marzhan", "Erkezhan", "Nazerke"],
        "Pedicure": ["Asylzhan", "Madina"],
        "Eyelash lamination": ["Alina", "Aisha", "Sofia"],
        "Eyelash extensions": ["Alina", "Polina", "Aymyzhan"],
        "Eyebrow lamination": ["Galina", "Marina"],
        "Haircut": ["Vitaliy", "Adema", "Anna"]
    },
    "kz": {
        "Маникюр (гель жабыны)": ["Аружан", "Сания", "Айымжан"],
        "Маникюр (кеңейту)": ["Маржан", "Еркежан", "Назерке"],
        "Педикюр": ["Асылжан", "Мадина"],
        "Кірпік ламинациясы": ["Алина", "Айша", "София"],
        "Кірпік ұзарту": ["Алина", "Полина", "Айымжан"],
        "Қас ламинациясы": ["Галина", "Марина"],
        "Шаш қию": ["Виталий", "Адема", "Анна"]
    }
}


# Команда /start
@bot.message_handler(commands=["start"])
def start(message):
    user = User(message.chat.id)
    users[message.chat.id] = user

    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for lang in LANGUAGES.keys():
        markup.add(KeyboardButton(lang))

    bot.send_message(
        message.chat.id,
        "Выберите язык / Choose a language / Тілді таңдаңыз :",
        reply_markup=markup
    )

# Обработка выбора языка

@bot.message_handler(func=lambda message: message.text in LANGUAGES.keys())
def set_language(message):
    user = users[message.chat.id]
    user.set_language(LANGUAGES[message.text])
    lang = user.get_language()

    messages = {
        "ru": ("Отлично! Вы выбрали Русский.\n",
               "Вы готовы засиять? ✨ Запишитесь к нам и почувствуйте себя королевой 👑"),
        "eng": ("Great! You chose English.\n",
                "Are you ready to shine? ✨ Book an appointment and feel like a queen 👑"),
        "kz": (
        "Жақсы! Сіз қазақ тілін таңдадыңыз.\n",
        "Жарқырауға дайынсыз ба? ✨ Бізге жазылыңыз және ханшайымдай сезініңіз 👑")
    }

    bot.send_message(message.chat.id, messages[lang][0])
    bot.send_message(message.chat.id, messages[lang][1])
    show_main_menu(message.chat.id, lang)

# Показать главное меню
def show_main_menu(chat_id, lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = {
        "ru": ["Просмотр услуг",
               "Запись на услугу",
               "Отмена записи",
               "Мои записи"
               ],
        "eng": ["View services",
                "Book an appointment",
                "Cancel booking",
                "My bookings"
                ],
        "kz": ["Қызметтерді қарау",
               "Қызметке жазылу",
               "Жазылымды болдырмау",
               "Менің жазылымдарым"
               ]
    }

    for btn_text in buttons[lang]:
        markup.add(KeyboardButton(btn_text))

    messages = {
        "ru": "Выберите действие:",
        "eng": "Choose an action:",
        "kz": "Әрекетті таңдаңыз:"
    }

    bot.send_message(chat_id, messages[lang], reply_markup=markup)



# Показать услуги
@bot.message_handler(func=lambda message: message.text in ["Просмотр услуг",
                                                           "View services",
                                                           "Қызметтерді қарау"])
def show_services(message):
    user = users[message.chat.id]
    lang = user.get_language()
    bot.send_message(message.chat.id, SERVICES[lang])

# Запрос на запись
@bot.message_handler(
    func=lambda message: message.text in ["Запись на услугу",
                                          "Book an appointment",
                                          "Қызметке жазылу"])
def request_appointment(message):
    user = users[message.chat.id]
    lang = user.get_language()
    messages = {
        "ru": "Выберите услугу:",
        "eng": "Select a service:",
        "kz": "Қызметті таңдаңыз:"
    }
    services = {
        "ru": [
            "Маникюр (гель покрытие)", "Маникюр (наращивание)", "Педикюр",
            "Стрижка", "Ламинирование ресниц", "Наращивание ресниц", "Ламинирование бровей"
        ],
        "eng": [
            "Manicure (gel coating)", "Manicure (extensions)", "Pedicure",
            "Haircut", "Eyelash lamination", "Eyelash extensions", "Eyebrow lamination"
        ],
        "kz": [
            "Маникюр (гель жабыны)", "Маникюр (кеңейту)", "Педикюр",
            "Шаш қию", "Кірпік ламинациясы", "Кірпік ұзарту", "Қас ламинациясы"
        ]
    }

    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
    buttons = [KeyboardButton(service) for service in services[lang]]
    markup.add(*buttons)
    bot.send_message(message.chat.id, messages[lang], reply_markup = markup)
    bot.register_next_step_handler(message,process_service_selection)

# Обработка выбора услуги
@bot.message_handler(
    func=lambda message: message.text in [item for sublist in SERVICES.values() if isinstance(sublist, list) for item in
                                          sublist])
def process_service_selection(message):
    user = users[message.chat.id]
    lang = user.get_language()
    selected_service = message.text.strip()

    response_messages = {
        "ru": f"Вы выбрали: {selected_service}. Теперь выберите мастера.",
        "eng": f"You selected: {selected_service}. Now choose a master.",
        "kz": f"Сіз таңдадыңыз: {selected_service}. Енді шеберді таңдаңыз."
    }

    bot.send_message(message.chat.id, response_messages[lang])
    choose_master(message, selected_service)

# Выбор мастера
def choose_master(message, service):
    user = users[message.chat.id]
    lang = user.get_language()

    normalized_services={s.lower().strip():s for s in MASTERS[lang]}
    service_key = normalized_services.get(service.lower().strip())

    if service_key:
        masters = MASTERS[lang][service_key]

        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        for master in masters:
            markup.add(KeyboardButton(master))

        bot.send_message(user.chat_id, "Выберите мастера:" if lang == "ru" else
                                   "Choose a master:" if lang == "eng" else
                                   "Маман таңдаңыз:", reply_markup=markup)

        bot.register_next_step_handler(message, choose_date, service_key)

    else:
        bot.send_message(user.chat_id, "Услуга не найдена. Пожалуйста, выберите услугу из списка."
        if lang == "ru"
        else
        "Service not found. Please choose from the list."
        if lang == "eng"
        else
        "Қызмет табылмады. Тізімнен таңдаңыз.")
        show_services(message)

# Выбор даты
def choose_date(message, service):
    user = users[message.chat.id]
    lang = user.get_language()
    master = message.text

    user_data = {"service": service, "master": master}
    user.set_appointment(user_data)

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    dates = [datetime.now() + timedelta(days=i) for i in range(1, 8)]


    messages = {
        "ru": "Выберите дату:",
        "eng": "Choose a date:",
        "kz": "Күнді таңдаңыз:"
    }
    for date in dates:
        markup.add(KeyboardButton(date.strftime("%Y-%m-%d")))

    bot.send_message(user.chat_id, messages[lang], reply_markup=markup)
    bot.register_next_step_handler(message, choose_time)

# Выбор времени
def choose_time(message):
    user = users[message.chat.id]
    lang = user.get_language()
    date = message.text

    user_data = user.get_appointment()
    user_data["date"] = date
    user.set_appointment(user_data)

    messages = {
        "ru": "Выберите время:",
        "eng": "Choose a time:",
        "kz": "Уақытты таңдаңыз:"
    }

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    times = ["10:00", "12:00", "14:00", "16:00", "18:00"]
    for time in times:
        markup.add(KeyboardButton(time))

    bot.send_message(user.chat_id, messages[lang], reply_markup=markup)
    bot.register_next_step_handler(message, confirm_booking)

# Подтверждение записи
def confirm_booking(message):
    user = users[message.chat.id]
    lang = user.get_language()
    time = message.text

    user_data = user.get_appointment()
    user_data["time"] = time

    service = user_data["service"]
    master = user_data["master"]
    date = user_data["date"]


    confirmation_message = {
        "ru": f"Вы записаны на {service} к мастеру {master} на {date} в {time}. Подтвердите запись:",
        "eng": f"You are booked for {service} with {master} on {date} at {time}. Confirm booking:",
        "kz": f"Сіз {service} қызметіне {master} маманына {date} күні {time} уақытына жазылдыңыз. Жазылуды растаңыз:"
    }

    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    confirm = {
        "ru": ["Да","Нет"],
        "eng": ["Yes","No"],
        "kz": ["ИӘ", "Жоқ"]
    }

    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton(confirm[lang][0]), KeyboardButton(confirm[lang][1]))

    bot.send_message(user.chat_id, confirmation_message[lang], reply_markup=markup)
    bot.register_next_step_handler(message, finalize_booking)

# Завершение записи
def finalize_booking(message):
    user = users[message.chat.id]
    lang = user.get_language()
    response = message.text


    responses = {
        "ru": {
            "confirm": "✅ Ваша запись подтверждена!\n📍 Ждем вас по адресу: г. Астана, ул. Мангилик Ел 1/2.\n🎉 До скорой встречи!",
            "cancel": "Ваша запись отменена.До свидания!"
        },
        "eng": {
            "confirm": "✅ Your booking is confirmed!\n📍 We are waiting for you at: Astana, Mangilik El 1/2.\n🎉 See you soon!",
            "cancel": "Your booking has been canceled. Good bye!"
        },
        "kz": {
            "confirm": "✅ Сіздің жазылуыңыз расталды!\n📍 Біз сізді мына мекенжайда күтеміз: Астана қ., Мәңгілік Ел 1/2.\n🎉 Жақында кездесеміз!",
            "cancel": "Сіздің жазылымыңыз жойылды.Сау болыңыз!"
        }
    }

    if response == "Да" or response == "Yes" or response == "ИӘ":
        appointment = Appointment(
            user.get_appointment()["service"],
            user.get_appointment()["master"],
            user.get_appointment()["date"],
            user.get_appointment()["time"]
        )
        user.set_appointment(appointment)
        bot.send_message(user.chat_id, responses[lang]["confirm"])
    else:
        bot.send_message(user.chat_id, responses[lang]["cancel"])

    show_main_menu(user.chat_id, lang)

# Отмена записи
@bot.message_handler(func=lambda message: message.text in ["Отмена записи",
                                                           "Cancel booking",
                                                           "Жазылымды болдырмау"])
def cancel_booking(message):
    user = users[message.chat.id]
    lang = user.get_language()

    responses = {
        "ru": "У вас нет активных записей.",
        "eng": "You have no active bookings.",
        "kz": "Сізде белсенді жазылымдар жоқ."
    }

    if user.get_appointment():
        appointment = user.get_appointment()
        user.cancel_appointment()
        cancel_messages = {
            "ru": f"Ваша запись {appointment.service} у {appointment.master} в {appointment.date} {appointment.time} отменена.",
            "eng": f"Your booking for {appointment.service} with {appointment.master} on {appointment.date} at {appointment.time} has been canceled.",
            "kz": f"Сіздің {appointment.service} қызметіне {appointment.master} маманына {appointment.date} күні {appointment.time} уақытына жазылуыңыз жойылды."
        }
        bot.send_message(user.chat_id, cancel_messages[lang])
    else:
        bot.send_message(user.chat_id, responses[lang])

        show_main_menu(user.chat_id, lang)

bot.set_my_commands([
    BotCommand("start", "Перезапустить бота"),
    BotCommand("settings", "Настройки"),
    BotCommand("main_menu", "Главное меню")
])

# Настройки
@bot.message_handler(commands=["settings"])
def settings(message):
    user = users[message.chat.id]
    lang = user.get_language()

    messages = {
        "ru": "Настройки:\n1. Сменить язык",
        "eng": "Settings:\n1. Change language",
        "kz": "Баптаулар:\n1. Тілді өзгерту"
    }

    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("Сменить язык") if lang == "ru" else
               KeyboardButton("Change language") if lang == "eng" else
               KeyboardButton("Тілді өзгерту"))

    bot.send_message(user.chat_id, messages[lang], reply_markup=markup)
    bot.register_next_step_handler(message, change_language)


@bot.message_handler(commands=["main_menu"])
def return_to_main_menu(message):
    user_id = message.chat.id
    lang = user_language.get(user_id, "ru")
    show_main_menu(user_id, lang)

# Смена языка
def change_language(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for lang in LANGUAGES.keys():
        markup.add(KeyboardButton(lang))

    bot.send_message(
        message.chat.id,
        "Выберите язык / Choose a language / Тілді таңдаңыз:",
        reply_markup=markup
    )
    bot.register_next_step_handler(message, set_language)

# Установка языка
def set_language(message):
    user = users[message.chat.id]
    user.set_language(LANGUAGES[message.text])
    lang = user.get_language()

    messages = {
        "ru": "Язык изменен на Русский",
        "eng": "Language changed to English",
        "kz": "Тіл Қазақ тіліне өзгертілді"
    }

    bot.send_message(user.chat_id, messages[lang])

# Возврат в главное меню
@bot.message_handler(commands=["main_menu"])
def return_to_main_menu(message):
    user = users[message.chat.id]
    lang = user.get_language()
    show_main_menu(user.chat_id, lang)


@bot.message_handler(func=lambda message: message.text in ["Мои записи", "My bookings", "Менің жазылымдарым"])
def show_my_bookings(message):
    user = users[message.chat.id]  # Получаем объект пользователя
    lang = user.get_language()  # Получаем язык пользователя

    # Получаем текущую запись пользователя
    appointment = user.get_appointment()

    if appointment:
        # Если запись существует, формируем сообщение
        booking_message = {
            "ru": f"📌 Ваша текущая запись:\n"
                  f"🛠 Услуга: {appointment.service}\n"
                  f"👤 Мастер: {appointment.master}\n"
                  f"📅 Дата: {appointment.date}\n"
                  f"⏰ Время: {appointment.time}",
            "eng": f"📌 Your current booking:\n"
                   f"🛠 Service: {appointment.service}\n"
                   f"👤 Master: {appointment.master}\n"
                   f"📅 Date: {appointment.date}\n"
                   f"⏰ Time: {appointment.time}",
            "kz": f"📌 Сіздің жазылуыңыз:\n"
                  f"🛠 Қызмет: {appointment.service}\n"
                  f"👤 Маман: {appointment.master}\n"
                  f"📅 Күні: {appointment.date}\n"
                  f"⏰ Уақыты: {appointment.time}"
        }
        bot.send_message(user.chat_id, booking_message[lang])
    else:
        # Если записи нет, отправляем сообщение об отсутствии записей
        no_booking_message = {
            "ru": "❌ У вас нет активных записей.",
            "eng": "❌ You have no active bookings.",
            "kz": "❌ Сізде белсенді жазылымдар жоқ."
        }
        bot.send_message(user.chat_id, no_booking_message[lang])

bot.polling(none_stop=True)