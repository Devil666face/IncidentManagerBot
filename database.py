import sqlite3
import os
import shutil
from pathlib import Path
from aiogram import types


class Database:
    def __init__(self, db_file_name='database.db') -> None:
        self.db = db_file_name
        self.connection = sqlite3.connect(self.db)
        self.cursor = self.connection.cursor()

    def create_user(self, id, name) -> bool:
        with self.connection:
            try:
                # Пишу запросы через жопу и мне пох
                self.cursor.execute(f"INSERT INTO User (id, name) VALUES ({id}, '{name}');")
                return True
            except Exception as error:
                print(f'[Ошибка добавления пользователя в БД] {error}')
                return False
            finally:
                self.connection.commit()

    def create_incident(self, incedent_text) -> int:
        with self.connection:
            self.cursor.execute(f"INSERT INTO Incidents (text) VALUES (?)", (incedent_text,))
            self.connection.commit()
            self.cursor.execute(f"SELECT id FROM Incidents ORDER BY id DESC LIMIT 1")
            return int(self.cursor.fetchone()[0])

    def add_photos(self, incident_id):
        images = os.listdir(Path(os.getcwd(),incident_id))
        with self.connection:
            for img in images:
                with open(Path(os.getcwd(),incident_id,img),'rb') as photo:
                    self.cursor.execute(f"INSERT INTO Photos (id, Photo) VALUES (?, ?)",(incident_id,photo.read()))
        self.connection.commit()
        shutil.rmtree(Path(os.getcwd(),incident_id))
            
    def get_incidents(self):
        with self.connection:
            self.cursor.execute(f"SELECT id,text FROM Incidents")
            return self.cursor.fetchall()

    def get_current_incident(self, incident_id):
        with self.connection:
            self.cursor.execute(f"SELECT text FROM Incidents WHERE id=?",(incident_id,))
            text = self.cursor.fetchone()
            self.cursor.execute(f"SELECT Photo FROM Photos WHERE id=?",(incident_id,))
            photos = self.cursor.fetchall()
            return text,photos

    def delete_incident(self, incident_id):
        with self.connection:
            self.cursor.execute(f"DELETE FROM Incidents WHERE id=?",(incident_id,))
            self.cursor.execute(f"DELETE FROM Photos WHERE id=?",(incident_id,))
            self.connection.commit()
