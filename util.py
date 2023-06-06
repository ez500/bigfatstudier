"""Utilities"""

from data_config import *


def get_real_subject(subject_name: str) -> list[str]:
    subject_name = ' '.join(subject_name.split()).lower()
    if subject_name in subject_data:
        return [subject_name, subject_data[subject_name]['real']]
    for name in subject_data:
        if subject_name in subject_data[name]['alias']:
            return [name, subject_data[name]['real']]
    raise KeyError('This subject doesn\'t exist!')


def add_subject(subject_name: str, owner: int) -> list[str]:
    subject_name = ' '.join(subject_name.split())
    if subject_name.lower() == 'all':
        raise AttributeError('You can\'t add an \'all\' subject!')
    if subject_name.lower() in subject_data:
        raise KeyError('This subject already exists!')
    subject_generate_default_data(subject_name, owner)
    return get_real_subject(subject_name)


def remove_subject(subject_name: str) -> None:
    subject_name = ' '.join(subject_name.split()).lower()
    if subject_name in subject_data:
        remove_all_users_subject(subject_name)
        remove_all_admins_subject(subject_name)
        del subject_data[subject_name]
        return
    raise KeyError('This subject doesn\'t exist!')


def get_subject_alias(subject_name: str) -> list[str]:
    subject_name = ' '.join(subject_name.split()).lower()
    if subject_name in subject_data:
        return subject_data[subject_name]['alias']
    raise KeyError('This subject doesn\'t exist!')


def add_subject_alias(subject_name: str, subject_alias: str) -> None:
    subject_name = ' '.join(subject_name.split()).lower()
    if subject_name in subject_data:
        for alias in subject_data[subject_name]['alias']:
            if alias.lower() == subject_alias:
                raise AttributeError(f'{subject_alias} is already an alias!')
        subject_data[subject_name]['alias'].append(subject_alias)
        return
    raise KeyError('This subject doesn\'t exist!')


def remove_subject_alias(subject_name: str, subject_alias: str) -> None:
    subject_name = ' '.join(subject_name.split()).lower()
    if subject_name in subject_data:
        for alias in subject_data[subject_name]['alias']:
            if alias.lower() == subject_alias:
                subject_data[subject_name]['alias'].remove(subject_alias)
                return
        raise AttributeError(f'{subject_alias} isn\'t an alias!')
    raise KeyError('This subject doesn\'t exist!')


def get_subject_description(subject_name: str) -> str:
    subject_name = ' '.join(subject_name.split()).lower()
    if subject_name in subject_data:
        return subject_data[subject_name]['description']
    raise KeyError('This subject doesn\'t exist!')


def set_subject_description(subject_name: str, subject_description: str) -> None:
    subject_name = ' '.join(subject_name.split()).lower()
    if subject_name in subject_data:
        if subject_data[subject_name]['description'] == subject_description.lower():
            raise AttributeError(f'{subject_description} is already the description!')
        subject_data[subject_name]['description'] = subject_description
        return
    raise KeyError('This subject doesn\'t exist!')


def get_subject_homework(subject_name: str) -> list[str]:
    subject_name = ' '.join(subject_name.split()).lower()
    if subject_name in subject_data:
        homework = []
        for h in subject_data[subject_name]['homework']:
            homework.append(f'''{h['name']}, due {h['due_date']}''')
        return homework
    raise KeyError('This subject doesn\'t exist!')


def get_subject_homework_name(subject_name: str) -> list[str]:
    subject_name = ' '.join(subject_name.split()).lower()
    if subject_name in subject_data:
        homework = []
        for h in subject_data[subject_name]['homework']:
            homework.append(h['name'])
        return homework
    raise KeyError('This subject doesn\'t exist!')


def add_subject_homework(subject_name: str, assignment: str, due_date: str) -> None:
    subject_name = ' '.join(subject_name.split()).lower()
    assignment = ' '.join(assignment.split())
    if subject_name in subject_data:
        for homework in subject_data[subject_name]['homework']:
            if assignment.lower() == homework['description']:
                raise AttributeError(f'{assignment} already exists in this subject!')
        subject_data[subject_name]['homework'].append(Work(name=assignment,
                                                           description=assignment.lower(),
                                                           due_date=due_date).to_dict())
        return
    raise KeyError('This subject doesn\'t exist!')


def remove_subject_homework(subject_name: str, assignment: str) -> None:
    subject_name = ' '.join(subject_name.split()).lower()
    assignment = ' '.join(assignment.split())
    if subject_name in subject_data:
        for homework in subject_data[subject_name]['homework']:
            if assignment.lower() == homework['description']:
                subject_data[subject_name]['homework'].remove(homework)
                return
        raise AttributeError('This assignment doesn\'t exist!')
    raise KeyError('This subject doesn\'t exist!')


def clear_subject_homework(subject_name: str) -> None:
    subject_name = ' '.join(subject_name.split()).lower()
    if subject_name in subject_data:
        for homework in subject_data[subject_name]['homework']:
            subject_data[subject_name]['homework'].remove(homework)
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


def get_user_subjects(user_id: int) -> list[str]:
    if user_id not in user_data:
        user_generate_default_data(user_id)
    return user_data[user_id]['classes']


def get_admin_subjects(user_id: int) -> list[str]:
    if user_id not in user_data:
        user_generate_default_data(user_id)
    return user_data[user_id]['admin']


def add_user_subject(user_id: int, subject_name: str) -> None:
    if user_id not in user_data:
        user_generate_default_data(user_id)
    if subject_name in subject_data:
        user_data[user_id]['classes'].append(subject_name)
        subject_data[subject_name]['students'].append(user_id)
        return
    raise KeyError('This subject doesn\'t exist!')


def remove_user_subject(user_id: int, subject_name: str) -> None:
    if user_id not in user_data:
        user_generate_default_data(user_id)
    elif subject_name in user_data[user_id]['classes']:
        user_data[user_id]['classes'].remove(subject_name)
        subject_data[subject_name]['students'].remove(user_id)
        return
    raise KeyError('This subject isn\'t in the user\'s list of subjects!')


def remove_all_users_subject(subject_name: str) -> None:
    for user_id in user_data:
        if subject_name in user_data[user_id]['classes']:
            user_data[user_id]['classes'].remove(subject_name)


def add_admin_subject(user_id: int, subject_name: str) -> None:
    if user_id not in user_data:
        user_generate_default_data(user_id)
    if subject_name in subject_data:
        user_data[user_id]['admin'].append(subject_name)
        subject_data[subject_name]['admin'].append(user_id)
        return
    raise KeyError('This subject doesn\'t exist!')


def remove_admin_subject(user_id: int, subject_name: str) -> None:
    if user_id not in user_data:
        user_generate_default_data(user_id)
    elif subject_name in user_data[user_id]['admin']:
        user_data[user_id]['admin'].remove(subject_name)
        subject_data[subject_name]['admin'].remove(user_id)
        return
    raise KeyError('This user isn\'t an admin of this subject!')


def remove_all_admins_subject(subject_name: str) -> None:
    for user_id in user_data:
        if subject_name in user_data[user_id]['admin']:
            user_data[user_id]['admin'].remove(subject_name)


def is_subscribed(user_id: int, subject_name: str) -> bool:
    if user_id not in user_data:
        user_generate_default_data(user_id)
    elif subject_name in get_user_subjects(user_id):
        return True
    return False


def is_admin(user_id: int, subject_name: str) -> bool:
    if user_id not in user_data:
        user_generate_default_data(user_id)
    elif subject_name in get_admin_subjects(user_id):
        return True
    return False
