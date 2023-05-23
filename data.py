import ast

with open('./data/subject', 'r') as f:
    subject = ast.literal_eval(f.read())


def get_real_subject(subject_name: str) -> str:
    subject_name = ' '.join(subject_name.split())
    for i in subject:
        if i.lower() == subject_name.lower():
            return i
    raise KeyError('This subject doesn\'t exist!')


def get_subject_homework(subject_name: str) -> str:
    subject_name = ' '.join(subject_name.split())
    for i in subject:
        if i.lower() == subject_name.lower():
            return subject[i]
    raise KeyError('This subject doesn\'t exist!')


def set_subject_homework(subject_name: str, assignment: str) -> None:
    subject_name = ' '.join(subject_name.split())
    for i in subject:
        if i.lower() == subject_name.lower():
            subject[i] = assignment
            return
    raise KeyError('This subject doesn\'t exist!')


def add_subject(subject_name: str) -> None:
    subject_name = ' '.join(subject_name.split())
    for i in subject:
        if i.lower() == subject_name.lower():
            raise KeyError('This subject is already added!')
        elif subject_name.lower() == 'all':
            raise NameError('You can\'t add an \'all\' subject!')
    subject[subject_name] = 'None'


def remove_subject(subject_name: str) -> None:
    subject_name = ' '.join(subject_name.split())
    for i in subject:
        if i.lower() == subject_name.lower():
            subject.pop(i)
            return
    raise KeyError('This subject never existed!')


def save_all() -> None:
    with open('data/subject', 'w') as file:
        file.write(repr(subject))
