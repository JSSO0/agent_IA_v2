from datetime import datetime
from venv import create
from sqlalchemy.ext.declarative import declarative_base
from admin.repository.db_config import  create_db_connection
from psycopg2 import sql

Base = declarative_base()

class IndexDatabaseManager:

    def save_index_metadata(self, client_id, index_name, file_name):
        try:
            conn = create_db_connection()
            cursor = conn.cursor()
            query = sql.SQL("INSERT INTO index_metadata (client_id, index_name, file_name, created_at, updated_at) "
                            "VALUES (%s, %s, %s, %s, %s)")
            cursor.execute(query, (client_id, index_name, file_name, datetime.now(), datetime.now()))
            conn.commit()
            print(f"✅ Metadados do índice '{index_name}' salvos com sucesso no banco de dados.")
        except Exception as e:
            print(f"Erro ao salvar os metadados do índice '{index_name}': {e}")
        finally:
            cursor.close()
            conn.close()
