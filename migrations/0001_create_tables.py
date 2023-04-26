from database import connect

def up(conn):
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            task_type VARCHAR(50) NOT NULL,
            priority VARCHAR(50) NOT NULL,
            description TEXT NOT NULL,
            status VARCHAR(50) NOT NULL,
            created_at TIMESTAMP NOT NULL,
            updated_at TIMESTAMP,
            creator_id INTEGER REFERENCES users(id),
            responsible_id INTEGER REFERENCES users(id)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS task_observations (
            id SERIAL PRIMARY KEY,
            content TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL,
            user_id INTEGER REFERENCES users(id),
            task_id INTEGER REFERENCES tasks(id)
        );
    """)

    conn.commit()
    cursor.close()

