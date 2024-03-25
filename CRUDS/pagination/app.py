from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_

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
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search', '')
    role_filter = request.args.get('role', '')

    users = AppUser.query

    if role_filter:
        users = users.filter_by(role=role_filter)

    if search_query:
        search_filter = or_(
            AppUser.username.ilike(f'%{search_query}%'),
            AppUser.email.ilike(f'%{search_query}%'),
            AppUser.phone.ilike(f'%{search_query}%'),
            AppUser.department.ilike(f'%{search_query}%'),
            AppUser.position.ilike(f'%{search_query}%'),
            AppUser.role.ilike(f'%{search_query}%')
        )
        users = users.filter(search_filter)

    users = users.paginate(page=page, per_page=10)

    return render_template('index.html', users=users, search_query=search_query, role_filter=role_filter)

if __name__ == '__main__':
    app.run(debug=True, port=9898)
