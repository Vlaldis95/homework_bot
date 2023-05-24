import logging
import os
import sys
import time

import requests
import telegram
from dotenv import load_dotenv

from exceptions import APIError, StatusError

load_dotenv()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
handler = logging.StreamHandler()
logger.addHandler(handler)
handler.setFormatter(formatter)

PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_PERIOD = 600.0
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}


def check_tokens():
    """Проверка доступности переменных окружения."""
    for token in (PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID):
        if token is None:
            logger.critical(f'Отсутствует переменная окружения {token}')
    return all([PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID])


def send_message(bot, message):
    """Отправка сообщения в телеграмм-чат."""
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
    except Exception as e:
        logger.error(f'Не удалось отправить сообщение из-за ошибки {e}')
    else:
        logger.debug('Удалось отправить сообщение')


def get_api_answer(timestamp):
    """Выполнение запроса к API практикума."""
    params = {'from_date': timestamp}
    try:
        response = requests.get(ENDPOINT, headers=HEADERS, params=params)
    except requests.exceptions.RequestException:
        print('Сбой запроса к API')
    else:
        if response.status_code != 200:
            raise StatusError('код запроса к API не равен 200!')
        return response.json()


def check_response(response):
    """Проверяет ответ API на корректность."""
    if not isinstance(response, dict):
        raise TypeError('Формат ответа не словарь')
    if 'homeworks' not in response:
        logger.error('В API ответа нет ключа homeworks')
    homework = response.get('homeworks')
    if not isinstance(homework, list):
        raise TypeError('Формат ответа по дз не список')
    return homework


def parse_status(homework):
    """Извлечение информации из JSON-данных API практикума."""
    homework_name = homework.get('homework_name')
    homework_status = homework.get('status')
    if homework_name is None:
        raise APIError('Данных о домашней работе нет')
    if homework_status in HOMEWORK_VERDICTS:
        verdict = HOMEWORK_VERDICTS[homework_status]
        return f'Изменился статус проверки работы "{homework_name}". {verdict}'
    else:
        logging.error(f'Данных о таком статусе нет: {homework_status}')
        raise APIError(
            f'Данных о таком статусе нет: {homework_status}')


def main():
    """Основная логика работы бота."""
    if not check_tokens():
        sys.exit(0)
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    timestamp = int(time.time())
    while True:
        try:
            response = get_api_answer(timestamp)
            checked_response = check_response(response)
            if len(checked_response) > 0:
                message = parse_status(checked_response[0])
            else:
                message = 'Обновлений статуса нет'
            send_message(bot, message)
        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            send_message(bot, message)
        timestamp = response.get('current_date', timestamp)
        time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    main()
