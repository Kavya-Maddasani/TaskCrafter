import sqlite3
import os

def create_tables():
    # Use environment variable for DB path or fallback to local
    connection = sqlite3.connect(os.getenv("DB_PATH", "taskcrafter.db"))
    cursor = connection.cursor()

    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    cursor.execute('''
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    task_name TEXT NOT NULL,
    description TEXT,
    estimated_time INTEGER NOT NULL,
    priority INTEGER DEFAULT 1,
    is_completed INTEGER DEFAULT 0,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    start_time TEXT,
    is_paused INTEGER DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users (id)
)
''')

    # Create task_logs table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS task_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id INTEGER NOT NULL,
        actual_time INTEGER NOT NULL,
        completed_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (task_id) REFERENCES tasks(id)
    )
    ''')

    # Create user_stats table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_stats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        tasks_completed INTEGER DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES users(id),
        UNIQUE(user_id, date)
    )
    ''')

    # Create completed_tasks table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS completed_tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    task_name TEXT NOT NULL,
    description TEXT,
    estimated_time INTEGER NOT NULL,
    actual_time INTEGER,
    start_time TEXT,  -- ✅ added column
    created_at TEXT,
    completed_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
''')


    connection.commit()
    connection.close()
    print("All tables created successfully!")

if __name__ == '__main__':
    create_tables()
