import requests
import os
import json
from util import logger

class Bot:

    def __init__(self, api_key) -> None:
        self.base_url = 'https://api.telegram.org/bot' + api_key
        self.update = None
        self.updates = None
        self.latest_update_id = None
        self.__api_response = {}

    def getUpdates(self) ->  dict:
        url = os.path.join(self.base_url, 'getUpdates')
        r = requests.get(url)
        self.__api_response =  r.json()
        if self.is_succes and self.is_result_present:
            self.latest_update_id = self.__result[-1]['update_id']

    def get_latest_update(self):
        params = {'offset': self.latest_update_id}
        url = os.path.join(self.base_url, 'getUpdates')
        r = requests.get(url=url, params=params)
        self.__api_response =  r.json()
        if self.is_succes and self.is_result_present:
            self.update = self.__result[0]
            self.latest_update_id = self.update['update_id'] + 1
            return True
        else:
            self.update = None
            return False

    def sendMessage(self, message: dict):
        url = os.path.join(self.base_url, 'sendMessage')
        r = requests.post(url=url, data=message)

    def get_message_from_upadate(self):
        try:
            self.update['message']
        except KeyError as e:
            pass

    def prepare_message(self, message: str):
        return {
            'chat_id': self.chat_id,
            'text': message,
            'parse_mode': 'HTML'
        }

    def createCommands(self, commands: list[dict]):
        url = os.path.join(self.base_url, 'setMyCommands')
        data = {
            'commands': json.dumps(commands),
            'language_code': 'en'
        }
        r = requests.post(url=url, data=data)
        self.__api_response =  r.json()
        if self.is_succes and self.__result:
            logger.info(f'Command created: {self.__api_response}')
        else:
            logger.info(f'Failed to create command due to {self.__api_response["description"]}')

    def createCommand(self, command: dict):
        self.createCommands(commands=[command])

    @property
    def __result(self):
        try:
            return self.__api_response['result']
        except KeyError as e:
            pass

    @property
    def type(self, update: dict = {}):
        try:
            return self.update['message']['entities'][0]['type']
        except KeyError as e:
            return None

    @property
    def is_bot_command(self):
        return True if self.type == 'bot_command' else False

    def get_text(self):
        try:
            return self.update['message']['text']
        except KeyError as e:
            pass

    @property
    def is_succes(self) -> bool:
        try:
            return self.__api_response['ok']
        except KeyError as e:
            return False

    @property
    def chat_id(self):
        try:
            return self.update['message']['chat']['id']
        except KeyError as e:
            return None

    @property
    def is_result_present(self):
        if 'result' in self.__api_response and len(self.__api_response['result']) > 0:
            return True
        else:
            return False


