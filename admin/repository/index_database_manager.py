from datetime import datetime
from venv import create

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy import text
from admin.repository.db_config import SessionLocal
import psycopg2
from psycopg2 import sql

Base = declarative_base()
"""
class IndexMetadataModel(Base):
    __tablename__ = "index_metadata"

    id = Column(String, primary_key=True, index=True)
    client_id = Column(Integer, nullable=False)
    index_name = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    created_at = Column(String, nullable=False)
    updated_at = Column(String, nullable=False)

class IndexModel(Base):
    __tablename__ = "indices"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    index_data = Column(JSONB, nullable=False)  # Usar o tipo JSONB do SQLAlchemy
    created_at = Column(String, nullable=False)
    updated_at = Column(String, nullable=False)
 """
class IndexDatabaseManager:
    def __init__(self):
        self.db_session = SessionLocal()

    def save_index_metadata(self, client_id, index_name, file_name):
        try:
            conn = psycopg2.connect(
                host="localhost",  # Substitua pelo seu host
                database="agent_avant",  # Substitua pelo nome do seu banco de dados
                user="postgres",  # Substitua pelo seu usuário
                password="1234"  # Substitua pela sua senha
            )

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
    """
    def save_index_metadata(self, client_id, index_name, file_name):
        query = text(f"INSERT INTO index_metadata (client_id, index_name, file_name, created_at, updated_at) "
                     f"VALUES (:client_id, :index_name, :file_name, :created_at, :updated_at)")
        print(client_id)
        print(index_name)
        print(file_name)

        try:
            self.db_session.execute(query, {
                'client_id': '1234',
                'index_name': 'default_index',
                'file_name': 'default_index.pkl',
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            })
            self.db_session.commit()
            print(f"✅ Metadados do índice '{index_name}' salvos com sucesso no banco de dados. Valores '{client_id}', '{file_name}', '{datetime.now().isoformat()}'")
        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise ValueError(f"Erro ao salvar os metadados do índice '{index_name}' no banco de dados: {e}")
        except Exception as e:
            self.db_session.rollback()
            raise ValueError(f"Erro ao salvar os metadados do índice '{index_name}'. Valores '{client_id}', '{file_name}', '{datetime.now().isoformat()}': {e}")
        except IntegrityError as e:
            self.db_session.rollback()
            raise ValueError(f"Erro de integridade ao salvar os metadados do índice '{index_name}': {e}")
        finally:
            self.db_session.close()

  
    def save_index_to_db(self, name, index_json):
        if not isinstance(index_json, (bytes, bytearray)):
            raise ValueError("Os dados do índice devem ser binários.")
        index_entry = IndexModel(
            client_id=1,  # Defina o client_id correto ou ajuste conforme necessário
            name=name,
            index_data=index_json.encode('utf-8'),  # Salvar o JSON como binário
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )
        print(f"Tentando salvar no banco: client_id={index_entry.client_id}, "
              f"name={index_entry.name}, created_at={index_entry.created_at}, "
              f"updated_at={index_entry.updated_at}, index_data_tamanho={len(index_entry.index_data)}")
        try:
            self.db_session.add(index_entry)
            self.db_session.commit()
            self.db_session.refresh(index_entry)
            print(f"✅ Índice '{name}' salvo com sucesso no banco de dados.")
            return index_entry
        except IntegrityError as e:
            self.db_session.rollback()
            raise ValueError(f"Erro de integridade ao tentar salvar o índice '{name}' no banco de dados: {e}")
        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise ValueError(f"Erro de banco de dados ao tentar salvar o índice '{name}': {e}")
        except Exception as e:
            self.db_session.rollback()
            raise ValueError(f"Erro inesperado ao salvar o índice '{name}': {e}")


    def get_index_file_name(self, index_name, client_id):
       
        try:
            index_entry = self.db_session.query(IndexMetadataModel).filter_by(
                index_name=index_name,
                client_id=client_id
            ).first()
            if not index_entry:
                raise ValueError(f"Metadados do índice '{index_name}' não encontrados para o cliente {client_id}.")
            return index_entry.file_name
        except SQLAlchemyError as e:
            raise ValueError(f"Erro ao carregar metadados do índice '{index_name}': {e}")
        finally:
            self.db_session.close()



    def load_index_from_db(self, index_id):

        # Buscar o índice no banco de dados pelo ID
        index_entry = self.db_session.query(IndexModel).filter(IndexModel.id == index_id).first()
        if not index_entry:
            raise ValueError(f"Índice com ID '{index_id}' não encontrado.")
        print(f"✅ Índice '{index_entry.name}' carregado com sucesso do banco de dados.")
        return index_entry

    def close(self):
        self.db_session.close()
"""