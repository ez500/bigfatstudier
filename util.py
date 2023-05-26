"""Utilities"""

import data_config


def get_real_subject(subject_name: str) -> str:
    subject_name = ' '.join(subject_name.split())
    for i in data_config.subject:
        if i.lower() == subject_name.lower():
            return i
    raise KeyError('This subject_data doesn\'t exist!')


def get_subject_homework(subject_name: str) -> str:
    subject_name = ' '.join(subject_name.split())
    for i in data_config.subject:
        if i.lower() == subject_name.lower():
            return data_config.subject[i]
    raise KeyError('This subject_data doesn\'t exist!')


def set_subject_homework(subject_name: str, assignment: str) -> None:
    subject_name = ' '.join(subject_name.split())
    for i in data_config.subject:
        if i.lower() == subject_name.lower():
            data_config.subject[i] = assignment
            return
    raise KeyError('This subject_data doesn\'t exist!')


def add_subject(subject_name: str) -> None:
    subject_name = ' '.join(subject_name.split())
    for i in data_config.subject:
        if i.lower() == subject_name.lower():
            raise KeyError('This subject_data is already added!')
        elif subject_name.lower() == 'all':
            raise NameError('You can\'t add an \'all\' subject_data!')
    data_config.subject[subject_name] = 'None'


def remove_subject(subject_name: str) -> None:
    subject_name = ' '.join(subject_name.split())
    for i in data_config.subject:
        if i.lower() == subject_name.lower():
            data_config.subject.pop(i)
            return
    raise KeyError('This subject_data never existed!')
