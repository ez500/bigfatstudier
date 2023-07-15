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
    subject_generate_default_data(subject_name)
    subject_data[subject_name.lower()]['real'] = subject_name
    subject_data[subject_name.lower()]['owner'] = owner
    subject_data[subject_name.lower()]['admin'].append(owner)
    subject_data[subject_name.lower()]['students'].append(owner)
    if owner not in user_data:
        user_generate_default_data(owner)
    user_data[owner]['classes'][subject_name.lower()] = (UserClass(name=subject_name, permission_level=2).to_dict())
    return get_real_subject(subject_name)


def remove_subject(subject_name: str) -> None:
    subject_name = ' '.join(subject_name.split()).lower()
    if subject_name in subject_data:
        remove_all_users_subject(subject_name)
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
            homework.append(f'''{subject_data[subject_name]['homework'][h]['name']}, '''
                            f'''due {subject_data[subject_name]['homework'][h]['due_date']}''')
        return homework
    raise SubjectError(f'There is no such subject as {subject_name}!')


def get_subject_homework_names(subject_name: str) -> list[str]:
    subject_name = ' '.join(subject_name.split()).lower()
    if subject_name in subject_data:
        homework = []
        for h in subject_data[subject_name]['homework']:
            homework.append(subject_data[subject_name]['homework'][h]['name'])
        return homework
    raise SubjectError(f'There is no such subject as {subject_name}!')


def add_subject_homework(subject_name: str, homework: str, due_date: str) -> None:
    subject_name = ' '.join(subject_name.split()).lower()
    homework = ' '.join(homework.split())
    if subject_name in subject_data:
        for h in subject_data[subject_name]['homework']:
            if homework.lower() == subject_data[subject_name]['homework'][h]['description']:
                raise SubjectAttributeError(f'You can\'t duplicate homework assignments!')
        subject_data[subject_name]['homework'][homework] = Work(name=homework,
                                                                description=homework.lower(),
                                                                due_date=due_date).to_dict()
        return
    raise SubjectError(f'There is no such subject as {subject_name}!')


def remove_subject_homework(subject_name: str, homework: str) -> str:
    subject_name = ' '.join(subject_name.split()).lower()
    homework = ' '.join(homework.split())
    if subject_name in subject_data:
        for h in subject_data[subject_name]['homework']:
            if homework.lower() == subject_data[subject_name]['homework'][h]['description']:
                real_name = subject_data[subject_name]['homework'][h]['name']
                del subject_data[subject_name]['homework'][h]
                return real_name
        raise SubjectAttributeError(f'{homework} doesn\'t exist!')
    raise SubjectError(f'There is no such subject as {subject_name}!')


def clear_subject_homework(subject_name: str) -> None:
    subject_name = ' '.join(subject_name.split()).lower()
    if subject_name in subject_data:
        subject_data[subject_name]['homework'].clear()
        return

    raise SubjectError(f'There is no such subject as {subject_name}!')


def get_subject_projects(subject_name: str) -> list[str]:
    subject_name = ' '.join(subject_name.split()).lower()
    if subject_name in subject_data:
        projects = []
        for p in subject_data[subject_name]['project']:
            projects.append(f'''{subject_data[subject_name]['project'][p]['name']}, '''
                            f'''due {subject_data[subject_name]['project'][p]['due_date']}''')
        return projects
    raise SubjectError(f'There is no such subject as {subject_name}!')


def get_subject_project_names(subject_name: str) -> list[str]:
    subject_name = ' '.join(subject_name.split()).lower()
    if subject_name in subject_data:
        projects = []
        for p in subject_data[subject_name]['project']:
            projects.append(subject_data[subject_name]['project'][p]['name'])
        return projects
    raise SubjectError(f'There is no such subject as {subject_name}!')


def add_subject_project(subject_name: str, project: str, due_date: str) -> None:
    subject_name = ' '.join(subject_name.split()).lower()
    project = ' '.join(project.split())
    if subject_name in subject_data:
        for p in subject_data[subject_name]['project']:
            if project.lower() == subject_data[subject_name]['project'][p]['description']:
                raise SubjectAttributeError(f'You can\'t duplicate projects!')
        subject_data[subject_name]['project'][project] = Work(name=project,
                                                              description=project.lower(),
                                                              due_date=due_date).to_dict()
        return
    raise SubjectError(f'There is no such subject as {subject_name}!')


def remove_subject_project(subject_name: str, project: str) -> str:
    subject_name = ' '.join(subject_name.split()).lower()
    project = ' '.join(project.split())
    if subject_name in subject_data:
        for p in subject_data[subject_name]['project']:
            if project.lower() == subject_data[subject_name]['project'][p]['description']:
                real_name = subject_data[subject_name]['project'][p]['name']
                del subject_data[subject_name]['project'][p]
                return real_name
        raise SubjectAttributeError(f'{project} doesn\'t exist!')
    raise SubjectError(f'There is no such subject as {subject_name}!')


def clear_subject_projects(subject_name: str) -> None:
    subject_name = ' '.join(subject_name.split()).lower()
    if subject_name in subject_data:
        subject_data[subject_name]['project'].clear()
        return
    raise SubjectError(f'There is no such subject as {subject_name}!')


def get_subject_tests(subject_name: str) -> list[str]:
    subject_name = ' '.join(subject_name.split()).lower()
    if subject_name in subject_data:
        tests = []
        for t in subject_data[subject_name]['test']:
            tests.append(f'''{subject_data[subject_name]['test'][t]['name']}, '''
                         f'''due {subject_data[subject_name]['test'][t]['due_date']}''')
        return tests
    raise SubjectError(f'There is no such subject as {subject_name}!')


def get_subject_test_names(subject_name: str) -> list[str]:
    subject_name = ' '.join(subject_name.split()).lower()
    if subject_name in subject_data:
        tests = []
        for t in subject_data[subject_name]['test']:
            tests.append(subject_data[subject_name]['test'][t]['name'])
        return tests
    raise SubjectError(f'There is no such subject as {subject_name}!')


def add_subject_test(subject_name: str, test: str, due_date: str) -> None:
    subject_name = ' '.join(subject_name.split()).lower()
    test = ' '.join(test.split())
    if subject_name in subject_data:
        for t in subject_data[subject_name]['test']:
            if test.lower() == subject_data[subject_name]['test'][t]['description']:
                raise SubjectAttributeError(f'You can\'t duplicate tests!')
        subject_data[subject_name]['test'][test] = Work(name=test,
                                                        description=test.lower(),
                                                        due_date=due_date).to_dict()
        return
    raise SubjectError(f'There is no such subject as {subject_name}!')


def remove_subject_test(subject_name: str, test: str) -> str:
    subject_name = ' '.join(subject_name.split()).lower()
    test = ' '.join(test.split())
    if subject_name in subject_data:
        for t in subject_data[subject_name]['test']:
            if test.lower() == subject_data[subject_name]['test'][t]['description']:
                real_name = subject_data[subject_name]['test'][t]['name']
                del subject_data[subject_name]['test'][t]
                return real_name
        raise SubjectAttributeError(f'{test} doesn\'t exist!')
    raise SubjectError(f'There is no such subject as {subject_name}!')


def clear_subject_tests(subject_name: str) -> None:
    subject_name = ' '.join(subject_name.split()).lower()
    if subject_name in subject_data:
        subject_data[subject_name]['test'].clear()
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
    admin_classes = [c for c in user_data[user_id]['classes'] if c['permission_level'] == 2]
    return admin_classes


def add_user_subject(user_id: int, subject_name: str) -> None:
    if user_id not in user_data:
        user_generate_default_data(user_id)
    if subject_name in subject_data:
        if is_subscribed(user_id, subject_name):
            raise UserError(f'You are already subscribed to {get_real_subject(subject_name)[1]}!')
        user_data[user_id]['classes'][subject_name] = (UserClass(name=subject_name, permission_level=0).to_dict())
        subject_data[subject_name]['students'].append(user_id)
        return
    raise SubjectError(f'There is no such subject as {subject_name}!')


def remove_user_subject(user_id: int, subject_name: str) -> None:
    if user_id not in user_data:
        user_generate_default_data(user_id)
    if is_owner(user_id, subject_name):
        raise UserOwnerError(f'An owner of the subject cannot unsubscribe!')
    if subject_name in user_data[user_id]['classes']:
        del user_data[user_id]['classes'][subject_name]
        subject_data[subject_name]['students'].remove(user_id)
        return
    raise UserError(f'You are already not subscribed to {get_real_subject(subject_name)[1]}!')


def remove_all_users_subject(subject_name: str) -> None:
    for user_id in user_data:
        if subject_name in user_data[user_id]['classes']:
            del user_data[user_id]['classes'][subject_name]


def add_admin_subject(user_mention: str, subject_name: str) -> None:
    user_id = int(user_mention[2:-1])
    if user_id not in user_data:
        user_generate_default_data(user_id)
    if subject_name in subject_data:
        if not is_subscribed(user_id, subject_name):
            raise UserError(f'{user_mention} is not subscribed to {get_real_subject(subject_name)[1]}!')
        if is_admin(user_id, subject_name):
            raise UserError(f'{user_mention} is already an admin of {get_real_subject(subject_name)[1]}!')
        user_data[user_id]['classes'][subject_name]['permission_level'] = 1
        subject_data[subject_name]['admin'].append(user_id)
        return
    raise SubjectError(f'There is no such subject as {subject_name}!')


def remove_admin_subject(user_mention: str, subject_name: str) -> None:
    user_id = int(user_mention[2:-1])
    if user_id not in user_data:
        user_generate_default_data(user_id)
    elif is_owner(user_id, subject_name):
        raise UserOwnerError(f'The owner cannot be removed as admin of their own subject!')
    elif is_admin(user_id, subject_name):
        user_data[user_id]['classes'][subject_name]['permission_level'] = 0
        subject_data[subject_name]['admin'].remove(user_id)
        return
    raise UserError(f'{user_mention} is not an admin of {get_real_subject(subject_name)[1]}!')


def is_subscribed(user_id: int, subject_name: str) -> bool:
    if user_id not in user_data:
        user_generate_default_data(user_id)
        return False
    return subject_name in user_data[user_id]['classes']


def is_admin(user_id: int, subject_name: str) -> bool:
    if user_id not in user_data:
        user_generate_default_data(user_id)
        return False
    if subject_name not in user_data[user_id]['classes']:
        return False
    return int(user_data[user_id]['classes'][subject_name]['permission_level']) >= 1


def is_owner(user_id: int, subject_name: str) -> bool:
    if user_id not in user_data:
        user_generate_default_data(user_id)
        return False
    if subject_name not in user_data[user_id]['classes']:
        return False
    return int(user_data[user_id]['classes'][subject_name]['permission_level']) == 2
