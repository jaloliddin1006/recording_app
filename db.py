import pandas as pd
import sqlite3

sqlite_file = "database.db"
conn_ = sqlite3.connect(sqlite_file)

query = "SELECT * FROM dataset;"  
df = pd.read_sql_query(query, conn_)
conn_.close()

# print(df.head() )


import sqlite3
from datetime import datetime, timedelta

# Ma'lumotlar bazasi faylini yo'l
db_path = "voices.db"

def create_table():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Jadvalni yaratish
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sentence_id VARCHAR,
            sentence VARCHAR,
            file_name VARCHAR NULL,
            status VARCHAR DEFAULT 'unread',
            time DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()
    
    


def update_audio_status(file_name, new_status):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    current_time = datetime.utcnow() + timedelta(hours=5)  # UTC+5

    # Jadvaldagi ma'lumotni yangilash
    cursor.execute('''
        UPDATE audios SET status = ?, date = ? WHERE file_name = ?
    ''', (new_status, current_time, file_name))

    conn.commit()
    conn.close()

def get_unread_audio():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM audios WHERE status = 'unread' LIMIT 1;")
    audio = cursor.fetchone()

    conn.close()

    return audio


def get_all_read_audio():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM audios WHERE status = 'read';")
    audios = cursor.fetchall()

    # delete all read audios
    cursor.execute("DELETE FROM audios WHERE status = 'read';")
    conn.commit()


    conn.close()


    return audios

def create_new_sql_db_and_insert(path, audios):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()

    # Jadvalni yaratish
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sentence_id VARCHAR,
            sentence VARCHAR,
            file_name VARCHAR,
            status VARCHAR ,
            time DATETIME
        )
    ''')

    for audio in audios:
        cursor.execute('''
            INSERT INTO audios (sentence_id, sentence, file_name, status, time) VALUES (?, ?, ?, ?, ?)
        ''', (audio[1], audio[2], audio[3], audio[4], audio[5]))

    conn.commit()
    conn.close()

    print("Ma'lumotlar bazasi yaratildi va ma'lumotlar qo'shildi.")
    # Ma'lumotlarni olish


# audios = get_all_read_audio()
# create_new_sql_db_and_insert("new_database.db", audios)



# # Jadvalni yaratish
create_table()

# # Ma'lumot qo'shish
# insert_audio("audio4.mp3", "Salom, dunyo!")

# # Ma'lumotni yangilash
# update_audio_status("audio3.mp3", "skip")

# unread_audio = get_unread_audio()
# print(unread_audio)  # Uni ekranga chiqaring

















conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Vaqtzonani olish

# Jadvalga ma'lumot qo'shish


print(len(df))
for i in range(0, len(df)):
    # print(df['sentence_id'][i],  df['sentence'][i])
    # insert_audio(df['wavfile'][i], df['text'][i])
    cursor.execute('''
    INSERT INTO audios (sentence_id, sentence) VALUES (?, ?)
''', (df['sentence_id'][i],  df['sentence'][i]))


conn.commit()
conn.close()
