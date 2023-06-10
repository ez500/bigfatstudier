"""Utilities"""

from data_config import *


class SubjectError(Exception):
    pass
class SubjectNameError(Exception):
    pass
class SubjectAttributeError(Exception):
    pass
class MessageError(Exception):
    pass
class MessageAttributeError(Exception):
    pass
class UserError(Exception):
    pass
class UserAdminError(Exception):
    pass
class UserOwnerError(Exception):
    pass


def get_real_subject(subject_name: str) -> list[str]:
    subject_name = ' '.join(subject_name.split()).lower()
    if subject_name in subject_data:
        return [subject_name, subject_data[subject_name]['real']]
    for name in subject_data:
        if subject_name in subject_data[name]['alias']:
            return [name, subject_data[name]['real']]
    raise SubjectError('This subject doesn\'t exist!')


def add_subject(subject_name: str, owner: int) -> list[str]:
    subject_name = ' '.join(subject_name.split())
    if subject_name.lower() == 'all' or subject_name.lower() == 'subscribed':
        raise SubjectNameError('You can\'t add an \'all\' or \'subscribed\' subject!')
    if subject_name.lower() in subject_data:
        raise SubjectError('This subject already exists!')
    for subject in subject_data:
        if subject_name.lower() in subject_data[subject]['alias']:
            raise SubjectAttributeError(f'{subject_name} already exists as an alias to {get_real_subject(subject)[1]}!')
    subject_generate_default_data(subject_name, owner)
    return get_real_subject(subject_name)


def remove_subject(subject_name: str) -> None:
    subject_name = ' '.join(subject_name.split()).lower()
    if subject_name in subject_data:
        remove_all_users_subject(subject_name)
        remove_all_admins_subject(subject_name)
        del subject_data[subject_name]
        return
    raise SubjectError('This subject doesn\'t exist!')


def get_subject_alias(subject_name: str) -> list[str]:
    subject_name = ' '.join(subject_name.split()).lower()
    if subject_name in subject_data:
        return subject_data[subject_name]['alias']
    raise SubjectError('This subject doesn\'t exist!')


def add_subject_alias(subject_name: str, subject_alias: str) -> None:
    subject_name = ' '.join(subject_name.split()).lower()
    if subject_name in subject_data:
        for alias in subject_data[subject_name]['alias']:
            if alias.lower() == subject_alias:
                raise SubjectAttributeError(f'{subject_alias} is already an alias!')
        subject_data[subject_name]['alias'].append(subject_alias)
        return
    raise SubjectError('This subject doesn\'t exist!')


def remove_subject_alias(subject_name: str, subject_alias: str) -> None:
    subject_name = ' '.join(subject_name.split()).lower()
    if subject_name in subject_data:
        for alias in subject_data[subject_name]['alias']:
            if alias.lower() == subject_alias:
                subject_data[subject_name]['alias'].remove(subject_alias)
                return
        raise SubjectAttributeError(f'{subject_alias} isn\'t an alias!')
    raise SubjectError('This subject doesn\'t exist!')


def get_subject_description(subject_name: str) -> str:
    subject_name = ' '.join(subject_name.split()).lower()
    if subject_name in subject_data:
        return subject_data[subject_name]['description']
    raise SubjectError('This subject doesn\'t exist!')


def set_subject_description(subject_name: str, subject_description: str) -> None:
    subject_name = ' '.join(subject_name.split()).lower()
    if subject_name in subject_data:
        if subject_data[subject_name]['description'] == subject_description.lower():
            raise SubjectAttributeError(f'{subject_description} is already the description!')
        subject_data[subject_name]['description'] = subject_description
        return
    raise SubjectError('This subject doesn\'t exist!')


def get_subject_homework(subject_name: str) -> list[str]:
    subject_name = ' '.join(subject_name.split()).lower()
    if subject_name in subject_data:
        homework = []
        for h in subject_data[subject_name]['homework']:
            homework.append(f'''{h['name']}, due {h['due_date']}''')
        return homework
    raise SubjectError('This subject doesn\'t exist!')


def get_subject_homework_names(subject_name: str) -> list[str]:
    subject_name = ' '.join(subject_name.split()).lower()
    if subject_name in subject_data:
        homework = []
        for h in subject_data[subject_name]['homework']:
            homework.append(h['name'])
        return homework
    raise SubjectError('This subject doesn\'t exist!')


def add_subject_homework(subject_name: str, homework: str, due_date: str) -> None:
    subject_name = ' '.join(subject_name.split()).lower()
    homework = ' '.join(homework.split())
    if subject_name in subject_data:
        for h in subject_data[subject_name]['homework']:
            if homework.lower() == h['description']:
                raise SubjectAttributeError(f'{homework} already exists in this subject!')
        subject_data[subject_name]['homework'].append(Work(name=homework,
                                                           description=homework.lower(),
                                                           due_date=due_date).to_dict())
        return
    raise SubjectError('This subject doesn\'t exist!')


def remove_subject_homework(subject_name: str, homework: str) -> None:
    subject_name = ' '.join(subject_name.split()).lower()
    homework = ' '.join(homework.split())
    if subject_name in subject_data:
        for h in subject_data[subject_name]['homework']:
            if homework.lower() == h['description']:
                subject_data[subject_name]['homework'].remove(h)
                return
        raise SubjectAttributeError('This assignment doesn\'t exist!')
    raise SubjectError('This subject doesn\'t exist!')


def clear_subject_homework(subject_name: str) -> None:
    subject_name = ' '.join(subject_name.split()).lower()
    if subject_name in subject_data:
        for homework in subject_data[subject_name]['homework']:
            subject_data[subject_name]['homework'].remove(homework)
        return
    raise SubjectError('This subject doesn\'t exist!')


def get_subject_projects(subject_name: str) -> list[str]:
    subject_name = ' '.join(subject_name.split()).lower()
    if subject_name in subject_data:
        project = []
        for p in subject_data[subject_name]['project']:
            project.append(f'''{p['name']}, due {p['due_date']}''')
        return project
    raise SubjectError('This subject doesn\'t exist!')


def get_subject_project_names(subject_name: str) -> list[str]:
    subject_name = ' '.join(subject_name.split()).lower()
    if subject_name in subject_data:
        project = []
        for p in subject_data[subject_name]['project']:
            project.append(p['name'])
        return project
    raise SubjectError('This subject doesn\'t exist!')


def add_subject_project(subject_name: str, project: str, due_date: str) -> None:
    subject_name = ' '.join(subject_name.split()).lower()
    project = ' '.join(project.split())
    if subject_name in subject_data:
        for p in subject_data[subject_name]['project']:
            if project.lower() == p['description']:
                raise SubjectAttributeError(f'{project} already exists in this subject!')
        subject_data[subject_name]['project'].append(Work(name=project,
                                                          description=project.lower(),
                                                          due_date=due_date).to_dict())
        return
    raise SubjectError('This subject doesn\'t exist!')


def remove_subject_project(subject_name: str, project: str) -> None:
    subject_name = ' '.join(subject_name.split()).lower()
    project = ' '.join(project.split())
    if subject_name in subject_data:
        for p in subject_data[subject_name]['project']:
            if project.lower() == p['description']:
                subject_data[subject_name]['project'].remove(p)
                return
        raise SubjectAttributeError('This assignment doesn\'t exist!')
    raise SubjectError('This subject doesn\'t exist!')


def clear_subject_projects(subject_name: str) -> None:
    subject_name = ' '.join(subject_name.split()).lower()
    if subject_name in subject_data:
        for project in subject_data[subject_name]['project']:
            subject_data[subject_name]['project'].remove(project)
        return
    raise SubjectError('This subject doesn\'t exist!')


def get_subject_tests(subject_name: str) -> list[str]:
    subject_name = ' '.join(subject_name.split()).lower()
    if subject_name in subject_data:
        test = []
        for t in subject_data[subject_name]['test']:
            test.append(f'''{t['name']}, due {t['due_date']}''')
        return test
    raise SubjectError('This subject doesn\'t exist!')


def get_subject_test_names(subject_name: str) -> list[str]:
    subject_name = ' '.join(subject_name.split()).lower()
    if subject_name in subject_data:
        test = []
        for t in subject_data[subject_name]['test']:
            test.append(t['name'])
        return test
    raise SubjectError('This subject doesn\'t exist!')


def add_subject_test(subject_name: str, test: str, due_date: str) -> None:
    subject_name = ' '.join(subject_name.split()).lower()
    test = ' '.join(test.split())
    if subject_name in subject_data:
        for t in subject_data[subject_name]['test']:
            if test.lower() == t['description']:
                raise SubjectAttributeError(f'{test} already exists in this subject!')
        subject_data[subject_name]['test'].append(Work(name=test,
                                                       description=test.lower(),
                                                       due_date=due_date).to_dict())
        return
    raise SubjectError('This subject doesn\'t exist!')


def remove_subject_test(subject_name: str, test: str) -> None:
    subject_name = ' '.join(subject_name.split()).lower()
    test = ' '.join(test.split())
    if subject_name in subject_data:
        for t in subject_data[subject_name]['test']:
            if test.lower() == t['description']:
                subject_data[subject_name]['test'].remove(t)
                return
        raise SubjectAttributeError('This assignment doesn\'t exist!')
    raise SubjectError('This subject doesn\'t exist!')


def clear_subject_tests(subject_name: str) -> None:
    subject_name = ' '.join(subject_name.split()).lower()
    if subject_name in subject_data:
        for test in subject_data[subject_name]['test']:
            subject_data[subject_name]['test'].remove(test)
        return
    raise SubjectError('This subject doesn\'t exist!')


def generate_message_listener(message_id: int, emojis: list[str], roles: list[int]):
    if len(emojis) != len(roles):
        print('here')
        raise MessageAttributeError('Emojis cannot be listened to with respective roles!')
    message_generate_default_data(message_id)
    for emoji, role in zip(emojis, roles):
        message_listener[message_id]['emoji'].append(emoji)
        message_listener[message_id]['role'].append(role)


def remove_message_listener(message_id: int):
    if message_id not in message_listener:
        raise MessageError('This message does not have any listeners!')
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
        if is_subscribed(user_id, subject_name):
            raise UserError('This user is already subscribed to this subject!')
        user_data[user_id]['classes'].append(subject_name)
        subject_data[subject_name]['students'].append(user_id)
        return
    raise SubjectError('This subject doesn\'t exist!')


def remove_user_subject(user_id: int, subject_name: str) -> None:
    if user_id not in user_data:
        user_generate_default_data(user_id)
    elif subject_name in user_data[user_id]['classes']:
        if is_owner(user_id, subject_name):
            raise UserOwnerError('The owner of this subject cannot unsubscribe!')
        user_data[user_id]['classes'].remove(subject_name)
        subject_data[subject_name]['students'].remove(user_id)
        return
    raise UserError('This user isn\'t subscribed to this subject!')


def remove_all_users_subject(subject_name: str) -> None:
    for user_id in user_data:
        if subject_name in user_data[user_id]['classes']:
            user_data[user_id]['classes'].remove(subject_name)


def add_admin_subject(user_id: int, subject_name: str) -> None:
    if user_id not in user_data:
        user_generate_default_data(user_id)
    if subject_name in subject_data:
        if is_admin(user_id, subject_name):
            raise UserError('This user is already an admin of this subject!')
        user_data[user_id]['admin'].append(subject_name)
        subject_data[subject_name]['admin'].append(user_id)
        return
    raise SubjectError('This subject doesn\'t exist!')


def remove_admin_subject(user_id: int, subject_name: str) -> None:
    if user_id not in user_data:
        user_generate_default_data(user_id)
    elif is_admin(user_id, subject_name):
        if is_owner(user_id, subject_name):
            raise UserOwnerError('The owner of this subject has to be an admin!')
        user_data[user_id]['admin'].remove(subject_name)
        subject_data[subject_name]['admin'].remove(user_id)
        return
    raise UserError('This user isn\'t an admin of this subject!')


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


def is_owner(user_id: int, subject_name: str) -> bool:
    if user_id not in user_data:
        user_generate_default_data(user_id)
    elif user_data[user_id]['owner'] == subject_name:
        return True
    return False
