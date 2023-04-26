from datetime import datetime

import psycopg2
import datetime

def connect():
    return psycopg2.connect(
        host="localhost",
        port="5432",
        database="Sistema",
        user="postgres",
        password="ppedro23"
    )

def fetch_tasks():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT tasks.*, users.username
        FROM tasks
        LEFT JOIN users ON tasks.responsible_id = users.id
    """)
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()

    return tasks


def get_task(task_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT tasks.*, u.username as responsible_name, c.username as creator_name
        FROM tasks
        LEFT JOIN users u ON tasks.responsible_id = u.id
        LEFT JOIN users c ON tasks.creator_id = c.id
        WHERE tasks.id = %s
    """, (task_id,))
    task = cursor.fetchone()
    cursor.close()
    conn.close()

    if task:
        task_dict = {
            "id": task[0],
            "title": task[1],
            "task_type": task[2],
            "priority": task[3],
            "description": task[4],
            "status": task[5],
            "created_at": task[6],
            "responsible_id": task[7],
            "creator_id": task[8],
            "finished_at": task[9],
            "responsible_name": task[10],
            "creator_name": task[11],
        }
        return task_dict
    return None

def get_observations(task_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, task_id, user_id, content, created_at::timestamp
        FROM task_observations
        WHERE task_id = %s
        ORDER BY created_at DESC
    """, (task_id,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()

    observations = []
    for row in result:
        observations.append({
            'id': row[0],
            'task_id': row[1],
            'user_id': row[2],
            'content': row[3],
            'created_at': row[4]
        })

    return observations

def get_user_name(user_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user:
        return user[0]
    return None


def save_observation_to_db(task_id, user_id, text, action=None, status=None):
    conn = connect()
    cursor = conn.cursor()
    current_timestamp = datetime.datetime.now()
    cursor.execute("""
        INSERT INTO task_observations (task_id, user_id, content, created_at)
        VALUES (%s, %s, %s, %s)
    """, (task_id, user_id, text, current_timestamp))

    if status:
        cursor.execute("""
            UPDATE tasks
            SET status = %s
            WHERE id = %s
        """, (status, task_id))

    conn.commit()
    cursor.close()
    conn.close()

