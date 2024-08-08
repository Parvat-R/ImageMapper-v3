from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)

    def __init__(self, username, date_of_birth):
        self.username = username
        self.date_of_birth = date_of_birth

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        date_of_birth = request.form['date_of_birth']
        user = User(username, date_of_birth)
        db.session.add(user)
        db.session.commit()
        flash('User created successfully!')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        date_of_birth = request.form['date_of_birth']
        user = User.query.filter_by(username=username, date_of_birth=date_of_birth).first()
        if user:
            flash('Logged in successfully!')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or date of birth')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    flash('Logged out successfully!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)