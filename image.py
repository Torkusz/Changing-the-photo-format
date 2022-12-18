# -*- coding: utf-8 -*-

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.exceptions import Throttled
from aiogram.types.message import ContentType
import aiogram.utils.markdown as fmt
import asyncio

import logging
from time import time
import datetime
import random
from random import randint
import re
import json
import requests
import numpy as np
import os
from PIL import Image
from api import *
import subprocess

def get_data():
	now = datetime.datetime.now()
	data = str(now.year) + "-" + str(now.month) + "-" + str(now.day) + " " + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second)
	return data

def link_user_mess(message):
	link = f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>"
	return link

bot = Bot(token=imag)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands = ["start"])
async def start(message: types.Message):
	await message.answer(f"{link_user_mess(message)}, привет!\nЭтот бот умеет менять формат фото", parse_mode="HTML")

@dp.message_handler(commands =("help", "помощь"))
async def help(message: types.Message):
	buttons = [
		types.InlineKeyboardButton(text="Связь", url="https://t.me/Torkusz"),
		types.InlineKeyboardButton(text="Проект на GitHub", url="https://github.com/Torkusz/Decryption_of_voiceMessages")
	]
	keyboard = types.InlineKeyboardMarkup(row_width=1)
	keyboard.add(*buttons)
	await message.answer("Этот бот умеет менять формат фото\n\nДержи ссылку для обратной связи и на проект", reply_markup=keyboard)

@dp.message_handler(content_types=ContentType.DOCUMENT)
async def check(message: types.Message):
	try:
		id = await bot.send_message(message.chat.id, f"Смотрю и рисую...")
		file_id = message.document.file_id
		file = await bot.get_file(file_id)
		file_path = file.file_path
		
		file_info = await bot.get_file(message.document.file_id)
		path = file_info.file_path
		fname = os.path.basename(path)

		await bot.download_file(file_path, fname)
		
		im = Image.open(fname)
		im.convert('RGB').save("image_name.jpg","JPEG")
		doc = open('image_name.jpg', 'rb')
		await message.reply_document(doc)
		
		os.remove(fname)
		os.remove('image_name.jpg')
		
	except Exception as e:
		await message.answer("Прошу прощения, но я не разобрал картину...")
		print(e)
	

if __name__ == "__main__":
	loop = asyncio.get_event_loop()
	executor.start_polling(dp, skip_updates=False)