import subprocess
import difflib

from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
from logging.handlers import RotatingFileHandler
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = RotatingFileHandler('my_logger.log', maxBytes=500000, backupCount=5)
logger.addHandler(handler)
formatter = logging.Formatter(
    '%(asctime)s, %(levelname)s, %(name)s, %(message)s'
)
handler.setFormatter(formatter)

update = Updater(token=)
TELEGRAM_CHAT_ID = 

result = {"pk": 1412, "model": "Users",
          "fields": {"ip": "10.0.0.77", "mac": "64:64:4A:75:9C:D3", "id": 1412, "gen_pwd": "alfa1234"}}


def check_login_password(login: str, password: str) -> bool:
    login_1 = "02921"
    return login == login_1 and password == result['fields']['gen_pwd']  # type: ignore


def check_mac(mac_1: str) -> bool:
    mac_1 = mac_1.lower()
    mac_2 = 'a8:f9:4b'

    # if mac_1[:8] == mac_2[:8]
    match = difflib.SequenceMatcher(None, mac_1, mac_2)
    return match.ratio() * 100 > 50


def proces(update, context):
    lst = {}
    ip = update.message.text
    ip = ip.split()
    lst[ip[0]] = ip[1]
    print(lst)
    for i in lst:
        if not check_login_password(i, lst[i]):
            return update.message.reply_text("Invalid login and/or password")

    ip = result['fields']['ip']
    mac = result['fields']['mac']

    if not check_mac(mac):
        return update.message.reply_text('Невозможно диагностировать устройство')

    url = f'http://{ip}/cgi-bin/webif/admin/status-diag.sh'

    ping = subprocess.run(['ping', '-s 65000', '-c 10', '-i 0,2', ip], stdout=subprocess.PIPE)

    if ping.returncode == 0:
        update.message.reply_text(
            f'{ping.stdout.decode("utf-8")}\nСоединение до оптического преобразователя ELTEX у вас в доме установлено, диагностика прошла успешно')

    console = subprocess.run(['curl', '-u', 'admin:99461310', '-F', 'ping_button="Ping"', url],
                             stdout=subprocess.DEVNULL)
    if console.returncode == 0:
        return update.message.reply_text(
            'Соединение от оптического преобразователя ELTEX у вас в доме установлено, диагностика прошла успешно')
    else:
        return update.message.reply_text('Невозможно установить соединение')


    # update.message.reply_text('Происходит диагностика соединения до вашего оборудования, пожалуйста подождите...')
    # try:
    #     ping = subprocess.run(['ping', '-s 65000', '-c 10', '-i 0,2', ip], stdout=subprocess.PIPE)
    #     if ping.returncode == 0:
    #         logger.info('Сообщение отправлено')
    #         update.message.reply_text(
    #             f'{ping.stdout.decode("utf-8")}\nСоединение до оптического преобразователя ELTEX у вас в доме установлено, диагностика прошла успешно')
    #     else:
    #         update.message.reply_text('Невозможно установить соединение')
    # except Exception as error:
    #     logging.error(error)
    #     # ...
    #
    # url = f'http://{ip}/cgi-bin/webif/admin/status-diag.sh'
    #
    # update.message.reply_text('Происходит диагностика соединения от вашего оборудования, пожалуйста подождите...')
    # try:
    #     console = subprocess.run(['curl', '-u', 'admin:99461310', '-F', 'ping_button="Ping"', url],
    #                              stdout=subprocess.DEVNULL)
    #     if console.returncode == 0:
    #         logger.info('Сообщение отправлено')
    #         update.message.reply_text(
    #             'Соединение от оптического преобразователя ELTEX у вас в доме установлено, диагностика прошла успешно')
    #     else:
    #         return update.message.reply_text('Невозможно установить соединение')
    # except Exception as error:
    #     logging.error(error)


def wake_up(update, context):
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id,
                             text='Спасибо, что включили меня')


def main():
    update.dispatcher.add_handler(CommandHandler('start', wake_up))
    update.dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), proces))

    update.start_polling()
    update.idle()


if __name__ == '__main__':
    main()
