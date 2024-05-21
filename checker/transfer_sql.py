import sqlite3
import pandas as pd
import os

def transfer(old_db_path= 'voices_2024-05-21_03-50.db', new_db_path= 'db.sqlite3'):

    conn_ = sqlite3.connect(old_db_path)

    query = "SELECT * FROM audios;"  
    df = pd.read_sql_query(query, conn_)
    conn_.close()
    for i in range(0, len(df)):
        print(df['sentence_id'][i],  df['sentence'][i])

        
    conn = sqlite3.connect(new_db_path)
    cursor = conn.cursor()

    print(len(df))
    for i in range(0, len(df)):
        cursor.execute('''
        INSERT INTO voice_audio (sentence_id, sentence, file_path, status, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)
    ''', (df['sentence_id'][i],  df['sentence'][i],  df['file_name'][i], df['status'][i], df['time'][i], df['time'][i]))


    conn.commit()
    conn.close()
    print("Ma'lumotlar bazasi yaratildi va ma'lumotlar qo'shildi.")


    #open zip and move files
    zip_path = old_db_path.replace('.db', '.zip')
    import zipfile
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall('media/records/')

    os.remove(old_db_path)
    os.remove(zip_path)

transfer()
