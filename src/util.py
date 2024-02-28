import os
import logging

base_dir = os.path.dirname(__file__).replace('src', '')
src_dir = os.path.dirname(__file__)
data_dir = os.path.join(base_dir, 'data')
log_dir = os.path.join(base_dir, 'log')

KTU_URL = 'https://ktu.edu.in'
ANNOUNCEMENT_URL = 'https://ktu.edu.in/menu/announcements'

API_KEY = os.getenv('TELEGRAM_BOT_KEY')


def load_data(file_name: str = 'announcements.json'):
    return os.path.join(data_dir, file_name)

def load_log(file_name: str = 'application.log'):
    return os.path.join(log_dir, file_name)

logger = logging.getLogger('ktu_notifier')
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(load_log())
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
