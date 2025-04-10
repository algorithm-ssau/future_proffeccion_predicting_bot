# Бот-предсказатель профессии будущего
Телеграм-бот, который предсказывает год, профессию и место работы пользователя. 
Бот приветствует пользователя и запрашивает имя и дату рождения человека, после чего случайным образом определяет, кем и где будет работать человек. Также с помощью ИИ генерируется изображение соответствующей профессии.

Инструкция по запуску:
1. В коде в 194 строке вставить токен от своего бота (токен выдает @BotFather)
2. На сервере создать папку bot
3. Скопировать в папку файлы main.py, cities.py, professions.py
4. Авторизоваться на сервере через терминал
5. Прописать по очереди следующие комманды:
6. cd bot
7. sudo apt update
8. sudo apt install python3-venv -y
9. python3 -m venv venv
10. source venv/bin/activate
11. pip install python-telegram-bot==20.3
12. pip install logging
13. pip install os
14. pip install json
15. pip install base64
16. pip install io
17. pip install asyncio
18. tmux new -s bot
19. python3 main.py
