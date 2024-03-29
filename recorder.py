import os
import wave
import time
import threading
import tkinter as tk
import pyaudio
import sqlite3
from datetime import datetime, timedelta

import numpy as np


### for backup 
import shutil
import zipfile
import asyncio
from aiogram import Bot, types

current_path = os.getcwd()
TOKEN = "6953736915:AAG7kWEKHZFJzssSgu1cPAwaJlwStyDtAAs"

# Chat ID
Chat_ID = "-1002115614399"
Message_ID = "2"

MEDIA_PATH = os.path.join(current_path, 'records')
DB_PATH = os.path.join(current_path, 'voices.db')

bot = Bot(token=TOKEN)

### RECORD REQUIREMENTS
RECORD_RATE = 44100 # Hz
RECORD_SECONDS = 5
RECORD_CHANNELS = 1 # Mono Audio
RECORD_FRAME_BUFFER = 1024
RECORD_FORMAT = pyaudio.paInt16


async def send_media(chat, thread_id):  
    # List of files to send
    file_list = []
    current_zip_size = 0
    zip_file_index = 1

    for root, dirs, files in os.walk(MEDIA_PATH):
        for file in files:
            file_path = os.path.join(root, file)
            file_size = os.path.getsize(file_path)

            # If adding the file exceeds the limit, create a new zip file
            if current_zip_size + file_size > 60 * 1024 * 1024:
                # print("sending files")
                await send_zip(chat, file_list, zip_file_index, thread_id)
                # print("ok send file")
                file_list = []
                zip_file_index += 1
                current_zip_size = 0

            file_list.append(file_path)
            current_zip_size += file_size

    # Send the remaining files
    if file_list:
        await send_zip(chat, file_list, zip_file_index, thread_id)

# Zip faylni yuborish funksiyasi
async def send_zip(chat, file_list, index, thread_id):
    time = datetime.now().strftime("%Y-%m-%d_%H-%M")
    zip_file_path = os.path.join(current_path, f"voices_{time}_{index}.zip")
        
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in file_list:
            zipf.write(file_path, os.path.relpath(file_path, MEDIA_PATH))
            os.remove(file_path)
            

    with open(zip_file_path, "rb") as zip_file:
        await bot.send_document(chat_id=chat, document=zip_file, message_thread_id=thread_id )

    os.remove(zip_file_path)
    
async def backup_database(chat, thread_id):
    print("okssdf")
    zip_file_path = os.path.join(current_path, f"voices_database.zip")
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(DB_PATH)
            

    with open(zip_file_path, "rb") as zip_file:
        await bot.send_document(chat_id=chat, document=zip_file, message_thread_id=thread_id )

    os.remove(zip_file_path)
    
   
async def main():
    await backup_database(Chat_ID, Message_ID)
    await send_media(Chat_ID, Message_ID)
    session = await bot.get_session()
    await session.close()
    print("ok")


# if __name__ == "__main__":
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(main())
#     asyncio.get_event_loop().run_until_complete(backup_database(Chat_ID, Message_ID))
#     print("okssdf")
    



 

def update_audio_status(db_path, file_name, new_status):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    current_time = datetime.utcnow() + timedelta(hours=5)  # UTC+5

    # Jadvaldagi ma'lumotni yangilash
    cursor.execute('''
        UPDATE audios SET status = ?, date = ? WHERE file_name = ?
    ''', (new_status, current_time, file_name))

    conn.commit()
    conn.close()

def get_unread_audio(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM audios WHERE status = 'unread' LIMIT 1;")
    audio = cursor.fetchone()

    conn.close()

    return audio

class VoiceRecorder:
    def __init__(self):
        self.check_audio_files()
        self.initialize_audio_data()
        self.initialize_gui()

    def initialize_gui(self):
        self.root = tk.Tk()
        self.root.resizable(True, True)
        self.root.title("Voice Recorder")
        self.root.geometry("1080x720")

        self.create_frames()
        self.create_widgets()

        self.is_recording = False
        self.root.mainloop()

    def initialize_audio_data(self):
        self.db_path = "voices.db"
        self.sentence_db = get_unread_audio(self.db_path)
        self.devices = self.get_audio_devices()
        self.selected_device = self.get_default_audio_device()

    def create_frames(self):
        self.topframe = tk.Frame(self.root)
        self.topframe.pack(side='top', expand=False, fill='x', anchor='center', padx=10, pady=10)

        self.centerframe = tk.Frame(self.root)
        self.centerframe.pack(side='bottom', expand=False, fill='x', anchor='center', padx=10, pady=10)

        self.recorder_time_frame = tk.Frame(self.centerframe)
        self.recorder_time_frame.pack(side='top')

        self.bottomframe = tk.Frame(self.centerframe, bd=1, relief='solid')
        self.bottomframe.pack(side='bottom')

    def create_widgets(self):
        self.create_sentence_label()
        self.create_send_audios_button()
        self.create_recording_button()
        self.create_next_sentence_button()
        self.create_timer_labels()

    def create_sentence_label(self):
        sentence_text = self.sentence_db[2]
        self.sentence = tk.Label(self.topframe, text=sentence_text, justify='center', wraplength=850, font=('Times New Roman', 24))
        self.sentence.pack(expand=True, padx=10, pady=20, anchor='center', side='top')

    def create_send_audios_button(self):
        self.send_audios_btn = tk.Button(self.recorder_time_frame, text="Send Audios", font=('Arial', 10, 'bold'),
                                         command=self.send_audios_func, cursor='hand2')
        self.send_audios_btn.pack(side='left', ipadx=10, ipady=10, anchor='center', padx=10, pady=50)

    def create_recording_button(self):
        self.record_button = tk.Button(self.recorder_time_frame, text="🎤 ", font=('Arial', 50, 'bold'),
                                       command=self.recording_button, border=5, width=4, height=1, cursor='hand2',
                                       fg='black', justify='center')
        self.record_button.pack(fill='both', expand=True, padx=10, pady=20, side='left')

    def create_next_sentence_button(self):
        self.next_sentence_button = tk.Button(self.recorder_time_frame, text="Next Sentence", font=('Arial', 10, 'bold'),
                                              command=self.next_sentence_func, cursor='hand2')
        self.next_sentence_button.pack(side='right', ipadx=10, ipady=10, anchor='center', padx=10, pady=20)

    def create_timer_labels(self):
        self.timer_label = tk.Label(self.centerframe, text="00:00:00")
        self.timer_label.pack(padx=10, pady=20, side='bottom', anchor='center')

        self.audio_timer_label = tk.Label(self.bottomframe, text="00:00:00 1")
        self.audio_timer_label.pack(fill='both', expand=True, padx=10, pady=20, side='bottom')

    def check_audio_files(self):
        if not os.path.exists("records"):
            os.mkdir("records")
        
    def get_audio_devices(self):
        audio = pyaudio.PyAudio()
        devices = []
        for i in range(audio.get_device_count()):
            device_info = audio.get_device_info_by_index(i)
            devices.append(device_info['name'])
        audio.terminate()
        return devices
    
    def get_default_audio_device(self):
        audio = pyaudio.PyAudio()
        default_device_index = audio.get_default_input_device_info()['index']
        default_device_name = audio.get_device_info_by_index(default_device_index)['name']
        audio.terminate()
        return default_device_name
    
    def recording_button(self):
        if self.is_recording:
            self.is_recording = False
            self.record_button.config(text="🎤 ", fg='black')
            self.next_sentence_func('read')
        else:
            self.is_recording = True
            self.record_button.config(text="⏹", fg='red')
            threading.Thread(target=self.record).start()
            
    def record(self):
        audio = pyaudio.PyAudio()
        
        selected_index = self.devices.index(self.selected_device)  # Tanlangan qurilma indeksini topish
        stream = audio.open(format=RECORD_FORMAT, channels=RECORD_CHANNELS, rate=RECORD_RATE,
                            input=True, frames_per_buffer=RECORD_FRAME_BUFFER,
                            input_device_index=selected_index)  # Tanlangan qurilmani ishlatish
        
        frames = []
        start_time = time.time()
        while self.is_recording:
            data = stream.read(RECORD_FRAME_BUFFER)
            frames.append(data)
            self.timer_label.config(text=time.strftime('%H:%M:%S', time.gmtime(time.time()-start_time)))
            self.root.update()
        
        stream.stop_stream()
        stream.close()
        audio.terminate()
        
        # exists = True
        # i = 1
        
        # while exists:
        #     filename = f"output_{i}.wav"
        #     exists = os.path.exists(filename)
        #     i += 1
        
        filename = self.sentence_db[1]
            
        sound_file = wave.open(f'records/{filename}', 'wb')
        sound_file.setnchannels(RECORD_CHANNELS)
        sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        sound_file.setframerate(RECORD_RATE)
        sound_file.writeframes(b''.join(frames))
        sound_file.close()
        
        self.timer_label.config(text="00:00:00")
        
     
    
    def next_sentence_func(self, status='skip'):
        update_audio_status(self.db_path, self.sentence_db[1], status)
        self.sentence_db = get_unread_audio(self.db_path)
        self.sentence.config(text=self.sentence_db[2])
    
        
    def send_audios_func(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
        
VoiceRecorder()


    
    
    