# -*- coding: utf-8 -*-

import telebot
import requests

#DevMode
bot = telebot.TeleBot('your-token-from-FatherBot')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    #wrapping in try:except to catch unexpected errors, for example JSONDecodeError
    try:
        response = requests.get(
            'http://api.duckduckgo.com/',
            params={
                'q': message.text,
                'format': 'json'
            }).json()
        text = response.get('AbstractText')
        image_url = response.get('Image')
        related_topics_text = response.get('RelatedTopics')[0]['Text']
        related_topics_icon = response.get('RelatedTopics')[0]['Icon']['URL']
        related_topics_full_link = response.get('RelatedTopics')[0]['FirstURL']
    except:
        bot.send_message(message.from_user.id, "No results")
        return
    if not text:
        bot.send_message(message.from_user.id, related_topics_text)
        bot.send_message(message.from_user.id, related_topics_full_link)
        bot.send_photo(message.from_user.id, related_topics_icon)
    bot.send_message(message.from_user.id, text)
    bot.send_photo(message.from_user.id, image_url)


bot.polling(none_stop=True, interval=0)
