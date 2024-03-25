from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/pfe'
app.config['SECRET_KEY'] = '123'

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    priority = db.Column(db.String(5), nullable=False)
    assignee = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    tags = db.Column(db.String(100), nullable=False)

@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    try:
        new_task = Task(
            title=request.form['title'],
            priority=request.form['priority'],
            assignee=request.form['assignee'],
            description=request.form['description'],
            start_date=request.form['start_date'],
            due_date=request.form['due_date'],
            tags=request.form['tags']
        )
        db.session.add(new_task)
        db.session.commit()
        flash('Task added successfully', 'success')
    except IntegrityError:
        db.session.rollback()
        flash('An error occurred while adding the task', 'error')

    return redirect(url_for('index'))

@app.route('/edit_task/<int:task_id>', methods=['POST'])
def edit_task(task_id):
    edited_task = Task.query.get(task_id)
    if edited_task:
        edited_task.title = request.form['title']
        edited_task.priority = request.form['priority']
        edited_task.assignee = request.form['assignee']
        edited_task.description = request.form['description']
        edited_task.start_date = request.form['start_date']
        edited_task.due_date = request.form['due_date']
        edited_task.tags = request.form['tags']
        db.session.commit()
        flash('Task updated successfully', 'success')
    else:
        flash('Task not found', 'error')

    return redirect(url_for('index'))

@app.route('/delete_task/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    task_to_delete = Task.query.get(task_id)
    if task_to_delete:
        db.session.delete(task_to_delete)
        db.session.commit()
        flash('Task deleted successfully', 'success')
    else:
        flash('Task not found', 'error')

    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
