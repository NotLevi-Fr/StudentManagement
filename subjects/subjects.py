from database.database import get_all_subjects


def get_subjects():
    return get_all_subjects()


def get_subject_map():

    subjects = {}

    for subject in get_all_subjects():
        subjects[subject[2]] = subject

    return subjects
