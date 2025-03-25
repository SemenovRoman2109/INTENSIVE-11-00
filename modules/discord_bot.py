'''
    Модуль для роботи з Discord 

    У цьому файлі логіка нашого бота, його взаємодії з Discord сервером
'''
import discord
import dotenv, os

dotenv.load_dotenv()

TOKEN = os.getenv("TOKEN")


intents = discord.Intents.default()
intents.message_content = True

bot_client = discord.Client(intents= intents)

@bot_client.event
async def on_ready():
    print(f"Бот {bot_client.user} запущено")

@bot_client.event
async def on_message(message):
    try:
        if message.author != bot_client.user:
            content = message.content
            await message.channel.send(content)
    except:
        print("error")