"""Utilities"""

import data_config
from data_config import *


def get_real_subject(subject_name: str) -> list[str]:
    subject_name = ' '.join(subject_name.split()).lower()
    if subject_name in subject:
        return [subject_name, subject[subject_name]['real']]
    raise KeyError('This subject doesn\'t exist!')


def add_subject(subject_name: str) -> None:
    subject_name = ' '.join(subject_name.split())
    if subject_name.lower() == 'all':
        raise AttributeError('You can\'t add an \'all\' subject!')
    if subject_name.lower() in subject:
        raise KeyError('This subject already exists!')
    data_config.subject_generate_default_data(subject_name)


def remove_subject(subject_name: str) -> None:
    subject_name = ' '.join(subject_name.split()).lower()
    if subject_name in subject:
        del subject[subject_name]
        return
    raise KeyError('This subject doesn\'t exist!')


def get_subject_alias(subject_name: str) -> list[str]:
    subject_name = ' '.join(subject_name.split()).lower()
    if subject_name in subject:
        return subject[subject_name]['alias']
    raise KeyError('This subject doesn\'t exist!')


def add_subject_alias(subject_name: str, subject_alias: str) -> None:
    subject_name = ' '.join(subject_name.split()).lower()
    if subject_name in subject:
        for alias in subject[subject_name]['alias']:
            if alias.lower() == subject_alias:
                raise AttributeError(f'{subject_alias} is already an alias!')
        subject[subject_name]['alias'].append(subject_alias)
        return
    raise KeyError('This subject doesn\'t exist!')


def remove_subject_alias(subject_name: str, subject_alias: str) -> None:
    subject_name = ' '.join(subject_name.split()).lower()
    if subject_name in subject:
        for alias in subject[subject_name]['alias']:
            if alias.lower() == subject_alias:
                subject[subject_name]['alias'].remove(subject_alias)
                return
        raise AttributeError(f'{subject_alias} isn\'t an alias!')
    raise KeyError('This subject doesn\'t exist!')


def get_subject_description(subject_name: str) -> str:
    subject_name = ' '.join(subject_name.split()).lower()
    if subject_name in subject:
        return subject[subject_name]['description']
    raise KeyError('This subject doesn\'t exist!')


def set_subject_description(subject_name: str, subject_description: str) -> None:
    subject_name = ' '.join(subject_name.split()).lower()
    if subject_name in subject:
        if subject[subject_name]['description'] == subject_description.lower():
            raise AttributeError(f'{subject_description} is already the description!')
        subject[subject_name]['description'] = subject_description
        return
    raise KeyError('This subject doesn\'t exist!')


def get_subject_homework(subject_name: str) -> list[str]:
    subject_name = ' '.join(subject_name.split()).lower()
    if subject_name in subject:
        homework = []
        for h in subject[subject_name]['homework']:
            homework.append(f'''{h['name']}, due {h['due_date']}''')
        return homework
    raise KeyError('This subject doesn\'t exist!')


def get_subject_homework_name(subject_name: str) -> list[str]:
    subject_name = ' '.join(subject_name.split()).lower()
    if subject_name in subject:
        homework = []
        for h in subject[subject_name]['homework']:
            homework.append(h['name'])
        return homework
    raise KeyError('This subject doesn\'t exist!')


def add_subject_homework(subject_name: str, assignment: str, due_date: str) -> None:
    subject_name = ' '.join(subject_name.split()).lower()
    assignment = ' '.join(assignment.split())
    if subject_name in subject:
        for homework in subject[subject_name]['homework']:
            if assignment.lower() == homework['description']:
                raise AttributeError(f'{assignment} already exists in this subject!')
        subject[subject_name]['homework'].append(data_config.Work(name=assignment,
                                                                  description=assignment.lower(),
                                                                  due_date=due_date).to_dict())
        return
    raise KeyError('This subject doesn\'t exist!')


def remove_subject_homework(subject_name: str, assignment: str) -> None:
    subject_name = ' '.join(subject_name.split()).lower()
    assignment = ' '.join(assignment.split())
    if subject_name in subject:
        for homework in subject[subject_name]['homework']:
            if assignment.lower() == homework['description']:
                subject[subject_name]['homework'].remove(homework)
                return
        raise AttributeError('This assignment doesn\'t exist!')
    raise KeyError('This subject doesn\'t exist!')


def clear_subject_homework(subject_name: str) -> None:
    subject_name = ' '.join(subject_name.split()).lower()
    if subject_name in subject:
        for homework in subject[subject_name]['homework']:
            subject[subject_name]['homework'].remove(homework)
        return
    raise KeyError('This subject doesn\'t exist!')


def generate_message_listener(message_id: int, emojis: list[str], roles: list[int]):
    if len(emojis) != len(roles):
        print('here')
        raise ValueError('Emojis cannot be listened to with respective roles!')
    message_generate_default_data(message_id)
    for emoji, role in zip(emojis, roles):
        message_listener[message_id]['emoji'].append(emoji)
        message_listener[message_id]['role'].append(role)


def remove_message_listener(message_id: int):
    if message_id not in message_listener:
        raise KeyError('This message does not have any listeners!')
    del message_listener[message_id]
