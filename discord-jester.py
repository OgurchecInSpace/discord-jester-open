import os  # Зачем-то импорт os
import discord  # импорт апи дискорда
from discord.ext import commands  # импорт ещё одной штуки апи дискорда
from random import choice, randrange  # Импорт рандом
from datetime import datetime  # импорта датывремени
import glob  # импорт для поиска фоток для Жака Фреско
import json  # импорт жисон
import pprint as pp  # Красиво пишем
import sympy as sp

from config import settings  # Импорт настроек
from phrases_and_words import words_hello  # Импорт слов для приветствия
from jokes import list_jokes  # импорт шутОчек

prefix = settings["prefix"]
images = glob.glob("Images/*.jpg")

intents = discord.Intents.default()
intents.members = True
intents.presences = True
client = discord.Client(intents=intents)


# функция генерации предложения
def generate_message():
    with open('words.txt', 'r', encoding='utf-8') as words_file:
        words = tuple(map(lambda word: word.strip(), words_file.readlines()))
        new_words = []
        for word in ' '.join(words).split():
            if not word.isdigit():
                new_words.append(word)
        n = randrange(4, 10)
        end = choice(['.', '!', '?', '...'])
        txt = ' '.join(tuple([choice(new_words) for _ in range(n)]))
        return (txt + end).capitalize()


date_launch = datetime.now()


def read_data(message):  # Чтение даты
    global date_launch
    print(f'Последний запуск - {date_launch}')
    with open('data.json', 'r', encoding='utf-8') as data_file:
        data = json.loads(data_file.read())
        for index_guild, guild in enumerate(client.guilds):
            if {} not in data['servers']:
                data['servers'].append({})
            data['servers'][index_guild]['name'] = guild.name
            data['servers'][index_guild]['users'] = [user.name for user in guild.members]

    with open('data.json', 'w', encoding='utf-8') as data_file:
        pp.pprint(data)
        json.dump(data, data_file)

    date_launch = datetime.now()


def get_words(message):
    with open('words.txt', 'a', encoding='utf-8') as words:  # Занесение сообщения и его частей в файл
        some_words = ''
        for word in message.content.split():
            if not word.lower().startswith('https://') and not word.lower().startswith(
                    prefix) and not message.embeds and not message.author.bot:
                new_word = ''
                for symbol in list(word):
                    if symbol not in ''',./'"_-()[]{}$#@!!&:;`~\|<>#^*№?''':
                        new_word += symbol
                some_words += f' {new_word}'
                len_digits_sw = len([l for l in some_words if l in '0123456789'])
                len_digits_nw = len([l for l in new_word if l in '0123456789'])
                if len(some_words) * 0.70 > len_digits_sw:
                    print(some_words.strip().lower(), file=words)
                if len(new_word) * 0.70 > len_digits_nw:
                    print(new_word.strip().lower(), file=words)


# Команды бота
def hello(message):
    author = message.author
    create_logs('Привет', message.author, message.channel.name, message.guild.name)
    return message.channel.send(f'{choice(words_hello)}, {author.mention}')


def commands(message):
    text_commands = discord.Embed(title='Команды')
    text_commands.set_footer(text='\n'.join([f'{command} - {info}' for command, info in bot_commands_info.items()]))
    create_logs('Команды', message.author, message.channel.name, message.guild.name)
    return message.channel.send(embed=text_commands)


def joke(message):
    create_logs('Шутка', message.author, message.channel.name, message.guild.name)
    return message.channel.send(choice(list_jokes))


def fresko(message):
    image = choice(images)
    create_logs('Жак Фреско', message.author, message.channel.name, message.guild.name)
    return message.channel.send(file=discord.File(image))


def not_found_command(message):
    create_logs(message.content[1:], message.author, message.channel.name, message.guild.name, command_found=False)
    return message.channel.send(f'Команда {message.content} не найдена')


def accordion(message):
    create_logs('Баян', message.author, message.channel.name, message.guild.name)
    adress = 'баян.jpg'
    return message.channel.send(file=discord.File(adress))


def top_secret(message):  # Ошень секретно
    create_logs('top_secret', message.author, message.channel.name, message.guild.name)
    return message.channel.send('Ты думал, здесь что-то будет?')


# Семейство калькуляторов
calculators_command = {f'{prefix}калькулятор обычное', f'{prefix}калькулятор уравнение',
                       f'{prefix}калькулятор упрощение'}


def calculate_classic(message, expression):  # Команда калькулятора обычного
    try:
        for letter, good_letter in {'^': '**', ',': '.'}.items():
            expression = expression.replace(letter, good_letter)
        expression = eval(expression)
        create_logs('Калькулятор', message.author, message.channel.name, message.guild.name)
        return message.channel.send(expression)
    except:
        create_logs('Калькулятор', message.author, message.channel.name, message.guild.name, done=False)
        return message.channel.send('Не корректно вызвана команда')


def calculate_equation(message, expression):  # Команда калькулятора уравнений (доделать)
    try:
        return message.channel.send('не работает')
        for letter, good_letter in {'^': '**', ',': '.'}.items():
            expression = expression.replace(letter, good_letter)
        res = expression[expression.rfind('=') + 1:]
        expression = expression[:expression.rfind('=')]
        print(expression, '///', res)
        expression = sp.Eq(expression, res)
        return message.channel.send(expression)
    except:
        pass


def calculate_simplification(message, expression):  # Команда калькулятора для упрощения
    try:
        for letter, good_letter in {'^': '**', ',': '.'}.items():
            expression = expression.replace(letter, good_letter)
        expression = str(sp.expand(expression))
        expression = str(sp.simplify(expression))
        expression = expression.replace('**', '^').replace('*', '')
        return message.channel.send(expression)
    except:
        create_logs('Упрощение', message.author, message.channel.name, message.guild.name, done=False)
        return message.channel.send('Не корректно вызвана команда')


def fonetic(message):
    create_logs('Фонетический разбор (не работающий)', message.author, message.channel.name, message.guild.name)
    return message.channel.send('Не работает, кому говорю')


# Словарь с командами
bot_commands = {
    f'{prefix}привет': hello,
    f'{prefix}команды': commands,
    f'{prefix}шутка': joke,
    f'{prefix}фраза': phrase,
    f'{prefix}жак фреско': fresko,
    f'{prefix}баян': accordion,
    f'{prefix}top_secret': top_secret,

    f'{prefix}калькулятор': calculate_classic,
    f'{prefix}уравнение': calculate_equation,
    f'{prefix}упрощение': calculate_simplification,

    f'{prefix}фонетический разбор': fonetic
}

# Словарь с описанием команд
bot_commands_info = {
    f'{prefix}Привет': 'Приветствие от бота',
    f'{prefix}Команды': 'Список команд',
    f'{prefix}Шутка': 'ШуТкА от бота',
    f'{prefix}Фраза': 'ФрАзА от бота',
    f'{prefix}Жак Фреско': 'МеМ с ЖаКоМ фРеСкОм',
    f'{prefix}Баян': 'Баян',
    f'{prefix}Калькулятор <выражение>': 'посчитает вам',
    f'{prefix}Уравнение <выражение>': 'попробует решить уравнение (но вряд ли у него получится)',
    f'{prefix}Упрощение <выражение>': 'попробует упростить',
    f'{prefix}Фонетический разбор': 'не работает'
}


def get_date():
    return str(datetime.today()).split(".")[0]  # получение даты в хорошем формате


def create_logs(mode, author, channel, server, command_found=True, done=True):  # создание лога
    with open('logs.txt', 'a', encoding='utf-8') as log_file:
        if command_found:
            print(f'[{get_date()}] Вызвана "{prefix}{mode}" от {author} в {channel} на {server}')  # создание лога
            print(f'[{get_date()}] Вызвана "{prefix}{mode}" от {author} в {channel} на {server}',
                  file=log_file)  # запись лога в файл
        else:
            print(
                f'[{get_date()}] Вызвана "{prefix}{mode}" от {author} в {channel} на {server}, которая не существует')  # создание лога, если команда не существует
            print(f'[{get_date()}] Вызвана "{prefix}{mode}" от {author} в {channel} на {server}, которая не существует',
                  file=log_file)  # запись лога в файл
        if not done:
            print(
                f'[{get_date()}] Вызвана "{prefix}{mode}" от {author} в {channel} на {server}, но она вызвана не корректно')  # создание лога
            print(
                f'[{get_date()}] Вызвана "{prefix}{mode}" от {author} в {channel} на {server}, но она вызвана не корректно', file=log_file)  # запись лога в файл


@client.event
async def on_ready():
    print(f'Загрузились как {client.user}')  # Загрузка
    await client.change_presence(status=discord.Status.online, activity=discord.Game("%Команды"))


@client.event  # основная часть программы с получением сообщения
async def on_message(message):
    global calculator_commands
    if message.author == client.user:  # Проверка, что автор сообщения - не сам бот
        return None
    if message.content.startswith(prefix):
        query_message = message.content.lower()  # получаем имя команды
        if any([query_message.startswith(txt) for txt in
                {f'{prefix}калькулятор', f'{prefix}уравнение', f'{prefix}упрощение'}]):
            expression = ' '.join(query_message.split()[1:])
            query_message = query_message.split()[0]
            await bot_commands[query_message](message, expression)
        else:
            await bot_commands.get(query_message, not_found_command)(message)  # Запрос команды

    get_words(message)

    if not randrange(0, 10) and not message.author.bot:
        await message.channel.send(
            generate_message())  # Случайная отправка этого всего дела (нагенерированного сообщения)

    if date_launch.day < datetime.now().day or date_launch.month < datetime.now().month or date_launch.year < datetime.now().year:
        print(f'Сейчас - {datetime.now()}')
        read_data(message)


client.run(settings['token'])  # пабежали
