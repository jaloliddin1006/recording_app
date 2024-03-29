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
db_path = "voices2.db"

def create_table():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Jadvalni yaratish
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name VARCHAR,
            sentence VARCHAR,
            status VARCHAR DEFAULT 'unread',
            date DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()
    
    
def insert_audio(file_name, sentence):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Vaqtzonani olish

    # Jadvalga ma'lumot qo'shish
    cursor.execute('''
        INSERT INTO audios (file_name, sentence) VALUES (?, ?)
    ''', (file_name, sentence))

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

# Ma'lumotlarni olish


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
for i in range(0, 500):
    # print(df['wavfile'][i], df['text'][i])
    # insert_audio(df['wavfile'][i], df['text'][i])
    cursor.execute('''
    INSERT INTO audios (file_name, sentence) VALUES (?, ?)
''', (df['wavfile'][i],  df['text'][i]))


conn.commit()
conn.close()
