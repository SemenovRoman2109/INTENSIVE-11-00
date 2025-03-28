'''
    Модуль для роботи з API OpenAI

    У цьому файлі логіка нашого бота, взаємодії бота з сервером OpenAI. Для формування відповіді від штучного інтелекта 
'''
import openai
import dotenv, os
import io
import random

list_voices = ['alloy', 'ash', 'coral', 'echo', 'fable', 'onyx', 'nova', 'sage', 'shimmer']
#
dotenv.load_dotenv()
OPENAI_SECRET_KEY = os.getenv("OPENAI_SECRET_KEY")

#
client_openai = openai.AsyncOpenAI(api_key = OPENAI_SECRET_KEY)

# 
async def get_response_from_ai(question: str):
    # 
    response = await client_openai.chat.completions.create(
        model = "ft:gpt-4o-mini-2024-07-18:worldit::BFf7bJwz", #
        messages = [{
            "role": "user", #
            "content": question, #
        }],
    )
    # 
    return response.choices[0].message.content


async def get_image(prompt: str):
    response = await client_openai.images.generate(
        model= "dall-e-2",
        prompt= prompt,
        size= "1024x1024",
        quality="standard"
    )

    return response.data[0].url


async def get_voice(text: str):
    speeker = random.choice(list_voices)
    response = await client_openai.audio.speech.create(
        model = "gpt-4o-mini-tts",
        voice= speeker,
        input = text
    )
    print(speeker, '- read your text')
    
    audio_file = io.BytesIO(response.content)
    return audio_file