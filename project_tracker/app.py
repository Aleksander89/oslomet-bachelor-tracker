import requests
import pickle
import os
from typing import List

from project_tracker.helpers import table_parser, email, utils

URL = 'https://www.cs.hioa.no/data/bachelorprosjekt/Prosjektforslag.php'
PROJECT_LIST_PATH = os.path.join(utils.get_project_root(), 'data', 'project_list.p')
Row = List[str]

def run() -> None:
    new_project_list = extract_project_list_from_url()

    if os.path.isfile(PROJECT_LIST_PATH):
        previous_project_list = load_project_list()
        number_of_new_items = len(new_project_list) - len(previous_project_list)
        if number_of_new_items > 0:
            #email.send_email(new_project_list, number_of_new_items)
            print('HEI!')
            
    save_project_list(new_project_list)

def extract_project_list_from_url() -> List[Row]:
    try:
        markup = requests.get(URL).text
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
        
    project_table = table_parser.parse_table(markup)
    project_list = table_parser.list_of_rows(project_table)
    return project_list

def save_project_list(project_list) -> None:
    pickle.dump(project_list, open(PROJECT_LIST_PATH, 'wb'))

def load_project_list() -> List[Row]:
    try:
        project_list = pickle.load((open(PROJECT_LIST_PATH, 'rb')))
    except IOError as err:
        raise SystemExit(err)

    return project_list