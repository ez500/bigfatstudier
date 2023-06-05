"""Configuring data"""

import ast
from dataclasses import dataclass, asdict


@dataclass
class Work:
    name: str
    description: str
    due_date: str

    def to_dict(self):
        return {k: str(v) for k, v in asdict(self).items()}


SUBJECT_DATA = {'real': '',
                'alias': [],
                'description': 'No description',
                'homework': [],
                'project': [],
                'test': [], }

MESSAGE_DATA = {'emoji': [],
                'role': [], }

with open('./data/subject_data', 'r') as f:
    subject = ast.literal_eval(f.read())
with open('./data/message_data', 'r', encoding='utf-8') as f:
    message_listener = ast.literal_eval(f.read())


def save_all() -> None:
    with open('./data/subject_data', 'w') as file:
        file.write(repr(subject))
    with open('./data/message_data', 'w', encoding='utf-8') as file:
        file.write(repr(message_listener))


def _generate_default_data(data: dict, default: dict):
    for key, value in default.items():
        if isinstance(value, dict):
            if key not in data:
                data[key] = {}
            _generate_default_data(data[key], value)
        if key not in data:
            data[key] = value


def subject_generate_default_data(subject_name: str):
    if subject_name.lower() not in subject:
        subject[subject_name.lower()] = {}
    _generate_default_data(subject[subject_name.lower()], SUBJECT_DATA)
    subject[subject_name.lower()]['real'] = subject_name


def message_generate_default_data(message_id: int):
    if message_id not in message_listener:
        message_listener[message_id] = {}
    _generate_default_data(message_listener[message_id], MESSAGE_DATA)
