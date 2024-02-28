from bot import Bot
from util import API_KEY, logger
import traceback
from util import load_data
import sqlite3
import messages

class KtuNotifier(Bot):

    def __init__(self, api_key) -> None:
        super().__init__(api_key)
        self.createCommands([
            {
            'command': 'subscribe',
            'description': 'Get latest notification'
            },
            {
                'command': 'unsubscribe',
                'description': 'Unscribe from latest notifications'
            },
            {
                'command': 'help',
                'description': 'See all available commands'
            }
        ])

    def check_new_announcements(self):
        pass

    def onboarding_greetings(self):
        text = messages.styled_greeting
        message = self.prepare_message(message=text)
        self.sendMessage(message)
        logger.info('Message sent')

    def subscribe_announcement(self):
        con = sqlite3.connect(load_data('announcement.db'))
        try:
            cur = con.cursor()
            cur.execute(f'INSERT INTO subscribers(chat_id) VALUES({self.chat_id})')
            con.commit()
            logger.info('Subscribed for notification')
            con.close()
        except sqlite3.IntegrityError as e:
            logger.info('Already subscribed')

        text = messages.subscription_greeting
        message = self.prepare_message(text)
        self.sendMessage(message)
        logger.info('Subscription message sent')

    def unsubscribe_announcement(self):
        con = sqlite3.connect(load_data('announcement.db'))
        try:
            cur = con.cursor()
            cur.execute(f'DELETE FROM subscribers WHERE chat_id={self.chat_id}')
            con.commit()
            logger.info('Unsubscribed for notification')
            con.close()
        except Exception as e:
            logger.info('Something went wrong')

        text = messages.unsubscription_message
        message = self.prepare_message(text)
        self.sendMessage(message)
        logger.info('Unsubscription message sent')

    def help_command(self):
        text = messages.help_message
        message = self.prepare_message(text)
        self.sendMessage(message)
        logger.info('Help message sent')

    def start_bot(self):
        self.getUpdates()
        while True:
            update =  self.get_latest_update()
            if update and self.is_bot_command:
                match self.get_text():
                    case '/start':
                        self.onboarding_greetings()
                    case '/subscribe':
                        self.subscribe_announcement()
                    case '/unsubscribe':
                        self.unsubscribe_announcement()
                    case '/help':
                        self.help_command()
                    case _ :
                        logger.info('Unknown command')

    @staticmethod
    def sendAnnouncement(self):
        pass


logger.info('Application started')
ktuNotifierBot = KtuNotifier(API_KEY)

try:
    ktuNotifierBot.start_bot()
except (Exception, KeyboardInterrupt) as e:
    logger.error(traceback.format_exc())
    print('Bot server stoped')
