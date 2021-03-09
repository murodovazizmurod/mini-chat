from flask import Flask, request, abort, send_from_directory

import datetime as dt
import time


servername = "Chat Server"
starttime = dt.datetime.now()


bot_active = True




app = Flask(__name__)

messages = []

users = {}




# Функция логики бота вызывается после каждого сообщени пользователей,
# если ответить нечего возвращает пустую строку



def filter_messages(elements, key, min_value):
    new_elements = []
    for element in elements:
        if element[key] > min_value:
            new_elements.append(element)
    return new_elements


@app.route("/")
def index_view():
    return f"Welcome to {servername}. For current status click <a href='/status'>here</a><br/>For web-client click <a href='/webclient'>here</a>"


@app.route("/webclient")
def webclient_view():
    return send_from_directory(directory=".", filename='web-client.html')


@app.route("/status")
def status_view():
    return {'status': True,
            'name': servername,
            'time': time.time(),
            'uptime': str(dt.datetime.now() - starttime),
            'client-ip': request.remote_addr,
            'users-registered': len(users),
            'messages-count': len(messages)
            }


@app.route("/send", methods=['POST'])
def send_view():
    name = request.json.get('name')
    password = request.json.get('password')
    text = request.json.get('text')
    for token in [name, password, text]:
        if not (isinstance(token, str) and (len(token) > 0) and (len(token) < 1024)):
            abort(400)
    if name in users:
        if users[name] != password:
            abort(401)
    else:
        users[name] = password
    messages.append({'name': name, 'time': time.time(), 'text': text})

    return {'ok': True}


@app.route("/messages")
def messages_view():
    try:
        after = float(request.args['after'])
    except:
        abort(400)
    return {'messages': filter_messages(messages, key='time', min_value=after)}


messages.append({'name': servername, 'time': time.time(), 'text': 'Chatga xush kelibsizlar!\nChat hozirda BETA rejimda ishlamoqda!'})
app.run(host='0.0.0.0')
