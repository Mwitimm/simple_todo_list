from flask import Flask,render_template,request,redirect,url_for
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
        
def get_task_by_id(id):
       conn = connect_db()
       cur = conn.cursor()
       cur.execute("SELECT * FROM tasks WHERE id=?", (id,))
       task = cur.fetchone()
       conn.close()
       return task
    
        
def update_task(id,task):
        conn = connect_db()
        conn.execute("UPDATE tasks SET task=? WHERE id=?", (task, id))
        conn.commit()
        conn.close()


@app.route("/",methods=["POST","GET"])
def home():
    if request.method == "POST":
        task =request.form.get("task")
        #tasks.insert(0,task)
        add_task_to_db(task)
        tasks = get_all_tasks()
        return render_template("Home.html",tasks=tasks)
    else:
        tasks = get_all_tasks()
        return render_template("Home.html",tasks=tasks)

@app.route("/update/<int:id>",methods=["POST","GET"])
def update(id):
    if request.method == "POST":
        task = request.form.get("task")
        update_task(id,task)
        return redirect("/")
    else:
        task = get_task_by_id(id)
        print(task[1])
        return render_template("Update.html",task=task)
    
    
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
