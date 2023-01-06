import asyncio
import telegram
from telebot.credentials import TOKEN


async def main():
    bot = telegram.Bot(TOKEN)
    async with bot:
        # print(await bot.get_me())
        print((await bot.get_updates())[0])

if __name__ == '__main__':
    asyncio.run(main())
