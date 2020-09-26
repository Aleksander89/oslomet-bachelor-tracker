from bs4 import BeautifulSoup
from typing import List

Row = List[str]

def list_of_rows(table: BeautifulSoup) -> List[Row]:
    rows = table.find_all('tr')
    data = []
    for row in rows:
        cols = row.find_all('td')
        cols = [col.text.strip() for col in cols]
        if len(cols) > 0:
            data.append(cols)
    
    return data

def parse_table(markup: BeautifulSoup) -> BeautifulSoup:
    soup = BeautifulSoup(markup, features='html.parser')
    project_table = soup.find(class_='studentTabell')
    return project_table

