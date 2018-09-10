import aiohttp
import asyncio
import json
import logging

import markovify
from aiotg import Bot, Chat


def run(config):
    logging.info('start reading model file')
    bot = Bot(api_token=config.token, proxy=config.proxy['proxy_url'])

    @bot.command(r"/start")
    def start(chat: Chat, match):
        keyboard = {
            "keyboard": [['Два чая, этому господину']],
            "resize_keyboard": True
        }
        return chat.send_text("В основе меня лежат цепи маркова, а обучен я на фанфиках, книгах по "
                              "программированию и ветхом завете. \n"
                              "Можешь попробовать поговорить со мной.\n"
                              "На любую вашу фразу я отвечу каким-то бредом.",
                              reply_markup=json.dumps(keyboard))

    @bot.default
    async def answerer(chat, message):
        async with aiohttp.ClientSession() as session:
            r = session.post(f'{config.api_uri}/phrase', json={'phrase': ''})
            answer = (await r.json())['answer']

        logging.info(f"{chat.sender}, {message}: {answer}")
        return chat.reply(answer)

    channel = bot.channel(config.chanel)

    async def chanel_posting():
        while True:
            async with aiohttp.ClientSession() as session:
                r = session.post(f'{config.api_uri}/phrase', json={'phrase': ''})
                answer = (await r.json())['answer']

            await channel.send_text(answer)
            await asyncio.sleep(60 * config.interval)

    loop = asyncio.get_event_loop()

    bot_loop = loop.create_task(bot.loop())
    chanel_loop = loop.create_task(chanel_posting())
    loop.run_until_complete(asyncio.gather(bot_loop, chanel_loop))
    loop.close()
