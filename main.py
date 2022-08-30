import difflib
import subprocess

result = {"pk": 1412, "model": "Users",
          "fields": {"ip": "10.0.0.77", "mac": "A8:F9:4B:02:E5:61", "id": 1412, "gen_pwd": "alfa1234"}}
login_2 = str(input())
password_2 = str(input())


# print(a[a.find(':')+1 : a.find('.')])
# da:f4:03:39:0e:dd

def check_login_password(login: str, password: str) -> bool:
    login_1 = "02921"
    return login == login_1 and password == result['fields']['gen_pwd']  # type: ignore
    # if login == login_1:
    # if password == result['fields']['gen_pwd']:
    # return True
    # return 'Логин и пароль верны'
    # else:
    # return 'Не верный пароль'
    # else:
    # return 'Не верный логин'


def check_mac(mac_1: str) -> bool:
    mac_1 = mac_1.lower()
    mac_2 = 'a8:f9:4b'

    # if mac_1[:8] == mac_2[:8]
    match = difflib.SequenceMatcher(None, mac_1, mac_2)
    return match.ratio() * 100 > 50
    # return True
    # else:
    # return 'Невозможно диагностировать устройство'


def main():
    if not check_login_password(login_2, password_2):
        # bot.send_message("Invalid login and/or password")
        return "Invalid login and/or password"

    # if check_lw is True:
    ip = result['fields']['ip']
    mac = result['fields']['mac']
    check_m = check_mac(mac)

    if not check_mac(mac):
        # bot.send_message('Невозможно диагностировать устройство')
        return 'Невозможно диагностировать устройство'

    url = f'http://{ip}/cgi-bin/webif/admin/status-diag.sh'

    ping = subprocess.run(['ping', '-s 65000', '-c 10', '-i 0,2', ip], stdout=subprocess.PIPE)
    console = subprocess.run(['curl', '-u', 'admin:99461310', '-F', 'ping_button="Ping"', url],
                             stdout=subprocess.DEVNULL)

    if ping.returncode == 0:
        # bot.send_message
        return (
            f'{ping.stdout.decode("utf-8")}\nСоединение до оптического преобразователя ELTEX у вас в доме установлено, диагностика прошла успешно')
    if console.returncode == 0:
        # bot.send_message
        return (
            'Соединение от оптического преобразователя ELTEX у вас в доме установлено, диагностика прошла успешно')
    else:
        # bot.send_message
        return ('Невозможно установить соединение')


# print(check_lw)


if __name__ == '__main__':
    main()

# str_1 = 'A8:F9:4B'
# str_2 = 'A8:F9:4B:02:BA:81'
#
# match = difflib.SequenceMatcher(None, str_2, str_1)
# if match.ratio() * 100 > 50:
#     print(match.ratio(), 'Success')
# else:
#     print(match.ratio(), 'Fuck yourself')
#
# result = {"pk": 1412, "model": "Users",
#           "fields": {"ip": "192.168.100.5", "mac": "da:f4:03:39:0e:dd", "id": 1412, "gen_pwd": "alfa1234"}}
#
#
# def status_connection():
#     ip = '83.217.13.196'
#     url = f'http://{ip}/cgi-bin/webif/admin/status-diag.sh'
#
#     ping = subprocess.Popen(['ping', '-s 30000', '-c 10', '-i 0,2', ip], stdout=subprocess.DEVNULL)
#     stdoutdata, stderrdata = ping.communicate()
#     console = subprocess.Popen(['curl', '-u', 'admin:99461310', '-F', 'ping_button="Ping"', url],
#                                stdout=subprocess.DEVNULL)
#     stdoutdata, stderrdata = console.communicate()
#
#     if ping.returncode == 0 and console.returncode == 0:
#         return 'Соединение установлено, диагностика прошла успешно'
#     else:
#         return 'Невозможно установить соединение'

# 83.217.13.196
