import sqlite3

DB_NAME = "student.db"


def connect():
    return sqlite3.connect(DB_NAME)


def create_table():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS student (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            age INTEGER,
            sexe TEXT,
            etude REAL,
            sommeil REAL,
            distraction REAL,
            env INTEGER,
            assiduite INTEGER,
            ponctualite INTEGER,
            discipline INTEGER,
            tache INTEGER,
            niveau TEXT,
            moyenne REAL
        )
    """)

    conn.commit()
    conn.close()


def insert_student(data_tuple):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO student (
            age, sexe, etude, sommeil, distraction,
            env, assiduite, ponctualite, discipline,
            tache, niveau, moyenne
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, data_tuple)

    conn.commit()
    conn.close()
