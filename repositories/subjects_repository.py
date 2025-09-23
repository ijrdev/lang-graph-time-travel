import sqlite3, pandas as pd

from pandas import DataFrame

class SubjectsRepository():
    def __init__(self):
        pass

    def get_all(self, status: list | None) -> DataFrame:
        connection = sqlite3.connect("/data/db.db", check_same_thread = False)
        
        try:
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
    