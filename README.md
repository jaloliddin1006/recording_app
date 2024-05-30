# recording_app
TTS uchun yasalgan desktop app

> db ni olish uchun `db.py` faylni ishga tushirish kerak. Bu `voices.db` nomli db yaratadi. keyin esa .exe(py -> exe) dasturni yaratish kerak


## .py to .exe steps
- install package:
  - `pip install pyinstaller`
- converT file: 
  - `pyinstaller recorder.py --onefile -w`

| buni ishga tushurishdan oldin windowsning security qismini o'chirib qo'yish kerak!

| so'ng .exe dastur `dist/` papkasini ichida joylashadi
