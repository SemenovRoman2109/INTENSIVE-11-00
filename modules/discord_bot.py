'''
    Модуль для роботи з Discord 

    У цьому файлі логіка нашого бота, його взаємодії з Discord сервером
'''
import discord
import dotenv, os
from .ai import get_response_from_ai, get_image, get_voice

# Загружаємо всі дані з .env файлу
dotenv.load_dotenv()

# Записуємо в змінну TOKEN значення токена
TOKEN = os.getenv("TOKEN")

# Використовуємо базові налаштування
intents = discord.Intents.default()
intents.message_content = True

# Створюємо об'єкт класу з налаштуваннями
bot_client = discord.Client(intents=intents)

@bot_client.event
async def on_ready():
    """
        Асинхронна функція, яка після запуску бота виводить у консоль, що бот запущений
    """
    print(f"Бот {bot_client.user} запущено")

@bot_client.event
async def on_message(message: discord.Message):
    """
	Ця асинхронна функція обробляє вхідне повідомлення і в залежності від нього викликає певні функції, такі як створення фото, озвучення тексту або відповідь від ШІ
    """
    # Частина коду, яка виводить помилку і не зупиняє код
    try:
        # Перевірка що повідомлення написав не цей бот
        if message.author != bot_client.user:
            # З повідомлення бере лише потрібний нам текст
            content = message.content
            # Дізнається id повідомленняна яке потрібно відповісти
            message_for_answer = await message.channel.fetch_message(message.id) 

            # Створюємо умову, що перевіряє, чи починається повідомлення із символів '!image'
            if content.startswith('!image'):
                # Створюємо змінну для асинхронної відповіді у вигляді гіфки заванатаження, під час генерування картинки
                load = await message_for_answer.reply('https://tenor.com/view/amalie-steiness-borregaard-loading-gif-loading-gif-25192894')
                # Отримуємо увесь інший запит після символів '!image'
                prompt = content[6:]
                # Створюємо  асинхронну відвоідь - згенеровану картинку за запитом
                response = await get_image(prompt = prompt)
                # В асинхронному режимі змінюємо гіфку завантаження на згенеровану картинку
                await load.edit(content=response) 
            elif content.startswith("!voice"):
                # З повідомлення виділяємо 
                text = content[6:]
                # Викликаємо функцію get_voice
                response = await get_voice(text = text)
                # Відповідає користувачу відповідь з аудіофайом
                await message_for_answer.reply(content= f"Ось звук який ви отримали:", file= discord.File(response, filename= "speech.mp3"))
            # Якщо не розпізнано як !voice та !image
            else:
                # Отримаємо відповідь ШІ 
                response = await get_response_from_ai(content)
                # Відправляє відповідь на повідомлення
                await message_for_answer.reply(response) 
    except:
        print("Error, message:", message)