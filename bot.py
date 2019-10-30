# ████████╗███████╗██╗     ███████╗ ██████╗ ██████╗  █████╗ ███╗   ███╗
# ╚══██╔══╝██╔════╝██║     ██╔════╝██╔════╝ ██╔══██╗██╔══██╗████╗ ████║
#   ██║   █████╗  ██║     █████╗  ██║  ███╗██████╔╝███████║██╔████╔██║
#   ██║   ██╔══╝  ██║     ██╔══╝  ██║   ██║██╔══██╗██╔══██║██║╚██╔╝██║
#   ██║   ███████╗███████╗███████╗╚██████╔╝██║  ██║██║  ██║██║ ╚═╝ ██║      v 0.7
#   ╚═╝   ╚══════╝╚══════╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝
#                ██████╗ ███████╗███████╗███████╗███╗   ██╗██████╗ ███████╗██████╗
#                ██╔══██╗██╔════╝██╔════╝██╔════╝████╗  ██║██╔══██╗██╔════╝██╔══██╗
#                ██║  ██║█████╗  █████╗  █████╗  ██╔██╗ ██║██║  ██║█████╗  ██████╔╝
#                ██║  ██║██╔══╝  ██╔══╝  ██╔══╝  ██║╚██╗██║██║  ██║██╔══╝  ██╔══██╗
#                ██████╔╝███████╗██║     ███████╗██║ ╚████║██████╔╝███████╗██║  ██║
#                ╚═════╝ ╚══════╝╚═╝     ╚══════╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝  ╚═╝
# ***by Night Sky Studios (night-sky-studios.com) special for Yale Fox (yalefox.com)
# **********************************************************************************

# Imports all the modules that we will need for this project, and an explanation of what each one does.
import time

import json
# Allows us to encode and decode JSON (JavaScript Object Notation) files
# https://docs.python.org/3/library/json.html#module-json
from threading import Timer

from urllib.parse import urlparse
# Allows you to parse a URL into components.
# https://docs.python.org/3/library/urllib.parse.html?highlight=urllib%20parse#module-urllib.parse

from telebot.types import Message
# Telegram Bots for python
# https://github.com/eternnoir/pyTelegramBotAPI/blob/master/telebot/types.py#L250

import telebot
# Telegram bot library
# https://pypi.org/project/telebot/


import traceback
# Allows you to extract, format and output stack traces in Python programs.
# https://docs.python.org/2/library/traceback.html

from groups import Groups
# Custom Groups object for easier data handling
# Detailed descriptions in groups.py file

from datetime import datetime
# Basic date and time
# https://docs.python.org/2/library/datetime.html

from AviraPyApi.Avira import Avira


# This scans a message for URLs, every time one is posted
def find_url(message):
    try:
        entities = message.json['entities']
    except KeyError:
        return None
    urls = []
    for e in entities:
        if e['type'] == 'url':
            urls.append(message.text[e['offset']: e['offset'] + e['length']])
        elif e['type'] == 'text_link':
            urls.append(e['url'])
    if urls:
        return urls
    else:
        return None


# This function cleans the URL and returns only the website. "https://www.news.com/story.html --> news.com"
def clear_url(url):
    if '://' not in url:
        url = 'http://' + url
    return urlparse(url).netloc.replace('www.', '').replace('/', '')

    # Check if the URL is in our data set (AllSides) amd returns the source dictionary if it is.
    # Source dictionary is a set of URLs, for example:
    '''
    "news_source": "About.com",
    "allsides_url": "https:\/\/www.allsides.com\/node\/12909",
    "url": "usconservatives.about.com",
    "bias_rating": "2690"
    '''


def check_url_in_json(url, data_set):
    for source in data_set:
        source_url = clear_url(source['url'])
        if source_url in clear_url(url):
            return source
    return None


def link_analysis(scans, message, bot, urls, reply=False):
    try:
        chat_id = str(message.chat.id)
        if groups.get_chat_by_id(chat_id) is None:
            groups.new_chat(chat_id)

        mode_verbose = 'short' if (mode := groups.get_chat_mode(chat_id)) == 1 else "long"
        mute = groups.get_chat_mute(chat_id)
        bias = groups.get_chat_bias(chat_id)
        for url_scan in scans:
            if int(url_scan['category']) != 1:
                # If we found more than 1 positive piece of malware, delete the message and tell the channel.
                bot.delete_message(chat_id, message.message_id)
                bot.send_message(chat_id, messages['replies']['malware'][mode_verbose], parse_mode="Markdown",
                                 disable_web_page_preview=True)
                return

        if not int(mute):
            if int(bias):
                for url in urls:
                    allsides_response = check_url_in_json(url, allsides_json)
                    if allsides_response and not allsides_response['bias_rating'] == '2690':
                        # If a link was found in AllSides
                        side = side_dict[allsides_response['bias_rating']]
                        img_path = side['img']
                        bias_name = side['name']
                        allsides_url = side['link']
                        emoji = side['emoji']
                        if int(mode) == 0:
                            bot.send_photo(chat_id, open(f'{images_base_dir}{img_path}', 'rb'),
                                           caption=messages['replies']['rating_found'][mode_verbose].format(
                                               side=bias_name,
                                               allsides_url=allsides_url),
                                           parse_mode="Markdown", )
                        else:
                            bot.send_message(chat_id,
                                             messages['replies']['rating_found'][mode_verbose].format(emoji=emoji,
                                                                                                      side=bias_name,
                                                                                                      allsides_url=allsides_url),
                                             parse_mode="Markdown", disable_web_page_preview=True)
                    else:
                        # no info in allsides data set
                        bot.send_message(chat_id, messages['replies']['no_rating'][mode_verbose].format(url=url),
                                         parse_mode="Markdown", disable_web_page_preview=True)
            else:
                bot.send_message(chat_id, messages['replies']['no_malware'][mode_verbose], parse_mode="Markdown",
                                 disable_web_page_preview=True)

    except Exception:
        bot.send_message(message.chat.id, messages['something_wrong'], parse_mode="Markdown",
                         disable_web_page_preview=True)
        # What to say if something goes wrong.
        # Where to save the logs.
        logs = open('logs.txt', 'w+')
        logs.read()
        logs.write(datetime.now().__str__() + '----' + traceback.format_exc())
        logs.close()


def later_reply(urls, bot, message):
    while True:
        avira_response = avira.scan_url(urls)
        if avira_response['status_code'] != 200:
            time.sleep(15)
        elif avira_response['status_code'] == 200:
            break
    link_analysis(avira_response['scans'], message, bot, urls, reply=True)


# We store the API tokens in a seperate JSON file so they are easy to switch out.
# VirusTotal and Telegram both have API tokens
try:
    token = json.load(open('json/token.json', 'r'))
except FileNotFoundError:
    raise FileNotFoundError('No such file as token.json')
try:
    avira_token = token['avira_token']
except KeyError:
    raise KeyError('No Avira token specified')
try:
    bot_token = token['bot_token']
except KeyError:
    raise KeyError('No Telegram Bot token specified')
try:
    avira_url = token['avira_url']
except KeyError:
    raise KeyError('No Avira Url specified')

# This initializes the Virusl Total API object.
avira = Avira(url=avira_url, api_key=avira_token)

# This will parse the info from Settings.JSON
# This contains a list of announcements, replies, images we use, etc.
try:
    settings = json.load(open("json/settings.json", "r", encoding='utf-8', errors='ignore'))
except FileNotFoundError:
    raise FileNotFoundError('No such file as settings.json')
messages = settings['messages']
replies_commands = list(settings['messages'].keys())
images_base_dir = settings['images_base_dir']

# This will parse the AllSides JSON for now
allsides_json = json.load(open('json/allsides.json', 'r'))

# parse bias json
side_dict = json.load(open('json/bias.json', 'r', errors='ignore'))

# parse groups json
groups = Groups('json/groups.json')

# Initializes the Telegram Bot
bot = telebot.TeleBot(bot_token)


# /start and /help commands
# This is the starting message (which comes from settings.json)
# This also outputs the commands if someone types /help
# If we don't have a reply set, do nothing.


@bot.message_handler(commands=['help', 'start'])  # list of commands to handle
def send_welcome(message):
    """
        This function handles a list of commands in settings.json and returns a string.
    """
    # global groups_dict
    if groups.get_chat_by_id(message.chat.id) is not None:
        groups.new_chat(message.chat.id)

    for cmd in replies_commands:
        if cmd in message.text:
            text = messages[cmd]
            bot.reply_to(message, text)


# Handle every settings command in the list
@bot.channel_post_handler(commands=['settings'])
@bot.message_handler(commands=['settings'])
def command_handling(message):
    chat_id = message.chat.id
    args = message.text.split(' ')

    if message.from_user.id in [instance.user.id for instance in bot.get_chat_administrators(chat_id)]:

        if len(args) != 3:
            bot.send_message(chat_id, 'Looks like command is in wrong format.')
            return
        if args[1] not in ['short', 'mute', 'bias'] or args[2] not in ['on', 'off']:
            bot.send_message(chat_id, 'Looks like command is in wrong format.')
            return

        setting = args[1]
        state = 1 if args[2] == 'on' else 0

        if groups.get_chat_by_id(chat_id) is None:
            groups.new_chat(chat_id)

        bot.send_message(chat_id, messages['state_change_responses'][setting][str(state)][
            "negative" if groups.get_chat_setting_by_name(chat_id, setting) == state else "positive"])
        groups.set_chat_setting_by_name(chat_id, setting, state)

    else:
        bot.send_message(chat_id, messages['permission_denied'])


# This sends a welcome message to a new chat member.
# This comes from settings.json as well
@bot.message_handler(content_types=['new_chat_members'])
def send_wel(message: Message):
    bot.send_message(message.chat.id, messages['welcome'], parse_mode="Markdown", disable_web_page_preview=True)


# This is the main function that checks the URL.
@bot.channel_post_handler(content_types=['text'])
@bot.message_handler(content_types=['text'])
def url_handler(message: Message):
    try:
        chat_id = str(message.chat.id)
        urls = find_url(message)
        if urls:
            urls = urls if isinstance(urls, list) else [urls]
            avira_response = avira.scan_url(urls)
            if avira_response['status_code'] != 200:
                # retry in 1min
                bot.send_message(chat_id, "I'll reply later", parse_mode="Markdown",
                                 disable_web_page_preview=True)
                t = Timer(int(settings['retry_delay']), later_reply, args=(urls, bot, message), kwargs=None)
                t.start()
                return
            elif avira_response['status_code'] == 200:
                link_analysis(avira_response['scans'], message, bot, urls)
    except Exception:
        bot.send_message(message.chat.id, messages['something_wrong'], parse_mode="Markdown",
                         disable_web_page_preview=True)
        # What to say if something goes wrong.

        # Where to save the logs.
        with open('logs.txt', 'w+') as log:
            log.read()
            log.write(datetime.now().__str__() + '----' + traceback.format_exc())
            log.close()


# This starts the bot
bot.polling(none_stop=True, interval=0, timeout=20)
