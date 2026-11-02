#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import logging
import telegram
from telegram.error import NetworkError, Unauthorized
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply
from time import sleep
import os
from time import time
import json
import csv 
import datetime

logging.basicConfig(
  format="%(asctime)s %(levelname)-8s %(message)s",
  level=logging.INFO,
  datefmt="%Y-%m-%d %H:%M:%S", 
)

try:
  BOT_TOKEN = "5448355125:AAGzYFw-6FPW8spTld4AframD0uZA49_aaw"
except KeyError:
  logging.error("Bot credentials not found in environment")

# How long the container exist
LIFESPAN = 240


def main():
  """Run the bot."""

  try:
    update_id = 1
  except:
    update_id = 0

  start_time = int(time())

  bot = telegram.Bot(BOT_TOKEN)

  runtime_logger = {"By": "", "Category": "", "Amount": 0, "Date": 0}
  day_logger = {}

  while True:
    try:
      for update in bot.get_updates(offset=update_id, timeout=10):
        update_id = update.update_id + 1
        logging.info(f"Update ID:{update_id}")
        entry(bot, update, runtime_logger, day_logger)
    except NetworkError:
      sleep(1)
    except Unauthorized:
      # The user has removed or blocked the bot.
      update_id += 1
    if int(time()) - start_time > LIFESPAN:
      logging.info("Enough for the day! Passing on to next Meeseek")
      with open("/tmp/update_id", "w") as the_file:
        the_file.write(str(update_id))
      break


def entry(bot, update, runtime_logger, day_logger):

  """if update.callback_query:

    data = update.callback_query.data 
    day_logger[data] = "INPROGRESS"
    force = ForceReply(input_field_placeholder=f"Enter {camelize(data)}")
 
    bot.send_message(
      reply_to_message_id=update.callback_query.message.reply_to_message.message_id,
      chat_id = update.callback_query.message.chat.id,
      text=f"Enter {camelize(data)}"
      #reply_markup=force
    )

    del runtime_logger[data]
  """
  if update.message:
    data = update.message.text
    logging.info(f"Update ID:{data}")
    """for key in day_logger:
      if day_logger[key] == "INPROGRESS":
        day_logger[key] = data
    """
    if update.message.text == "/done":
      with open("data.csv", "a", encoding="utf-8") as datafile:
        csvfile = csv.writer(datafile, delimiter=",")
        csvfile.writerow([
          day_logger['By'],
          day_logger['Category'],
          day_logger['Amount'],
          day_logger['Date'],
          datetime.date.today().strftime("%d/%m/%Y")
        ])
        
      
    if update.message.text == "/add":
      """button_list = []
      for key in runtime_logger:
        button_list.append(
          InlineKeyboardButton(camelize(key), callback_data=key)
        )
      """
      reply_markup = "Add in the following format: 'Spender, Amount, Category, Date'. Type /done once done"#InlineKeyboardMarkup(build_menu(button_list, n_cols=4))

      bot.send_message(
        chat_id=update.message.chat.id,
        text="Add in the following format: 'Spender, Amount, Category, Date'",
        reply_to_message_id=update.message.message_id
      )
    else:
      expenses = ""
      bot.send_message(
        chat_id=update.message.chat.id,
        text=f"Entered: {expenses}. Want to restart? Type /add. Else type /done",
      )
      runtime_logger['By'] = 0
      runtime_logger['Category'] = 0
      runtime_logger['Amount'] = 0
      runtime_logger['Date'] = ''
      day_logger = {}

def camelize(label):
  words = label.split("_")
  name = ""
  for word in words:
    name = name + " " + word[0].upper() + word[1:].lower()
  return name
      
def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
  menu = [buttons[i : i + n_cols] for i in range(0, len(buttons), n_cols)]
  if header_buttons:
    menu.insert(0, [header_buttons])
  if footer_buttons:
    menu.append([footer_buttons])

  return menu

if __name__ == "__main__":
  main() 
