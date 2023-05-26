"""Configuring data"""

import ast


SUBJECT_DATA = {}


with open('./data/subject_data', 'r') as f:
    subject = ast.literal_eval(f.read())


def save_all() -> None:
    with open('./data/subject_data', 'w') as file:
        file.write(repr(subject))
