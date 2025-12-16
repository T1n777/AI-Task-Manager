from database import connect

def add_task(title, description, deadline, priority):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO tasks VALUES (NULL, ?, ?, ?, ?, ?)",
        (title, description, deadline, priority, "pending")
    )

    conn.commit()
    conn.close()

def get_tasks():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks")
    tasks = cur.fetchall()
    conn.close()
    return tasks

def mark_done(task_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("UPDATE tasks SET status='done' WHERE id=?", (task_id,))
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()
