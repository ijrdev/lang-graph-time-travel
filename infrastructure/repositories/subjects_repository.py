import sqlite3, pandas as pd, uuid

from datetime import datetime
from sqlite3 import Connection, Cursor

from pandas import DataFrame

from application.enums.status_enum import StatusEnum

class SubjectsRepository():
    @classmethod
    def create_table(cls) -> None:
        connection: Connection | None = None
        
        try:
            try:
                connection = sqlite3.connect("../../data/db.db", check_same_thread = False)
            except Exception as ex:
                connection = sqlite3.connect("data/db.db", check_same_thread = False)
            
            cursor: Cursor = connection.cursor()
            
            query: str = """
                CREATE TABLE IF NOT EXISTS subjects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    thread_id TEXT NOT NULL UNIQUE,
                    created_at DATETIME NOT NULL,
                    updated_at DATETIME NULL,
                    subject TEXT NOT NULL,
                    status TEXT NOT NULL
                )
            """
            
            cursor.execute(query)
            
            connection.commit()
        except Exception as ex:
            raise ex
        finally:
            if connection:
                connection.close()
    
    @classmethod
    def add(cls, subject: str) -> None:
        connection: Connection | None = None
        
        try:
            try:
                connection = sqlite3.connect("../../data/db.db", check_same_thread = False)
            except Exception as ex:
                connection = sqlite3.connect("data/db.db", check_same_thread = False)
            
            cursor: sqlite3.Cursor = connection.cursor()
            
            query: str = """
                INSERT INTO subjects (thread_id, created_at, updated_at, subject, status)
                VALUES (?, ?, ?, ?, ?)
            """
            
            cursor.execute(query, (str(uuid.uuid4()), datetime.now().isoformat(), None, subject, StatusEnum.PENDING.value,))
            
            connection.commit()
        except Exception as ex:
            print(ex)
            raise ex
        finally:
            if connection:
                connection.close()
    
    @classmethod
    def update(cls, id: int, subject: str, status: str | None) -> None:
        connection: Connection | None = None
        
        try:
            try:
                connection = sqlite3.connect("../../data/db.db", check_same_thread = False)
            except Exception as ex:
                connection = sqlite3.connect("data/db.db", check_same_thread = False)
            
            cursor: Cursor = connection.cursor()
            
            query: str = "UPDATE subjects"
            params: tuple = ()
                 
            if status:
                params += (subject, datetime.now().isoformat(), status, id)
                query += " SET subject = ?, updated_at = ?, status = ?"
            else:
                params += (subject, datetime.now().isoformat(), id)
                query += " SET subject = ?, updated_at = ?"
            
            query += " WHERE id = ?"
            
            cursor.execute(query, params)
            
            connection.commit()
        except Exception as ex:
            raise ex
        finally:
            if connection:
                connection.close()
    
    @classmethod
    def delete(cls, id: int) -> None:
        connection: Connection | None = None
        
        try:
            try:
                connection = sqlite3.connect("../../data/db.db", check_same_thread = False)
            except Exception as ex:
                connection = sqlite3.connect("data/db.db", check_same_thread = False)
            
            cursor: Cursor = connection.cursor()
            
            query: str = "DELETE FROM subjects WHERE id = ?"
            
            cursor.execute(query, (id,))
            
            connection.commit()
        except Exception as ex:
            raise ex
        finally:
            if connection:
                connection.close()
    
    @classmethod
    def get_all(cls, status: list | None = None) -> DataFrame:
        connection: Connection | None = None
        
        try:
            try:
                connection = sqlite3.connect("../../data/db.db", check_same_thread = False)
            except Exception as ex:
                connection = sqlite3.connect("data/db.db", check_same_thread = False)
            
            query: str = f"SELECT * FROM subjects"
            params: tuple = ()
            
            if status:
                placeholders: str = ", ".join("?" * len(status))
                query += f" WHERE status IN ({placeholders})"
                params = tuple(status)
            
            query += f" ORDER BY created_at DESC"
            
            return pd.read_sql_query(query, connection, params = params)
        except Exception as ex:
            raise ex
        finally:
            if connection:
                connection.close()
    