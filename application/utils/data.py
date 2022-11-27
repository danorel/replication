import csv
import logging
import random

DATASET_PATH = './data/titanic.csv'


def get_random_record() -> dict:
    with open(DATASET_PATH, newline='') as csv_file:
        reader = csv.reader(csv_file)
        random_row = random.choice(list(reader))
        return {
            'PassengerId': int(random_row[0] or 0),
            'Survived': int(random_row[1] or 0),
            'Pclass': int(random_row[2] or 0),
            'Name': str(random_row[3] or ""),
            'Sex': str(random_row[4] or ""),
            'Age': int(random_row[5] or 0),
            'Ticket': str(random_row[8] or "")
        }
