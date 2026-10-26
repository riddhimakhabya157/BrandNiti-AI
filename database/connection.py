"""Database connection management for BrandNiti AI."""
import os
import sqlite3
from pathlib import Path
from contextlib import contextmanager

DEFAULT_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "brandniti.db")

def get_db_path() -> str:
    return os.environ.get("BRANDNITI_DB_PATH", DEFAULT_DB_PATH)

def init_db_dir():
    db_path = get_db_path()
    Path(os.path.dirname(os.path.abspath(db_path))).mkdir(parents=True, exist_ok=True)

@contextmanager
def get_db_connection():
    init_db_dir()
    db_path = get_db_path()
    conn = sqlite3.connect(db_path, timeout=15.0)
    conn.row_factory = sqlite3.Row
    # Enforce foreign key constraints
    conn.execute("PRAGMA foreign_keys = ON;")
    # WAL journal mode for concurrent read/write reliability
    conn.execute("PRAGMA journal_mode = WAL;")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
