from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/pfe'
app.config['SECRET_KEY'] = '123'

db = SQLAlchemy(app)

class AppUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    department = db.Column(db.String(50), nullable=False)
    position = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='Owner')

@app.route('/')
def index():
    users = AppUser.query.all()
    return render_template('index.html', users=users)

@app.route('/add_user', methods=['POST'])
def add_user():
    try:
        new_user = AppUser(
            username=request.form['username'],
            email=request.form['email'],
            phone=request.form['phone'],
            department=request.form['department'],
            position=request.form['position'],
            role='Owner' if AppUser.query.count() == 0 else 'Regular'
        )
        db.session.add(new_user)
        db.session.commit()
        flash('User added successfully', 'success')
    except IntegrityError:
        db.session.rollback()
        flash('Username or Email already exists', 'error')

    return redirect(url_for('index'))

@app.route('/edit_user/<int:user_id>', methods=['POST'])
def edit_user(user_id):
    edited_user = AppUser.query.get(user_id)
    if edited_user:
        edited_user.username = request.form['username']
        edited_user.email = request.form['email']
        edited_user.phone = request.form['phone']
        edited_user.department = request.form['department']
        edited_user.position = request.form['position']
        db.session.commit()
        flash('User updated successfully', 'success')
    else:
        flash('User not found', 'error')

    return redirect(url_for('index'))

@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user_to_delete = AppUser.query.get(user_id)
    if user_to_delete:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash('User deleted successfully', 'success')
    else:
        flash('User not found', 'error')

    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=9898)
