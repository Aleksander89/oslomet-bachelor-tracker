import configparser
import os
from .utils import get_project_root

ROOT_DIR = get_project_root()
CONFIG_PATH = os.path.join(ROOT_DIR, 'data', 'config.ini')

config = configparser.ConfigParser()
config.read(CONFIG_PATH)


def send_email(project_list, num_new_items):
    pass
