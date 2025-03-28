'''
    Модуль для роботи з Discord 

    У цьому файлі логіка нашого бота, його взаємодії з Discord сервером
'''
import discord
import dotenv, os
from .ai import get_response_from_ai, get_image, get_voice

dotenv.load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot_client = discord.Client(intents= intents)

@bot_client.event
async def on_ready():
    print(f"Бот {bot_client.user} запущено")

@bot_client.event
async def on_message(message: discord.Message):
    try:
        if message.author != bot_client.user:
            content = message.content
            message_for_answer = await message.channel.fetch_message(message.id)

            if content.startswith('!image'):
                load = await message_for_answer.reply('https://tenor.com/view/amalie-steiness-borregaard-loading-gif-loading-gif-25192894')
                prompt = content[6:]
                response = await get_image(prompt = prompt)
                await load.edit(content=response)
            elif content.startswith("!voice"):
                text = content[6:]
                response = await get_voice(text = text)
                await message_for_answer.reply(content= f"Ось звук який ви отримали:", file= discord.File(response, filename= "speech.mp3"))
            else:
                response = await get_response_from_ai(content)
                await message_for_answer.reply(response)
    except:
        print("Error, message:", message)