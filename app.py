from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, make_response, session, abort
from database import connect, get_task, get_observations, save_observation_to_db, get_user_name
import datetime
from math import ceil

app = Flask(__name__)
app.secret_key = '@pCz+W^xg6f#vA!U~Y6nQm]m#_6B'

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT id, password FROM users WHERE username=%s", (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user and password == user[1]:
        session['user_id'] = user[0]
        return redirect(url_for('list_tasks', page=1))
    else:
        flash('Usuário ou senha incorretos')
        return redirect(url_for('index'))

@app.route('/tasks/page/<int:page>', methods=['GET'])
def list_tasks(page=1):
    user_id = session.get('user_id')
    if user_id:
        user_name = get_user_name(user_id)
    else:
        user_name = None

    tasks_per_page = 10
    offset = (page - 1) * tasks_per_page

    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE tasks.status = 'Aberta'")
    total_tasks = cursor.fetchone()[0]
    total_pages = ceil(total_tasks / tasks_per_page) if total_tasks > tasks_per_page else 1

    cursor.execute("""
        SELECT tasks.id, tasks.title, tasks.task_type, tasks.priority, tasks.created_at, users.username
        FROM tasks
        JOIN users ON tasks.responsible_id = users.id
        WHERE tasks.status = 'Aberta' 
        ORDER BY tasks.id
        LIMIT %s OFFSET %s
    """, (tasks_per_page, offset))
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('list_tasks.html', tasks=tasks, total_pages=total_pages, current_page=page, user_name=user_name)

@app.route('/create_task', methods=['GET', 'POST'])
def create_task():
    if request.method == 'POST':
        return redirect(url_for('list_tasks', page=1))
    return render_template('create_task.html')

@app.route('/tasks', methods=['POST'])
def save_task():
    task_data = request.get_json()

    title = task_data['title']
    task_type = task_data['task_type']
    priority = task_data['priority']
    created_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    description = task_data['description']
    status = 'Aberta'
    creator_id = session.get('user_id', 1)
    responsible_id = creator_id


    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (title, task_type, priority, created_at, description, status,  creator_id, responsible_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        (title, task_type, priority,  created_at, description, status, creator_id, responsible_id),
    )
    conn.commit()
    cursor.close()
    conn.close()

    return make_response(jsonify({}), 201)

@app.route('/tasks')
def get_tasks():
    page = int(request.args.get('page', 1))
    tasks = []
    total_tasks = 0

    return jsonify(tasks=tasks, total_tasks=total_tasks)

@app.route('/task/<int:task_id>')
def task_details(task_id):
    task = get_task(task_id)
    if not task:
        return "Tarefa não encontrada", 404

    user_id = None
    user_name = None
    if 'user_id' in session:
        user_id = session['user_id']
        user_name = get_user_name(user_id)

    observations = get_observations(task_id)
    creator_name = task["creator_name"]
    return render_template('task_details.html', task=task, observations=observations, user_id=user_id, user_name=user_name, creator_name=creator_name)


@app.route('/task/<int:task_id>/save', methods=['POST'])
def save_task_observation(task_id):
    task = get_task(task_id)
    if not task:
        abort(404)

    observation_text = request.form['text']
    task_status = request.form.get('task_status', None)

    user_id = session.get('user_id', 1)

    if task_status:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE tasks
            SET status = %s
            WHERE id = %s
        """, (task_status, task_id))
        conn.commit()
        cursor.close()
        conn.close()

    save_observation_to_db(task_id, user_id, observation_text, action='alterou_status')

    return redirect(url_for('list_tasks', page=1))


@app.route('/task/<int:task_id>/assume', methods=['POST'])
def assume_task(task_id):
    user_id = session.get('user_id', 1)
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET responsible_id = %s WHERE id = %s", (user_id, task_id))
    conn.commit()
    cursor.close()
    conn.close()

    return make_response(jsonify({}), 200)

@app.route('/tasks/complete/<int:task_id>', methods=['PUT'])
def complete_task(task_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET status = 'Concluída' WHERE id = %s", (task_id,))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'status': 'success'}), 200


if __name__ == '__main__':
    app.run(debug=True)
