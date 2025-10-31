from flask import Flask, render_template, request, redirect, url_for
import csv
import os

app = Flask(__name__)

# The name of the file where tasks are stored
CSV_FILE = "tasks.csv"

class Task:
    """Represents a single to-do task."""
    def __init__(self, title, description, category, completed=False):
        self.title = title
        self.description = description
        self.category = category
        # Ensure 'completed' is a boolean
        self.completed = completed if isinstance(completed, bool) else completed == 'True'

    def to_csv_row(self):
        """Converts the task object to a list for CSV writing."""
        return [self.title, self.description, self.category, self.completed]

def load_tasks():
    """Loads tasks from the tasks.csv file."""
    if not os.path.exists(CSV_FILE):
        return []
    
    tasks = []
    with open(CSV_FILE, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row:
                tasks.append(Task(title=row[0], description=row[1], category=row[2], completed=row[3]))
    return tasks

def save_tasks(tasks):
    """Saves a list of tasks to the tasks.csv file."""
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for task in tasks:
            writer.writerow(task.to_csv_row())

# Main route to display tasks
@app.route('/')
def index():
    tasks = load_tasks()
    return render_template('index.html', tasks=tasks)

# Route to add a new task
@app.route('/add', methods=['POST'])
def add_task():
    tasks = load_tasks()
    title = request.form.get('title')
    description = request.form.get('description')
    category = request.form.get('category')
    if title:
        tasks.append(Task(title, description, category))
        save_tasks(tasks)
    return redirect(url_for('index'))

# Route to mark a task as completed
@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        tasks[task_id].completed = True
        save_tasks(tasks)
    return redirect(url_for('index'))

# Route to delete a task
@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
        save_tasks(tasks)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
