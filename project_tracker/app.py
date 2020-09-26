import requests
import pickle
import os.path
from project_tracker.helpers import table_parser

URL = 'https://www.cs.hioa.no/data/bachelorprosjekt/Prosjektforslag.php'
PROJECT_LIST = 'project_list.p'

def run():
    new_project_list = extract_project_list_from_url()
    if os.path.isfile(PROJECT_LIST):
        previous_project_list = load_project_list()
        number_of_new_items = len(new_project_list) - len(previous_project_list)
        if number_of_new_items > 0:
            send_email(new_project_list, number_of_new_items)
    else:
        save_project_list(new_project_list)

def extract_project_list_from_url():
    try:
        markup = requests.get(URL).text
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
        
    project_table = table_parser.parse_table(markup)
    project_list = table_parser.list_of_rows(project_table)
    return project_list

def save_project_list(project_list):
    pickle.dump(project_list, open(PROJECT_LIST, 'wb'))

def load_project_list():
    try:
        project_list = pickle.load((open(PROJECT_LIST, 'rb')))
    except IOError as err:
        raise SystemExit(err)

    return project_list

def send_email(project_list, num_new_items):
    pass
