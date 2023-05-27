"""Utilities"""

from datetime import datetime

import data_config
from data_config import subject


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


def get_subject_homework(subject_name: str) -> str:
    subject_name = ' '.join(subject_name.split()).lower()
    if subject_name in subject:
        homework = ''
        for h in subject[subject_name]['homework']:
            homework += h.name + ", due " + h.due_date
        return homework
    raise KeyError('This subject doesn\'t exist!')


def add_subject_homework(subject_name: str, assignment: str, due_date: str) -> None:
    subject_name = ' '.join(subject_name.split()).lower()
    assignment = ' '.join(assignment.split())
    if subject_name in subject:
        for h in subject[subject_name]['homework']:
            if assignment.lower() == h.description:
                raise AttributeError('This assignment already exists!')  # TODO: BETTER EXCEPTIONS
        subject[subject_name]['homework'].append(data_config.Work(name=assignment,
                                                                  description=assignment.lower(),
                                                                  due_date=due_date))
        return
    raise KeyError('This subject doesn\'t exist!')


def remove_subject_homework(subject_name: str, assignment: str) -> None:
    subject_name = ' '.join(subject_name.split()).lower()
    assignment = ' '.join(assignment.split())
    if subject_name in subject:
        for h in subject[subject_name]['homework']:
            if assignment.lower() == h.description:
                subject[subject_name]['homework'].remove(h)
        raise AttributeError('This assignment doesn\'t exist!')
    raise KeyError('This subject doesn\'t exist!')