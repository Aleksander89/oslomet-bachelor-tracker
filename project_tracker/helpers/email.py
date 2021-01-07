import configparser
import os
import smtplib
import ssl
import csv

from typing import List, Tuple
from .utils import get_project_root

ROOT_DIR = get_project_root()
CONFIG_PATH = os.path.join(ROOT_DIR, 'data', 'config.ini')
EMAIL_LIST_PATH = os.path.join(ROOT_DIR, 'data', 'email_list.csv')

def send_email(project_list, num_new_items) -> None:
    server, port = get_server_info_from_config()
    user, pw = get_credentials_from_config()

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(server, port, context=context) as server:
        server.login(user, pw)

        with open(EMAIL_LIST_PATH) as email_list:
            reader = csv.reader(email_list)
            next(reader)
            for name, email in reader:
                message = create_message(project_list, num_new_items).format(name)
                server.sendmail(user, email, message)

def get_server_info_from_config() -> Tuple[str, str]:
    config = read_config()
    server = config['gmail']['server']
    port = config['gmail']['port']

    return (server, port)

def get_credentials_from_config() -> Tuple[str, str]:
    config = read_config()
    user = config['gmail']['username']
    pw = config['gmail']['password']

    return (user, pw)

def read_config() -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    return config

def create_message(project_list: List, num_new_items: int) -> str:
    projects = ""

    for project in project_list[-num_new_items:]:
        projects += ' '.join(project)
        projects += '\n'

    message = 'Subject: ' + str(num_new_items) + ' nye bachelorprosjekter!\n\n' + \
    'Hei {},' + '\nDet er lagt ut ' + str(num_new_items) + ' nye bachelorprosjekter:\n\n' + projects + \
    '\nSjekk de ut her:' + \
    ' https://www.cs.hioa.no/data/bachelorprosjekt/Prosjektforslag.php' 

    # Hack to ignore non-ascii characters
    return ''.join([i if ord(i) < 128 else ' ' for i in message])

