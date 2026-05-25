import sqlite3
import yaml
from contextlib import contextmanager

def load_config():
    with open('config.yaml', 'r') as f:
        return yaml.safe_load(f)
    
config = load_config()
DB_PATH = config['database']['path']

@contextmanager
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()