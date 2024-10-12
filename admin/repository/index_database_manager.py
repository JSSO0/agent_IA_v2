from datetime import datetime
from venv import create
from sqlalchemy.ext.declarative import declarative_base
from admin.repository.db_config import  create_db_connection
import psycopg2
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

    def get_index_file_name(self, index_name, client_id):
        query = "SELECT file_name FROM index_metadata WHERE index_name = %s AND client_id = %s"
        try:
            conn = create_db_connection()  # Crie a conexão conforme mostrado anteriormente
            cursor = conn.cursor()
            cursor.execute(query, (index_name, client_id))
            result = cursor.fetchone()
            if not result:
                raise ValueError(f"Metadados do índice '{index_name}' não encontrados para o cliente {client_id}.")
            return result[0]  # Retorna o primeiro valor da tupla (nome do arquivo)
        except Exception as e:
            print(f"Erro ao carregar metadados do índice '{index_name}': {e}")
        finally:
            cursor.close()
            conn.close()

    def load_index_from_db(self, index_id):
        query = "SELECT * FROM index_metadata WHERE id = %s"
        try:
            conn = create_db_connection()  # Crie a conexão conforme mostrado anteriormente
            cursor = conn.cursor()
            cursor.execute(query, (index_id,))
            result = cursor.fetchone()
            if not result:
                raise ValueError(f"Índice com ID '{index_id}' não encontrado.")
            print(
                f"✅ Índice '{result[1]}' carregado com sucesso do banco de dados.")  # Assume que o nome do índice está na segunda posição da tupla
            return result
        except Exception as e:
            print(f"Erro ao carregar índice com ID '{index_id}': {e}")
        finally:
            cursor.close()
            conn.close()

