import time
import sys

def print_slowly(text, delay=0.03):
    """Печатает текст посимвольно с задержкой."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()  # Перевод строки в конце

# Ваш текст (безопасная версия)
text =      """Первым делом нам нужно проверить этот номер на валидность. Заходим на сайт https://smsc.ru/testhlr/ и отправляем HLR запрос на найденный номер.
Если сайт отображает данный запрос:

То можно идти дальше. Если же пишет, что номер телефона не находится в сети, это может объясниться 3 причинами:
-Номер телефона стар, заблокирован.
-Включен режим полета
-Номер телефона виртуален.

Даже если номер не в сети можно дальше деанонить сайт иногда тупит.


Поиск по URL

4. https: //my.mail.ru/fb/USERID - найдет аккаунт в Моем Мире, замените USERID в ссылке на ID аккаунта.

дополнение:
Мощный инструмент для пробива информации по номеру(мультисервисы)Ф

https://github.com/sundowndev/PhoneInfoga

Sherlock
Самый мощный известный мне инструмент по пробиву ника

https://github.com/sherlock-project/sherlock

Photon
Очень сильный кравлер(Выгрузка информации с сайтов)

https://github.com/s0md3v/Photon

Библия пентестера
Крупнейший сборник информации по пентесту, что тебе пригодится в будущем.Информация на английском, и информации настолько дохуя, что эге по английскому языку ты сдашь на нехуй делать.

https://github.com/blaCCkHatHacEEkr/PENTESTING-BIBLE

Если же тебе это нахуй не интересно, держи материал с этой библии для OSINT

4500 гугл дорков — https://sguru.org/ghdb-download-list-4500-google-dork..

OSINT Ресурсы 2019 — https://medium.com/p/b15d55187c3f

OSINT Тулкит — https://medium.com/@micallst/osint-resources-for-2019..

Визуализация информации OSINT — https://medium.com/hackernoon/osint-tool-for-visualiz..

Instagram OSINT — https://medium.com/secjuice/what-a-nice-picture-insta..

Наилучший сборник OSINT
https://github.com/jivoi/awesome-osint

СЛОЖНЕЙШИЙ ИНСТРУМЕНТ SPIDERFOOT(Lampyre Lighthouse на стероидах)
https://github.com/smicallef/spiderfoot

Для тебя это будет заданием — поставить эту хуету, и подключить все бесплатные API

Общий OSINT GitHub топик
https://github.com/topics/osint



Боты
├ Quick OSINT — найдет оператора, email, как владелец записан в контактах, базах данных и досках объявлений, аккаунты в соц. сетях и мессенджерах, в каких чатах состоит, документы, адреса и многое другое
├ @clerkinfobot — бот берет данные из приложения getcontact, показывает как записан номер телефона в контактах
├ @dosie_Bot — как и в боте uabaza дает информацио о паспорте только польностью, 3 бесплатные попытки
├ @find_caller_bot — найдет ФИО владельца номера телефона
├ @get_caller_bot — поиск по утечкам персональных данных и записным книгам абонентов, может найти ФИО, дату рождения, e-mail
├ @get_kolesa_bot — найдет объявления на колеса.кз
├ @get_kontakt_bot — найдет как записан номер в контактах, дает результаты что и getcontact
├ @getbank_bot — дает номер карты и полное ФИО клиента банка
├ @GetFb_bot — бот находит Facebook
├ @Getphonetestbot — бот берет данные из приложения getcontact, показывает как записан номер телефона в контактах
├ @info_baza_bot — поиск в базе данных
├ @mailsearchbot — найдет часть пароля
├ @MyGenisBot — найдет имя и фамилию владельца номера
├ @phone_avito_bot — найдет аккаунт на Авито
├ @SafeCallsBot — бесплатные анонимные звонки на любой номер телефона с подменой Caller ID
└ @usersbox_bot — бот найдет аккаунты в ВК у которых в поле номера телефона указан искомый номер

⚙ Ресурсы
├ lampyre.io — программа выполняет поиск аккаунтов, паролей и многих других данных
├ avinfo.guru — проверка телефона владельца авто, иногда нужен VPN
├ fa-fa.kz — найдет ФИО, проверка наличия задолженностей, ИП, и ограничения на выезд
├ getcontact.com — найдет информацию о том как записан номер в контактах
├ globfone.com — бесплатные анонимные звонки на любой номер телефона
├ mirror.bullshit.agency — поиск объявлений по номеру телефона
├ mysmsbox.ru — определяет чей номер, поиск в Instagram, VK, OK, FB, Twitter, поиск объявлений на Авито, Юла, Из рук в руки, а так же найдет аккаунты в мессенджерах
├ nuga.app — найдет Instagram аккаунт, авторизация через Google аккаунт и всего 1 попытка
├ numberway.com — найдет телефонный справочник
├ personlookup.com.au — найдет имя и адрес
├ phoneInfoga.crvx.fr — определят тип номера, дает дорки для номера, определяет город
├ spravnik.com — поиск по городскому номеру телефона, найдет ФИО и адрес
├ spravochnik109.link — поиск по городскому номеру телефона, найдет ФИО и адрес
├ teatmik.ee — поиск в базе организаций, ищет номер в контактах
└ truecaller.com — телефонная книга, найдет 

🔨 Восстановление доступа
├ ICQ — icq.com/password/ru
├ Yahoo — login.yahoo.com/?display=login
├ Steam — help.steampowered.com/ru/wizard/HelpWithLoginInfo
├ Twitter — twitter.com/account/begin_password_reset
├ VK.com — vk.com/restore
├ Facebook — facebook.com/login/identify?ctx=recover
├ Microsoft — account.live.com/acsr
└ Instagram — instagram.com/accounts/password/reset
@killerkill88_bot
@EyeOfAllah_bot узнать айди может показать номер не полный
@poiskorRobot
@UniversalSearchRobot Очень полезный бот

Социальная информация

1. haveibeenpwned.com - проверка просочившихся баз данных

2. emailrep.io - найти сайты, на которых был зарегистрирован аккаунт по электронной почте

3. dehashed.com - проверка почты в просочившихся базах данных

4. @Smart_SearchBot - найдите полное имя, DoB, адрес и номер телефона

5. pwndb2am4tzkvold.onion - поиск в pwndb, также поиск по паролю

6. intelx.io - многофункциональная поисковая система, поиск ведется также и в даркнете

7. @mailsearchbot - поиск по базе, выдает пароль частично

8. @shi_ver_bot - взломанные пароли

9. @info_baza_bot - показать с какой базы просочилась почта, 2 бесплатных сканирования

10. leakedsource.ru - покажите, из какой базы просочилась почта

11. mostwantedhf.info - найти аккаунт в скайпе

12. email2phonenumber (t) - автоматически собирает данные со страниц восстановления аккаунта и находит номер телефона.

13. spiderfoot.net (r) - автоматический поиск с использованием огромного количества методов, инструмент доступен в облаке с регистрацией

14. reversegenie.com - поиск местоположения, первой буквы имени и телефонных номеров

15. searchmy.bio - найти инстаграм-аккаунт с адресом электронной почты в описании

17. leakprobe.net - найдет ник и источник утечки базы данных.

18.) Получите информацию fb по электронной почте"""

print_slowly(text, delay=0.02)