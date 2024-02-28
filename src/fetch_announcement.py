import requests
from bs4 import BeautifulSoup
import re
from util import ANNOUNCEMENT_URL, load_data, logger
import hashlib
import sqlite3
import traceback

class FetchAnnouncement:
    def __init__(self) -> None:
        self.announcement_hash = self.__get_hash()


    def hash_announcement(self, announcement: str):
        diagest = hashlib.sha256()
        diagest.update(str(announcement).encode('UTF-8'))

        return diagest.hexdigest()

    def latest_announcement(self):
        r = requests.get(ANNOUNCEMENT_URL)
        soup = BeautifulSoup(r.text, 'html.parser')
        announcement_list = []
        updated_hash = ''
        updated_heading = ''
        try:
            container = soup.select('table', {'class': 'ktu-news'})[0]
            announcements = container.find_all('tr')
        except IndexError as e:
            logger.info(f'error {e}')
            announcements = []

        try:
            for announcement in announcements:
                announcement_date = announcement.find('label').text
                heading = announcement.find('td').find_next_sibling().find('li').b.text
                hash = self.hash_announcement(heading)

                if self.announcement_hash != hash:
                    desc = announcement.find('td').find_next_sibling().find('li')
                    annnouncement_links = {}

                    try:
                        for link in desc.find_all('a'):
                            text = link.text
                            try:
                                href = link.attrs['href']
                            except KeyError as e:
                                href = None
                            annnouncement_links[text] = href
                    except AttributeError as e:
                        logger.info(traceback.format_exc())

                    link_text_pattern = re.compile('|'.join([i.text for i in desc.find_all('a')]))
                    annnouncement_text = link_text_pattern.sub('', desc.text)
                    annnouncement_text = re.sub('\n', '', annnouncement_text)
                    annnouncement_obj = {
                        'date': announcement_date,
                        'description': annnouncement_text,
                        'link_details': annnouncement_links
                    }
                    announcement_list.append(annnouncement_obj)
                    updated_hash = hash
                    updated_heading = heading
                else:
                    logger.info(f'matching hash found: {announcement}')
                    logger.info(f'Before: self.announcement_hash: {self.announcement_hash}')
                    logger.info(f'updated_heading: {updated_heading}')
                    logger.info(f'updated_hash: {updated_hash}')
                    logger.info(f'hash: {hash}')
                    logger.info(f'heading: {heading}')
                    self.announcement_hash = updated_hash
                    logger.info(f'After: self.announcement_hash: {self.announcement_hash}')
                    self.__update_hash(updated_heading, updated_hash)
                    return announcement_list
        except AttributeError as e:
            logger.info(f'error {e}')
            logger.info(traceback.format_exc())
        logger.info('No announcements')
        return announcement_list

    def __get_hash(self):
        try:
            db_con = sqlite3.connect(load_data('announcement.db'))
            db_cur = db_con.cursor()
            hash = db_cur.execute('SELECT hash FROM latest_announcement_hash').fetchone()[0]
            db_con.close()
            return hash
        except Exception as e:
            logger.info(traceback.format_exc())

    def __update_hash(self, title: str, hash: str):
        logger.info(f'Updating the hash with heading {title} and hash: {hash}')
        try:
            db_con = sqlite3.connect(load_data('announcement.db'))
            db_cur = db_con.cursor()
            db_cur.execute(f"UPDATE latest_announcement_hash SET title = '{title}', hash='{hash}' WHERE id=1")
            db_con.commit()
            db_con.close()
        except Exception as e:
            logger.info(traceback.format_exc())
