# Homework Bot - Бот для проверки статуса домашней работы на код ревью в Яндекс.Практикум

## Простой бот работающий с API Яндекс.Практикум, весь функционал-это отображать статус проверки кода ревью вашей работы.

Работает как на ПК так и на Heroku, достаточно запустить бота, прописать токены. Каждые 10 минут бот проверяет API Яндекс.Практикум. И присылает в телеграм статус. Если работа проверена вы получите сообщение о статусе вашего код ревью.

У API Практикум.Домашка есть лишь один эндпоинт:

**https://practicum.yandex.ru/api/user_api/homework_statuses/**

и доступ к нему возможен только по токену.

Получить токен можно по адресу. Копируем его, он нам пригодится чуть позже.

### Принцип работы API

Когда ревьюер проверяет вашу домашнюю работу, он присваивает ей один из статусов:

* работа принята на проверку
* работа возвращена для исправления ошибок
* работа принята

### Запуск на ПК

* Клонируем проект:

'''bash
git clone https://github.com/themasterid/homework_bot.git
'''

или

' git clone git@github.com:themasterid/homework_bot.git

* Переходим в папку с ботом.

cd homework_bot
Устанавливаем виртуальное окружение

python -m venv venv
Активируем виртуальное окружение

source venv/Scripts/activate
Для деактивации виртуального окружения выполянем (после работы)

deactivate
Устанавливаем зависимости

pip install -r requirements.txt
В консоле импортируем токены для ЯндексюПрактикум и для Телеграмм:

export PRACTICUM_TOKEN=<PRACTICUM_TOKEN>
export TELEGRAM_TOKEN=<TELEGRAM_TOKEN>
export CHAT_ID=<CHAT_ID>
Запускаем бота

python homework.py
Бот будет работать, и каждые 10 минут проверять статус вашей домашней работы.

Автор: Лукьяненко Владислав 

