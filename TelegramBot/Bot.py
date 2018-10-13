import time
from TelegramBot import Parser
from TelegramBot.Proxy import getProxy
from TelegramBot.Requests import Request


class TelegramBot:
    def __init__(self):
        self.blank = True
        self.token = '534432525:AAFwQpKXRWMtQ8AD8vAAfZ04lqdhJXaPWv0'
        self.url = 'https://api.telegram.org/bot{}/'.format(self.token)
        self.proxies = getProxy()
        self.chat_id = []

    def getMessage(self):
        """ Функция возвращает последние сообщение и id чата. """
        try:
            url = self.url + "getupdates"
            data = Request(url, self.proxies).getHtml()
            last_object = data['result'][-1]
            chat_id = last_object['message']['chat']['id']
            text = last_object['message']['text']
            message = {'chat_id': chat_id,
                       'text': text}
            return message
        except:
            self.blank = False
            message = {'chat_id': '',
                       'text': ''}
            return message

    def sendMessage(self):
        """ Функция отправляет сообщение. """
        for id in self.chat_id:
            text_id = self.getText(id)
            if text_id != 'stop':
                name_coin = self.getText(id)
                text = Parser.getData(name_coin)
                url = self.url + 'sendmessage?chat_id={}&text={}'.format(id, text)
                Request(url, self.proxies).getHtml()
                time.sleep(10)
            else:
                self.chat_id.pop(self.chat_id.index(id))

    def getText(self, id):
        """ Функция возвращает текст сообщения от пользователя. """
        index = -1
        url = self.url + "getupdates"
        data = Request(url, self.proxies).getHtml()
        while self.blank:
            last_id = data['result'][index]['message']['chat']['id']
            if last_id == id:
                text = data['result'][index]['message']['text']
                return text
            else: index -= 1

    def main(self):
        message = self.getMessage()
        id = message['chat_id']
        self.chat_id.append(id)
        while True:
            message = self.getMessage()
            if self.blank:
                new_id = message['chat_id']
                if new_id != id: self.chat_id.append(new_id)
                self.sendMessage()


if __name__ == '__main__':
    Bot = TelegramBot()
    Bot.main()
