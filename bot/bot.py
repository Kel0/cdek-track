import sys

sys.path = ["", ".."] + sys.path[1:]  # noqa: F841


import jsonmodule.jsonimporter  # noqa: F841
from aiogram import Bot, Dispatcher, executor, types

import bot.Resources.bot as bot_creds
from tracker.cookie_graber import graber
from tracker.tracker import Tracker

API_TOKEN = bot_creds.raw_data["API_TOKEN"]

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot=bot)


@dp.message_handler(text_contains=["track"])
async def send_track(message: types.Message):
    try:
        track_info_dict = Tracker(track_code=message.text).track()

        track_info = (
            f"From: {track_info_dict['js']['Content']['cityFrom']['name']} \n"
            f"To: {track_info_dict['js']['Content']['cityTo']['name']}\n"
            f"Status: {track_info_dict['js']['Content']['status']['name']}\n"
            f"Tel. 1: {track_info_dict['js']['Content']['receiverStockPhone'][0]['phoneNumber']}\n"
            f"Tel. 2: {track_info_dict['js']['Content']['receiverStockPhone'][1]['phoneNumber']}\n\n"
        )

        for data in track_info_dict["js"]["Content"]["trackingDetails"]:
            track_info += f"{data['date']}\n"
            track_info += f"{data['statusName']} | {data['cityName']}\n\n"

    except Exception as e:
        track_info = e
        if track_info == "'Content'":
            track_info = "Order not found"

    await message.reply(track_info, reply=False)


@dp.message_handler(commands=["cookie"])
async def generate_cookie(message: types.Message):
    cookies = graber.Record.store_cookie()
    await message.reply(f"New cookies: {cookies}", reply=False)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
