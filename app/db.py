import sqlite3

DB_PATH = "observation.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS llm_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            request_id TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            model_name TEXT NOT NULL,
            prompt TEXT NOT NULL,
            duration REAL NOT NULL,
            status TEXT NOT NULL,
            token_count INTEGER DEFAULT 0,
            error_message TEXT
        )
    """)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Observability database initialized successfully!")