import sqlite3, pandas as pd

from sqlite3 import Connection

from pandas import DataFrame

class CheckpointsRepository():
    @classmethod
    def get(cls, id: str, thread_id: str) -> DataFrame:
        connection: Connection | None = None
        
        try:
            connection = sqlite3.connect("data/db.db", check_same_thread = False)
            
            query: str = f"SELECT *, ROWID FROM checkpoints WHERE checkpoint_id = ? AND thread_id = ? ORDER BY ROWID DESC LIMIT 1"
            
            return pd.read_sql_query(query, connection, params = (id, thread_id))
        except Exception as ex:
            raise ex
        finally:
            if connection:
                connection.close()
    