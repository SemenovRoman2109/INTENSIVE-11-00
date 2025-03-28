'''
    Модуль для роботи з API OpenAI

    У цьому файлі логіка нашого бота, взаємодії бота з сервером OpenAI. Для формування відповіді від штучного інтелекта 
'''
import openai
import dotenv, os
import io
import random

list_voices = ['alloy', 'ash', 'coral', 'echo', 'fable', 'onyx', 'nova', 'sage', 'shimmer']
# Загружаємо всі дані з .env файлу
dotenv.load_dotenv()
OPENAI_SECRET_KEY = os.getenv("OPENAI_SECRET_KEY")

# Створюємо асинхронний об'єкт для openAi
client_openai = openai.AsyncOpenAI(api_key = OPENAI_SECRET_KEY)


async def get_response_from_ai(question: str):
    """
    функція яка отримує відповідь від штучного інтелекту за допомогою моделі gpt-4o-mini, яка навчена нашою інформауією
    """
    response = await client_openai.chat.completions.create(
        model = "ft:gpt-4o-mini-2024-07-18:worldit::BFf7bJwz", # Використовуємо нашу навчену модель
        messages = [{
            "role": "user", # Ставимо роль звичайного користувача
            "content": question, # Ставимо щоб на вхід було питання
        }],
    )
    # Повертаємо відповідь на питання яке ми задали штучному інтелекту
    return response.choices[0].message.content 


async def get_image(prompt: str):
    """
    Створюємо асинхронну функцію котра генерує зображення за даними користувача
    """ 
    response = await client_openai.images.generate(
        model= "dall-e-2", #  Вказуємо модель генерації
        prompt= prompt, #  Те що буде генерувати
        size= "1024x1024", # Розміри зображення
        quality="standard" #  Якість зображення
    )
    # Отримуємо посилання на зображення
    return response.data[0].url 


async def get_voice(text: str):
    """
        Ця функція повертає аудіо файл с озвученим текстом
    """
    # Отримуємо рандомний голос зі списку list_voices
    speeker = random.choice(list_voices)
    # відповідь від ШІ 
    response = await client_openai.audio.speech.create(
        model = "gpt-4o-mini-tts", # Версія моделі яка буде озвучувати текст
        voice= speeker, # голос яким буде озвучуватись текст
        input = text # той текст який потрібно озвучити
    )
    print(speeker, '- read your text')
    # перетворюємо звук з байт-коду у звук 
    audio_file = io.BytesIO(response.content)
    # повертаємо цей звук
    return audio_file