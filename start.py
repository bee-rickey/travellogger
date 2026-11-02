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

  data = []

  while True:
    try:
      for update in bot.get_updates(offset=update_id, timeout=10):
        update_id = update.update_id + 1
        logging.info(f"Update ID:{update_id}")
        entry(bot, update, data)
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


def entry(bot, update, data):
  if update.message:    
    if update.message.text == "/done":
      with open("data.csv", "a", encoding="utf-8") as datafile:
        csvfile = csv.writer(datafile, delimiter=",")
        for item in data:
          csvfile.writerow([
            item
          ])
        
    if update.message.text == "/add":
      bot.send_message(
        chat_id=update.message.chat.id,
        text="Add in the following format: 'Spender, Amount, Category, Date. Type /done once done'",
        reply_to_message_id=update.message.message_id
      )
      
    else:
      data += update.message.text.splitlines()
      logging.info(f"Update ID:{data}")
      bot.send_message(
        chat_id=update.message.chat.id,
        text=f"You Entered: {data}. Want to restart? Type /add. Else type /done",
      )

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
