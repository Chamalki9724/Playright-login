import os
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        correct_username = "user123"
        correct_password = "password123"
        if username == correct_username and password == correct_password:
            flash('Login Successful! Welcome!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid Username or Password. Please try again.', 'error')
            return render_template('login.html')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Here you would save the user to a database (this is just a demo)
        if username and password:
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Please fill out all fields.', 'error')
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    return "<h1>Welcome to the Dashboard!</h1><p>You have successfully logged in.</p><p><a href='/'>Logout</a></p>"

if __name__ == '__main__':
    app.run(debug=True)
