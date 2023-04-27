from flask import Flask,render_template,request,redirect
import sqlite3
from datetime import datetime

app = Flask("__main__")


# Set up the database
def connect_db():
    conn = sqlite3.connect('tasks.db')
    return conn

def create_table():
    conn = connect_db()
    conn.execute('''CREATE TABLE IF NOT EXISTS tasks
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 task TEXT NOT NULL,
                 date_created TEXT NOT NULL,
                 time_created TEXT NOT NULL)''')
    conn.commit()
    conn.close()
    
    
def add_task_to_db(task):
    conn = connect_db()
    date_created = datetime.now().strftime("%Y-%m-%d")
    time_created = datetime.now().strftime("%H:%M:%S")
    conn.execute("INSERT INTO tasks (task, date_created, time_created) VALUES (?, ?, ?)",
                 (task, date_created, time_created))
    conn.commit()
    conn.close()
    
def get_all_tasks():
    conn = connect_db()
    cursor = conn.execute("SELECT id, task, date_created, time_created FROM tasks")
    tasks = []
    for row in cursor:
        task = {"id": row[0], "task": row[1], "date_created": row[2], "time_created": row[3]}
        tasks.append(task)
    conn.close()
    return tasks

def delete_task(id):
        conn = connect_db()
        conn.execute("DELETE FROM tasks WHERE id=?", (id,))
        conn.commit()
        conn.close()


@app.route("/",methods=["POST","GET"])
def home():
    if request.method == "POST":
        task =request.form.get("task")
        #tasks.insert(0,task)
        add_task_to_db(task)
        tasks = get_all_tasks()
        return render_template("home.html",tasks=tasks)
    else:
        tasks = get_all_tasks()
        return render_template("Home.html",tasks=tasks)

@app.route("/update",methods=["POST","GET"])
def update():
    if request.method == "POST":
        return "<h1>Update clicked</h1>"
    else:
        tasks = get_all_tasks()
        return render_template("Home.html",tasks=tasks)
    
    
@app.route("/delete/<int:id>",methods=["POST","GET"])
def delete(id):
    if request.method == "POST":
        delete_task(id)
        return redirect("/")
    else:
        tasks = get_all_tasks()
        return render_template("Home.html",tasks=tasks)

if __name__ == "__main__":
    create_table()
    app.run(debug=True)
