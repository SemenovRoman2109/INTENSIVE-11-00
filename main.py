'''
    Головний модуль запуску Dicord бота
'''

from modules import bot_client, TOKEN

def main():
    # 
    bot_client.run(TOKEN)
# 
if __name__ == '__main__':
    main()