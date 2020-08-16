import requests
import time
import json
import os
from pprint import pprint

class TelegramBot:
    def __init__(self):
        self.env = json.load(open('env.json'))

        self.bot_name = self.env['bot_name']
        self.bot_username = self.env['bot_name']        
        token = self.env['bot_token']
        self.url_base = f'https://api.telegram.org/bot{token}'

    def InitBot(self):
        update_id = None
        while True:
            update = self.GetMessages(update_id)
            messages = update['result']
            if messages:
                for message in messages:
                  message_data = message['message'] if 'message' in message else message['edited_message']
                  update_id = message['update_id']
                  chat_id = message_data['from']['id']
                  is_first_chat = message_data['message_id'] == 1
                  reply_message = self.CreateMessageReply(message, is_first_chat)
                  self.Reply(reply_message, chat_id)

    def dd(self, data):
        pprint(data)
        exit()

    def GetMessages(self, update_id):
        request_link = f'{self.url_base}/getUpdates?timeout=100'
        if update_id:
            request_link = f'{request_link}&offset={update_id + 1}'
        result = requests.get(request_link)
        return json.loads(result.content)

    def CreateMessageReply(self, message, is_first_chat):
      message_data = message['message'] if 'message' in message else message['edited_message']
      name = message_data['from']['first_name']
      if 'text' in message_data:
        message_text = message_data['text']
        message_text = message_text.lower()
        if is_first_chat == True or message_text == '/menu' or message_text == 'menu' or message_text == 'm':
          regards = f"Olá {name}, {os.linesep}Seja bem-vindo ao {self.bot_name}.{os.linesep}"
          options = f"1 - Cheese Burger Duplo{os.linesep}2 - Duplo Bacon{os.linesep}3 - X Egg"
          return f''' {regards} Digite o número do item que deseja pedir:{os.linesep}{options}'''
        if message_text == '1':
          return f"1 - Cheese Burger Duplo - R$ 7.50 {os.linesep}Confirmar pedido?{os.linesep} Envie 's' ou 'sim' para /confirmar |{os.linesep}Ver /menu"
        if message_text == '2':
          return f"2 - Duplo Bacon - R$ 9.50 {os.linesep}Confirmar pedido?{os.linesep} Envie 's' ou 'sim' para /confirmar |{os.linesep}Ver /menu"
        if message_text == '3':
          return f"3 - X Egg - R$ 8.50 {os.linesep}Confirmar pedido?{os.linesep} Envie 's' ou 'sim' para /confirmar |{os.linesep}Ver /menu"
        if message_text in ('s', 'sim', '/confirmar'):
          return f"Pedido confirmado!"
        else:
          return f"Gostaria de acessar o menu?{os.linesep}Você pode clicar em /menu ou digitar 'm' ou 'menu'"
      else:
        return f"Gostaria de acessar o menu?{os.linesep}Você pode clicar em /menu ou digitar 'm' ou 'menu'"

    def Reply(self, reply_message, chat_id):
        send_url = f'{self.url_base}/sendMessage?chat_id={chat_id}&text={reply_message}'
        requests.get(send_url)


bot = TelegramBot()
bot.InitBot()

