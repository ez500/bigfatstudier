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
    raise SubjectError(f'There is no such subject as {subject_name}!')


def add_subject(subject_name: str, owner: int) -> list[str]:
    subject_name = ' '.join(subject_name.split())
    if subject_name.lower() == 'all':
        raise SubjectNameError('You can\'t add an \'all\' subject!')
    if subject_name.lower() == 'subscribed':
        raise SubjectNameError('You can\'t add a \'subscribed\' subject!')
    if subject_name.lower() in subject_data:
        raise SubjectError(f'The subject {get_real_subject(subject_name.lower())[1]} already exists!')
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
    raise SubjectError(f'There is no such subject as {subject_name}!')


def get_subject_alias(subject_name: str) -> list[str]:
    subject_name = ' '.join(subject_name.split()).lower()
    if subject_name in subject_data:
        return subject_data[subject_name]['alias']
    raise SubjectError(f'There is no such subject as {subject_name}!')


def add_subject_alias(subject_name: str, subject_alias: str) -> None:
    subject_name = ' '.join(subject_name.split()).lower()
    if subject_name in subject_data:
        for alias in subject_data[subject_name]['alias']:
            if alias.lower() == subject_alias:
                raise SubjectAttributeError(f'{subject_alias} already exists as an alias to '
                                            f'{get_real_subject(subject_name)[1]}!')
        subject_data[subject_name]['alias'].append(subject_alias)
        return
    raise SubjectError(f'There is no such subject as {subject_name}!')


def remove_subject_alias(subject_name: str, subject_alias: str) -> None:
    subject_name = ' '.join(subject_name.split()).lower()
    if subject_name in subject_data:
        for alias in subject_data[subject_name]['alias']:
            if alias.lower() == subject_alias:
                subject_data[subject_name]['alias'].remove(subject_alias)
                return
        raise SubjectAttributeError(f'There is no such alias as {subject_alias} in '
                                    f'{get_real_subject(subject_name)[1]}!')
    raise SubjectError(f'There is no such subject as {subject_name}!')


def get_subject_description(subject_name: str) -> str:
    subject_name = ' '.join(subject_name.split()).lower()
    if subject_name in subject_data:
        return subject_data[subject_name]['description']
    raise SubjectError(f'There is no such subject as {subject_name}!')


def set_subject_description(subject_name: str, subject_description: str) -> None:
    subject_name = ' '.join(subject_name.split()).lower()
    if subject_name in subject_data:
        if subject_data[subject_name]['description'] == subject_description.lower():
            if subject_description.lower() == 'no description':
                raise SubjectAttributeError(f'{get_real_subject(subject_name)[1]} has no description to clear!')
            raise SubjectAttributeError(f'{subject_description} is already the description of '
                                        f'{get_real_subject(subject_name)[1]}!')
        subject_data[subject_name]['description'] = subject_description
        return
    raise SubjectError(f'There is no such subject as {subject_name}!')


def get_subject_homework(subject_name: str) -> list[str]:
    subject_name = ' '.join(subject_name.split()).lower()
    if subject_name in subject_data:
        homework = []
        for h in subject_data[subject_name]['homework']:
            homework.append(f'''{h['name']}, due {h['due_date']}''')
        return homework
    raise SubjectError(f'There is no such subject as {subject_name}!')


def get_subject_homework_names(subject_name: str) -> list[str]:
    subject_name = ' '.join(subject_name.split()).lower()
    if subject_name in subject_data:
        homework = []
        for h in subject_data[subject_name]['homework']:
            homework.append(h['name'])
        return homework
    raise SubjectError(f'There is no such subject as {subject_name}!')


def add_subject_homework(subject_name: str, homework: str, due_date: str) -> None:
    subject_name = ' '.join(subject_name.split()).lower()
    homework = ' '.join(homework.split())
    if subject_name in subject_data:
        for h in subject_data[subject_name]['homework']:
            if homework.lower() == h['description']:
                raise SubjectAttributeError(f'You can\'t duplicate homework assignments!')
        subject_data[subject_name]['homework'].append(Work(name=homework,
                                                           description=homework.lower(),
                                                           due_date=due_date).to_dict())
        return
    raise SubjectError(f'There is no such subject as {subject_name}!')


def remove_subject_homework(subject_name: str, homework: str) -> None:
    subject_name = ' '.join(subject_name.split()).lower()
    homework = ' '.join(homework.split())
    if subject_name in subject_data:
        for h in subject_data[subject_name]['homework']:
            if homework.lower() == h['description']:
                subject_data[subject_name]['homework'].remove(h)
                return
        raise SubjectAttributeError(f'{homework} doesn\'t exist!')
    raise SubjectError(f'There is no such subject as {subject_name}!')


def clear_subject_homework(subject_name: str) -> None:
    subject_name = ' '.join(subject_name.split()).lower()
    if subject_name in subject_data:
        for homework in subject_data[subject_name]['homework']:
            subject_data[subject_name]['homework'].remove(homework)
        return
    raise SubjectError(f'There is no such subject as {subject_name}!')


def get_subject_projects(subject_name: str) -> list[str]:
    subject_name = ' '.join(subject_name.split()).lower()
    if subject_name in subject_data:
        project = []
        for p in subject_data[subject_name]['project']:
            project.append(f'''{p['name']}, due {p['due_date']}''')
        return project
    raise SubjectError(f'There is no such subject as {subject_name}!')


def get_subject_project_names(subject_name: str) -> list[str]:
    subject_name = ' '.join(subject_name.split()).lower()
    if subject_name in subject_data:
        project = []
        for p in subject_data[subject_name]['project']:
            project.append(p['name'])
        return project
    raise SubjectError(f'There is no such subject as {subject_name}!')


def add_subject_project(subject_name: str, project: str, due_date: str) -> None:
    subject_name = ' '.join(subject_name.split()).lower()
    project = ' '.join(project.split())
    if subject_name in subject_data:
        for p in subject_data[subject_name]['project']:
            if project.lower() == p['description']:
                raise SubjectAttributeError(f'You can\'t duplicate projects!')
        subject_data[subject_name]['project'].append(Work(name=project,
                                                          description=project.lower(),
                                                          due_date=due_date).to_dict())
        return
    raise SubjectError(f'There is no such subject as {subject_name}!')


def remove_subject_project(subject_name: str, project: str) -> None:
    subject_name = ' '.join(subject_name.split()).lower()
    project = ' '.join(project.split())
    if subject_name in subject_data:
        for p in subject_data[subject_name]['project']:
            if project.lower() == p['description']:
                subject_data[subject_name]['project'].remove(p)
                return
        raise SubjectAttributeError(f'{project} doesn\'t exist!')
    raise SubjectError(f'There is no such subject as {subject_name}!')


def clear_subject_projects(subject_name: str) -> None:
    subject_name = ' '.join(subject_name.split()).lower()
    if subject_name in subject_data:
        for project in subject_data[subject_name]['project']:
            subject_data[subject_name]['project'].remove(project)
        return
    raise SubjectError(f'There is no such subject as {subject_name}!')


def get_subject_tests(subject_name: str) -> list[str]:
    subject_name = ' '.join(subject_name.split()).lower()
    if subject_name in subject_data:
        test = []
        for t in subject_data[subject_name]['test']:
            test.append(f'''{t['name']}, due {t['due_date']}''')
        return test
    raise SubjectError(f'There is no such subject as {subject_name}!')


def get_subject_test_names(subject_name: str) -> list[str]:
    subject_name = ' '.join(subject_name.split()).lower()
    if subject_name in subject_data:
        test = []
        for t in subject_data[subject_name]['test']:
            test.append(t['name'])
        return test
    raise SubjectError(f'There is no such subject as {subject_name}!')


def add_subject_test(subject_name: str, test: str, due_date: str) -> None:
    subject_name = ' '.join(subject_name.split()).lower()
    test = ' '.join(test.split())
    if subject_name in subject_data:
        for t in subject_data[subject_name]['test']:
            if test.lower() == t['description']:
                raise SubjectAttributeError(f'You can\'t duplicate tests!')
        subject_data[subject_name]['test'].append(Work(name=test,
                                                       description=test.lower(),
                                                       due_date=due_date).to_dict())
        return
    raise SubjectError(f'There is no such subject as {subject_name}!')


def remove_subject_test(subject_name: str, test: str) -> None:
    subject_name = ' '.join(subject_name.split()).lower()
    test = ' '.join(test.split())
    if subject_name in subject_data:
        for t in subject_data[subject_name]['test']:
            if test.lower() == t['description']:
                subject_data[subject_name]['test'].remove(t)
                return
        raise SubjectAttributeError(f'{test} doesn\'t exist!')
    raise SubjectError(f'There is no such subject as {subject_name}!')


def clear_subject_tests(subject_name: str) -> None:
    subject_name = ' '.join(subject_name.split()).lower()
    if subject_name in subject_data:
        for test in subject_data[subject_name]['test']:
            subject_data[subject_name]['test'].remove(test)
        return
    raise SubjectError(f'There is no such subject as {subject_name}!')


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
            raise UserError(f'You are already subscribed to {get_real_subject(subject_name)[1]}!')
        user_data[user_id]['classes'].append(subject_name)
        subject_data[subject_name]['students'].append(user_id)
        return
    raise SubjectError(f'There is no such subject as {subject_name}!')


def remove_user_subject(user_id: int, subject_name: str) -> None:
    if user_id not in user_data:
        user_generate_default_data(user_id)
    elif subject_name in user_data[user_id]['classes']:
        if is_owner(user_id, subject_name):
            raise UserOwnerError(f'An owner of the subject cannot unsubscribe!')
        user_data[user_id]['classes'].remove(subject_name)
        subject_data[subject_name]['students'].remove(user_id)
        return
    raise UserError(f'You are already not subscribed to {get_real_subject(subject_name)[1]}!')


def remove_all_users_subject(subject_name: str) -> None:
    for user_id in user_data:
        if subject_name in user_data[user_id]['classes']:
            user_data[user_id]['classes'].remove(subject_name)


def add_admin_subject(user_mention: str, subject_name: str) -> None:
    user_id = int(user_mention[2:-1])
    if user_id not in user_data:
        user_generate_default_data(user_id)
    if subject_name in subject_data:
        if is_admin(user_id, subject_name):
            raise UserError(f'{user_mention} is already an admin of {get_real_subject(subject_name)[1]}!')
        user_data[user_id]['admin'].append(subject_name)
        subject_data[subject_name]['admin'].append(user_id)
        return
    raise SubjectError(f'There is no such subject as {subject_name}!')


def remove_admin_subject(user_mention: str, subject_name: str) -> None:
    user_id = int(user_mention[2:-1])
    if user_id not in user_data:
        user_generate_default_data(user_id)
    elif is_admin(user_id, subject_name):
        if is_owner(user_id, subject_name):
            raise UserOwnerError(f'The owner cannot be removed as admin of their own subject!')
        user_data[user_id]['admin'].remove(subject_name)
        subject_data[subject_name]['admin'].remove(user_id)
        return
    raise UserError(f'{user_mention} is not an admin of {get_real_subject(subject_name)[1]}!')


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
