import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from src.model import Base 
from sqlalchemy.exc import OperationalError 

load_dotenv()
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "db_taskfy_tp3")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_session():
    """Retorna uma nova instância de sessão do banco de dados."""
    return SessionLocal()

def init_db():
    """
    Cria todas as tabelas (definidas nos modelos) no banco de dados.
    Esta função é segura para ser chamada múltiplas vezes.
    """
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"Erro ao inicializar o banco: {e}")

def check_db_connection():
    """Verifica se a conexão com o banco de dados pode ser estabelecida."""
    print("Verificando conexão com o banco de dados...")
    try:
        db = get_db_session()
        db.execute(text("SELECT 1")) 
        db.close()
        print(f"Conexão com o banco de dados bem-sucedida (Banco: {DB_NAME})")
        return True
    except OperationalError as e:
        print("\n" + "="*50)
        print(f"ERRO FATAL: Não foi possível conectar ao banco de dados.")
        print("1. O servidor PostgreSQL está rodando?")
        print(f"2. As credenciais no arquivo .env estão corretas?")
        print(f"   (Host: {DB_HOST}, Banco: {DB_NAME}, Usuário: {DB_USER})")
        print("="*50 + "\n")
        return False
    except Exception as e:
        print(f"Um erro inesperado ocorreu: {e}")
        return False