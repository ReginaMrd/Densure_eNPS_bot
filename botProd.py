import telebot
import csv
from chart_utils import build_pie_chart


# Указываем токен бота, который вы получили от BotFather в Telegram
TOKEN = ''

# Создаем объект бота
bot = telebot.TeleBot(TOKEN)

# Словарь для хранения ответов каждого пользователя
user_answers = {}

# Словарь для хранения комментариев
comments = {}

# Функция для вычисления eNPS
def calculate_nps():
    promoters = 0
    passives = 0
    detractors = 0

    for user_id, answers in user_answers.items():
        # Берем только последний ответ пользователя
        last_answer = answers[-1]

        if last_answer >= 9:
            promoters += 1
        elif last_answer >= 7:
            passives += 1
        else:
            detractors += 1

    total_responses = promoters + passives + detractors

    if total_responses == 0:
        return 0

    promoters_percent = (promoters / total_responses) * 100
    detractors_percent = (detractors / total_responses) * 100
    return promoters_percent - detractors_percent

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10')
            
    bot.send_message(message.chat.id, "Привет😊\nКак ты уже знаешь, мы регулярно собираем обратную связь у сотрудников.", reply_markup=markup)
    bot.send_message(message.chat.id, "Сегодня мы проводим опрос, чтобы понять, насколько ты удовлетворён работой в Densure и что можно улучшить. Опрос является анонимным, и мы будем благодарны за честную обратную связь. Просим ответить всего на один вопрос:", reply_markup=markup)
    bot.send_message(message.chat.id, "<b>На сколько вероятно, что ты порекомендуешь работу в нашей компании своим друзьям или знакомым?</b> <i>(Ответь на вопрос числом от 0 до 10.)</i>", reply_markup=markup, parse_mode='HTML')

# Обработчик ответа на вопрос
@bot.message_handler(func=lambda message: message.text.isdigit() and 0 <= int(message.text) <= 10)
def process_answer(message):
    user_id = message.from_user.id
    score = int(message.text)

    if user_id not in user_answers:
        user_answers[user_id] = []

    user_answers[user_id].append(score)


    # Сохраняем ответы в файл CSV
    with open('responses.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([user_id, score])
    # Отправляем соответствующий стикер в зависимости от оценки
    if score == 0:
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAED2nxl41gJLcMRYRbykOIK9PStCr3JswACvwQAAiBtOwAB_cxvpUFJxfg0BA')
    elif 1 <= score <= 5:
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAED2n5l41hY3M5X5ZCxpfK3vq-xTAM0DAACwQQAAiBtOwABJt1yAAGdcgQ6NAQ')
    elif 6 <= score <= 8:
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAED2oBl41hx-jt57ujws9WoLw_x1aigEgAC0gQAAiBtOwABGpQPENnnAYs0BA')
    elif 9 <= score <= 10:
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAED2oJl41iWYSY0lNtxe18LUcGQoDN2pAACvQQAAiBtOwABu5XYnmuPHNo0BA')


    # Если оценка меньше 7, запрашиваем комментарий
    if score < 7:
        bot.send_message(message.chat.id, "Спасибо за оценку! Мы ценим твою честность.")
        bot.send_message(message.chat.id, "Пожалуйста, оставь комментарий, что бы тебе хотелось улучшить?")
        bot.register_next_step_handler(message, ask_comment)
    else:
        bot.send_message(message.chat.id, "Спасибо за оценку! Мы ценим твою поддержку ❤️")
# Функция для запроса комментария
def ask_comment(message):
    user_id = message.from_user.id
    comment = message.text

    # Сохраняем комментарий
    if user_id not in comments:
        comments[user_id] = []

    comments[user_id].append(comment)
    bot.send_message(message.chat.id, "Благодарим за ответ! Постараемся сделать всё возможное, чтобы твоё сотрудничество с Densure стало ещё более комфортным ❤️")

# Обработчик команды /allcom для просмотра всех комментариев
@bot.message_handler(commands=['allcom'])
def show_all_comments(message):
    all_comments = []
    for user_comments in comments.values():
        all_comments.extend(user_comments)

    if all_comments:
        bot.send_message(message.chat.id, "\n".join(all_comments))
    else:
        bot.send_message(message.chat.id, "Комментариев пока нет.")


# Обработчик команды /enps для расчета eNPS
@bot.message_handler(commands=['enps'])
def show_nps(message):
    nps = calculate_nps()
    unique_responses = len(user_answers)
    bot.send_message(message.chat.id, f"Текущий показатель eNPS: {nps:.2f}\nВсего уникальных ответов: {unique_responses}")
    
        
    # Подсчитываем количество промоутеров, пассивов и детракторов
    promoters = sum(1 for answer in user_answers.values() if answer[-1] >= 9)
    passives = sum(1 for answer in user_answers.values() if 7 <= answer[-1] < 9)
    detractors = sum(1 for answer in user_answers.values() if answer[-1] < 7)
    
    # Выводим отдельно промоутеров, пассивов и детракторов
    bot.send_message(message.chat.id, f"Промоутеров: {promoters}")
    bot.send_message(message.chat.id, f"Пассивов: {passives}")
    bot.send_message(message.chat.id, f"Детракторов: {detractors}")
    

    # Строим круговую диаграмму
    build_pie_chart(promoters, passives, detractors)
    
    # Отправляем изображение с круговой диаграммой
    with open('pie_chart.png', 'rb') as chart:
        bot.send_photo(message.chat.id, chart)

    # Обработчик команды /reset для сброса старых ответов
@bot.message_handler(commands=['reset'])
def reset_answers(message):
    global user_answers
    global comments

    user_answers.clear()
    comments.clear()
    
    bot.send_message(message.chat.id, "Все старые ответы были успешно удалены.")

# Запускаем бота
bot.polling()