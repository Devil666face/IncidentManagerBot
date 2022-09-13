from datetime import datetime
import os
from datetime import datetime
from pathlib import Path
from aiogram.dispatcher.filters.state import State, StatesGroup

class StateBot(StatesGroup):
    get_text = State()
    get_photo = False
    created_id : int

def make_dir(created_id):
    os.makedirs(Path(os.getcwd(),str(created_id)),exist_ok=True)
    count_photo = len(os.listdir(Path(os.getcwd(),str(created_id))))
    return count_photo+1

# def save_photo_from_blob(data):
#     file_name = f"{datetime.now().microsecond}.jpg"
#     with open(file_name,'wb') as photo:
#         photo.write(data)
#     return file_name