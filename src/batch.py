from fetch_announcement import FetchAnnouncement
import time
from util import logger, load_data, API_KEY
from bot import Bot
import sqlite3
import messages
import re

class Batch:

    def __init__(self) -> None:
        self.bot = Bot(API_KEY)

    def send_announcement(self, announcement: str):
        announcement = re.sub(r"\n|\r\n", "", announcement)
        logger.info('New announcement')
        db_con = sqlite3.connect(load_data('announcement.db'))
        db_cur = db_con.cursor()
        chat_ids = db_cur.execute('SELECT chat_id FROM subscribers').fetchall()
        for chat_id in chat_ids:
            message = messages.announcement_message.format(announcement)
            self.bot.sendMessage({
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'HTML'
            })
            logger.info(f'Announcement sent for {chat_id}')

    def run(self):
        fetach_announcement = FetchAnnouncement()
        announcements = fetach_announcement.latest_announcement()
        for announcement in announcements:
            self.send_announcement(announcement['description'])

if __name__ == '__main__':
    batch = Batch()
    while True:
        logger.info('Checking new announcement')
        batch.run()
        time.sleep(30)
