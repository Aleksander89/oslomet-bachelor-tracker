import requests, pickle
from project_tracker.data import parser

URL = 'https://www.cs.hioa.no/data/bachelorprosjekt/Prosjektforslag.php'

def run():
    markup = requests.get(URL).text
    project_table = parser.parse_table(markup)
    project_list = parser.list_of_rows(project_table)

    print(project_list)