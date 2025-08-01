# app.py
import os
from flask import Flask, render_template, request, redirect, url_for, flash

# Initialize Flask app
app = Flask(__name__)
# Set a secret key for session management and flash messages
# In a real application, use a strong, randomly generated key
app.secret_key = os.urandom(24)

# --- In-memory User Store (for demonstration) ---
# In a real application, use a database and hash passwords.
users = {
    "user123": "password123"  # A default user to start with
}

@app.route('/', methods=['GET', 'POST'])
def login():
    """
    Handles the login page.
    GET request: Displays the login form.
    POST request: Processes the login attempt.
    """
    if request.method == 'POST':
        # Strip whitespace from input to prevent login errors
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        # --- Debugging: Print received credentials to the terminal ---
        print(f"Login attempt with: Username='{username}', Password='{password}'")

        # --- Check credentials against the in-memory user store ---
        if username in users and users[username] == password:
            flash('Login Successful! Welcome!', 'success')
            # In a real app, you'd set up a user session here
            return redirect(url_for('dashboard')) # Redirect to a dashboard page
        else:
            flash('Invalid Username or Password. Please try again.', 'error')
            return render_template('login.html') # Re-render the login page with error

    # For GET requests, just render the login form
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handles the registration page.
    GET request: Displays the registration form.
    POST request: Processes the registration attempt (demo).
    """
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        if not username or not password:
            flash('Please fill out all fields to register.', 'error')
            return render_template('register.html')
            
        # --- Check if username already exists ---
        if username in users:
            flash('Username already exists. Please choose a different one.', 'error')
            return render_template('register.html')

        # --- Add new user to the in-memory store ---
        users[username] = password
        print(f"New user registered: {username}. Current users: {users}") # Debug print
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))
    
    # For GET requests, just render the registration form
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    """
    A simple dashboard page accessible after successful login.
    """
    return "<h1>Welcome to the Dashboard!</h1><p>You have successfully logged in.</p><p><a href='/'>Logout</a></p>"

if __name__ == '__main__':
    # Make sure a 'templates' folder exists in the same directory as app.py
    # and put login.html inside it.
    app.run(debug=True) # debug=True allows for automatic reloading and debugging


 