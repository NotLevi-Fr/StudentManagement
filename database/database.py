import sqlite3
import json
from pathlib import Path

DATABASE = str(Path(__file__).resolve().parent.parent / "student.db")

SUBJECT_SEED = [
    "Programming 1",
    "Programming 2",
    "Data Structures",
    "Database Systems",
    "Web Development",
    "Computer Networks",
    "Operating Systems",
    "Software Engineering",
    "Information Management",
    "Artificial Intelligence",
    "Machine Learning",
    "System Administration",
    "Capstone Project 1",
    "Capstone Project 2",
    "Research in Computing"
]

TIME_SLOTS = [
    "M630-M730",
    "M730-M830",
    "M830-M930",
    "M930-M1030",
    "M1030-M1130",
    "M1130-M1230"
]


def get_connection():
    return sqlite3.connect(DATABASE)


def create_database():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT NOT NULL,
            age INTEGER NOT NULL,
            address TEXT NOT NULL,
            contact TEXT NOT NULL,
            email TEXT NOT NULL,
            course TEXT NOT NULL,
            year_level TEXT NOT NULL,
            subjects TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subjects(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code INTEGER UNIQUE NOT NULL,
            name TEXT UNIQUE NOT NULL,
            time TEXT NOT NULL,
            room TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS enrollments(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            subject_id INTEGER NOT NULL,
            fullname TEXT NOT NULL,
            age INTEGER NOT NULL,
            address TEXT NOT NULL,
            contact TEXT NOT NULL,
            email TEXT NOT NULL,
            course TEXT NOT NULL,
            year_level TEXT NOT NULL,
            enrolled_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
        )
    """)

    seed_subjects(cursor)
    backfill_enrollments(cursor)

    connection.commit()
    connection.close()


def seed_subjects(cursor):

    cursor.execute("SELECT COUNT(*) FROM subjects")

    if cursor.fetchone()[0] > 0:
        return

    for index, name in enumerate(SUBJECT_SEED):

        code = index + 1
        time = TIME_SLOTS[index % len(TIME_SLOTS)]
        room = "A" + str(code)

        cursor.execute("""
            INSERT INTO subjects (code, name, time, room)
            VALUES (?,?,?,?)
        """, (code, name, time, room))


def backfill_enrollments(cursor):

    cursor.execute("SELECT COUNT(*) FROM enrollments")

    if cursor.fetchone()[0] > 0:
        return

    cursor.execute("""
        SELECT id, fullname, age, address, contact, email,
               course, year_level, subjects
        FROM students
    """)

    students = cursor.fetchall()

    for student in students:

        if not student[8]:
            continue

        try:
            subjects = json.loads(student[8])
        except ValueError:
            continue

        _add_enrollments(cursor, student[0], student[1:8], subjects)


def _add_enrollments(cursor, student_id, student_data, subject_names):

    cursor.execute("SELECT id, name FROM subjects")

    subject_ids = {}

    for row in cursor.fetchall():
        subject_ids[row[1]] = row[0]

    for name in subject_names:

        subject_id = subject_ids.get(name)

        if subject_id is None:
            continue

        cursor.execute("""
            INSERT INTO enrollments(
                student_id,
                subject_id,
                fullname,
                age,
                address,
                contact,
                email,
                course,
                year_level
            )
            VALUES (?,?,?,?,?,?,?,?,?)
        """, (
            student_id,
            subject_id,
            student_data[0],
            student_data[1],
            student_data[2],
            student_data[3],
            student_data[4],
            student_data[5],
            student_data[6]
        ))


def get_all_subjects():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, code, name, time, room
        FROM subjects
        ORDER BY code
    """)

    subjects = cursor.fetchall()

    connection.close()

    return subjects


def get_all_enrollments():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            e.id,
            e.fullname,
            e.course,
            e.year_level,
            s.code,
            s.name,
            s.time,
            s.room,
            e.enrolled_at
        FROM enrollments e
        LEFT JOIN subjects s ON s.id = e.subject_id
        ORDER BY e.id DESC
    """)

    enrollments = cursor.fetchall()

    connection.close()

    return enrollments


def register_user(username, password):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute("""
            INSERT INTO users (username, password)
            VALUES (?,?)
        """, (username, password))

        connection.commit()
        connection.close()

        return True

    except sqlite3.IntegrityError:

        connection.close()

        return False


def authentication(username, password):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, username
        FROM users
        WHERE username = ? AND password = ?
    """, (username, password))

    user = cursor.fetchone()

    connection.close()

    return user


def add_student(
    fullname,
    age,
    address,
    contact,
    email,
    course,
    year_level,
    subjects
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO students(
            fullname,
            age,
            address,
            contact,
            email,
            course,
            year_level,
            subjects
        )
        VALUES (?,?,?,?,?,?,?,?)
    """, (
        fullname,
        age,
        address,
        contact,
        email,
        course,
        year_level,
        json.dumps(subjects)
    ))

    connection.commit()

    student_id = cursor.lastrowid

    _add_enrollments(
        cursor,
        student_id,
        (fullname, age, address, contact, email, course, year_level),
        subjects
    )

    connection.commit()

    connection.close()

    return student_id


def get_all_students():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            fullname,
            age,
            address,
            contact,
            email,
            course,
            year_level
        FROM students
        ORDER BY id DESC
    """)

    students = cursor.fetchall()

    connection.close()

    return students


def get_student(student_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            fullname,
            age,
            address,
            contact,
            email,
            course,
            year_level,
            subjects
        FROM students
        WHERE id = ?
    """, (student_id,))

    student = cursor.fetchone()

    connection.close()

    return student


def update_student(
    student_id,
    fullname,
    age,
    address,
    contact,
    email,
    course,
    year_level,
    subjects
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT subjects
        FROM students
        WHERE id = ?
    """, (student_id,))

    old_row = cursor.fetchone()

    old_subjects = []

    if old_row and old_row[0]:

        try:
            old_subjects = json.loads(old_row[0])
        except ValueError:
            old_subjects = []

    cursor.execute("""
        UPDATE students
        SET
            fullname = ?,
            age = ?,
            address = ?,
            contact = ?,
            email = ?,
            course = ?,
            year_level = ?,
            subjects = ?
        WHERE id = ?
    """, (
        fullname,
        age,
        address,
        contact,
        email,
        course,
        year_level,
        json.dumps(subjects),
        student_id
    ))

    added = [
        subject for subject in subjects
        if subject not in old_subjects
    ]

    _add_enrollments(
        cursor,
        student_id,
        (fullname, age, address, contact, email, course, year_level),
        added
    )

    connection.commit()
    connection.close()


def delete_student(student_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM students
        WHERE id = ?
    """, (student_id,))

    connection.commit()
    connection.close()