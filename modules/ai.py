'''
    Модуль для роботи з API OpenAI

    У цьому файлі логіка нашого бота, взаємодії бота з сервером OpenAI. Для формування відповіді від штучного інтелекта 
'''
import openai
import dotenv, os

#
dotenv.load_dotenv()
OPENAI_SECRET_KEY = os.getenv("OPENAI_SECRET_KEY")

#
client_openai = openai.AsyncOpenAI(api_key = OPENAI_SECRET_KEY)

# 
async def get_response_from_ai(question: str):
    # 
    response = await client_openai.chat.completions.create(
        model = "gpt-4o-mini", #
        messages = [{
            "role": "user", #
            "content": question, #
        }],
    )
    # 
    return response.choices[0].message.content