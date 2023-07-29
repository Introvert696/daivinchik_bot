import telebot
from database import Database

dbworker = Database()
dbworker.createDB()


token = "5910689968:AAG4N8nfP7EQYhe-SVQL2NvPOg-3617rM_k"
bot = telebot.TeleBot(token)
context = ""  # переменная, которая показывает что сейчас должен делать пользователь
name = ""
age = ""
city = ""
content = ""
photo = ""
sex = 0
sex_search = 0
is_search = False


def getAnket(message):
    swith = True
    while swith:

        random_user = dbworker.getRandomUser(message.from_user.id)

        if random_user[1] != message.from_user.id:
            anketa = f'{random_user[3]} , {random_user[4]}. \n{random_user[7]}'
            bot.send_photo(message.chat.id, random_user[5])
            bot.send_message(message.chat.id, anketa)
            swith = False
            return random_user[0]


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(
        message.chat.id, "Добро пожаловать в бота, для начала вам нужно создать свою анкету, чтобы создать анкету, напишите - Анкета")


@bot.message_handler(func=lambda _: True)
def handle_message(message):
    global context
    global name
    global age
    global city
    global content
    global is_search
    current_anket = None  # текущая анкета
    registered = dbworker.checkUserId(str(message.from_user.id))
    # Проверка есть ли юзер в бд, если нету будем регать
    if not registered:
        bot.send_message(
            message.chat.id, "У вас нет анкеты, давайте ее создадим")
        msg = bot.send_message(
            message.chat.id, "Какого вы пола (парень, девушка)?")
        bot.register_next_step_handler(msg, getSex)

    else:

        if is_search == False and (message.text == "1. Смотреть анкеты" or message.text == "1"):
            is_search = True
            current_anket = getAnket(message)

            # print(anket_id)  # получаем id  просматриваемой анкеты

        elif is_search == False and (message.text == "1. Смотреть анкеты" or message.text == "1"):
            current_anket = getAnket(message)

        elif is_search and message.text == "Лайк":
            print(current_anket)
            user_id = dbworker.getUserId(message.from_user.id)
            # если лайк, то берем current_anket и добавляем новую строку (выполняем ффункцию)
            dbworker.saveAnswer(user_id, current_anket, 1)
            current_anket = getAnket(message)

        elif is_search and message.text == "Дизлайк":

            dbworker.saveAnswer(
                getUserId(message.from_user.id, current_anket, 0))
            current_anket = getAnket(message)
            # если дизлайк то вызывем функцию, которая добавляет дизлайк строку в таблицу и обновляем current anket
        elif is_search and message.text == "Отправить сообщение":
            # если нажал это то пишем что типо напиши сообщение и передаем на register_next_step_handler где сохраняем сообщение,
            # и информируем что сообщение отправлено, так же выводим новую акеты
            pass
        elif is_search and message.text == "Ждать":
            is_search == False
            bot.send_message(message.chat.id,
                             "1. Смотреть анкеты \r\n2. Посмотреть мою анкету\r\n3. Я больше не хочу никого искать")

        else:
            bot.send_message(message.chat.id,
                             "1. Смотреть анкеты \r\n2. Посмотреть мою анкету\r\n3. Я больше не хочу никого искать")


def getSex(message):
    global sex
    text = message.text
    if text == "Парень" or text == "парень":
        sex = 1
    msg = bot.send_message(
        message.chat.id, "Вас интересуют (девушки, парни)"
    )
    bot.register_next_step_handler(msg, getSexSearch)


def getSexSearch(message):
    global sex_search
    text = message.text
    if text == "Парни" or text == "парни":
        sex_search = 1
    msg = bot.send_message(message.chat.id, "Хорошо, теперь как вас зовут?")
    bot.register_next_step_handler(msg, getName)


def getName(message):
    global name
    name = message.text
    msg = bot.send_message(
        message.chat.id, "Хорошо, а теперь скажите, сколько вам лет?")
    bot.register_next_step_handler(msg, getAge)


def getAge(message):
    global age
    age = message.text
    msg = bot.send_message(
        message.chat.id, "Замечательно, из какого вы города")
    bot.register_next_step_handler(msg, getCity)


def getCity(message):
    global city
    city = message.text
    msg = bot.send_message(
        message.chat.id, "О круто как. А теперь черканите что нибудь в анкету")
    bot.register_next_step_handler(msg, getContent)


def getContent(message):
    global content
    content = message.text
    msg = bot.send_message(
        message.chat.id, "Ну вы и писатель. А теперь жду ваше фото")
    bot.register_next_step_handler(msg, getPhoto)


def getPhoto(message):
    global photo
    global name
    global age
    global content
    global city

    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)
    photo = downloaded_file
    msg = bot.send_message(message.chat.id, "Почти все готово")
    bot.send_photo(message.chat.id, photo)
    bot.send_message(message.chat.id, name+" - "+age+". "+city+"\n"+content)
    mes = bot.send_message(message.chat.id, "Все верно?")
    bot.register_next_step_handler(mes, checkInfo)


def checkInfo(message):
    global photo
    global name
    global age
    global content
    global city
    if (message.text == "Да"):
        msg = bot.send_message(message.chat.id, "Информация сохранена")
        dbworker.saveUser(
            message.from_user.id, message.from_user.username, name, age, photo, city, content, sex, sex_search)
        bot.send_message(
            message.chat.id, "1. Смотреть анкеты \r\n2. Посмотреть мою анкету\r\n3. Я больше не хочу никого искать")
    else:
        bot.send_message(message.chat.id, "Заполняем заново")
        msg = bot.send_message(message.chat.id, "Как вас зовут?")
        bot.register_next_step_handler(msg, getName)


def menu(message):
    bot.send_message(
        message.chat.id, "1. Смотреть анкеты \r\n2.Посмотреть мою анкету\r\n3.Я больше не хочу никого искать")


if __name__ == "__main__":
    bot.polling()
