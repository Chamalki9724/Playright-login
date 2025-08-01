# app.py
import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session

# Initialize Flask app
app = Flask(__name__)
# Set a secret key for session management and flash messages
# In a real application, use a strong, randomly generated key
app.secret_key = os.urandom(24)

# --- In-memory User Store (for demonstration) ---
# In a real application, use a database and hash passwords.
# This dictionary will store username: password pairs.
users = {
    "user123": "password123",  # A default user to start with
    "admin": "adminpass"       # An admin user for demonstration purposes
}

# In a real application, you would manage user sessions properly,
# but for this API demo, we'll use a simple "logged_in_user" in session
# to simulate authentication for API calls that require it.

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
            # In a real app, you'd set up a proper user session here (e.g., store user_id)
            session['logged_in_user'] = username # Simulate login for API
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
    # In a real app, you'd check session['logged_in_user'] here
    return f"<h1>Welcome to the Dashboard!</h1><p>You have successfully logged in as {session.get('logged_in_user', 'Guest')}.</p><p><a href='/'>Logout</a></p>"

# --- NEW API ENDPOINTS START HERE ---

@app.route('/api/users', methods=['GET'])
def api_get_users():
    """
    API Endpoint 1: Get a list of all registered usernames.
    (Simulated admin access for 'admin' user or if any user is logged in)
    In a real app, this would require proper admin authentication.
    """
    if 'logged_in_user' not in session:
        return jsonify({"message": "Unauthorized. Please log in."}), 401
    
    # In a real application, you might filter sensitive data or restrict to admin roles.
    # For this demo, if 'admin' is logged in, show all users. Otherwise, show only own user.
    if session['logged_in_user'] == 'admin':
        return jsonify({"users": list(users.keys())}), 200
    else:
        return jsonify({"users": [session['logged_in_user']]}), 200

@app.route('/api/user/<username>', methods=['GET'])
def api_get_user_details(username):
    """
    API Endpoint 2: Get details for a specific user.
    (Limited to own profile or if 'admin' is logged in)
    """
    if 'logged_in_user' not in session:
        return jsonify({"message": "Unauthorized. Please log in."}), 401

    if username not in users:
        return jsonify({"message": "User not found."}), 404
    
    # Only allow access to own profile, or if logged in as 'admin'
    if session['logged_in_user'] == username or session['logged_in_user'] == 'admin':
        # In a real application, you wouldn't expose password or other sensitive info.
        return jsonify({"username": username, "status": "active"}), 200
    else:
        return jsonify({"message": "Forbidden. You can only view your own profile."}), 403

@app.route('/api/user/change_password', methods=['POST'])
def api_change_password():
    """
    API Endpoint 3: Allow a logged-in user to change their password.
    Requires JSON payload: {"username": "current_user", "old_password": "...", "new_password": "..."}
    """
    if 'logged_in_user' not in session:
        return jsonify({"message": "Unauthorized. Please log in."}), 401

    data = request.get_json()
    if not data or 'username' not in data or 'old_password' not in data or 'new_password' not in data:
        return jsonify({"message": "Missing data. Requires username, old_password, and new_password."}), 400

    username = data['username'].strip()
    old_password = data['old_password'].strip()
    new_password = data['new_password'].strip()

    # Ensure the user changing password is the logged-in user
    if session['logged_in_user'] != username:
        return jsonify({"message": "Forbidden. You can only change your own password."}), 403

    if username not in users or users[username] != old_password:
        return jsonify({"message": "Invalid username or old password."}), 401
    
    if not new_password:
        return jsonify({"message": "New password cannot be empty."}), 400

    users[username] = new_password
    print(f"Password for {username} changed. Current users: {users}")
    return jsonify({"message": "Password changed successfully."}), 200

@app.route('/api/user/delete', methods=['POST'])
def api_delete_account():
    """
    API Endpoint 4: Allow a logged-in user to delete their own account.
    Requires JSON payload: {"username": "user_to_delete", "password": "..."}
    """
    if 'logged_in_user' not in session:
        return jsonify({"message": "Unauthorized. Please log in."}), 401

    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"message": "Missing data. Requires username and password."}), 400

    username = data['username'].strip()
    password = data['password'].strip()

    # Ensure the user deleting account is the logged-in user
    if session['logged_in_user'] != username:
        return jsonify({"message": "Forbidden. You can only delete your own account."}), 403

    if username not in users or users[username] != password:
        return jsonify({"message": "Invalid username or password."}), 401

    del users[username]
    # In a real app, you would also clear the session of the deleted user
    if 'logged_in_user' in session and session['logged_in_user'] == username:
        session.pop('logged_in_user', None)
    
    print(f"User {username} deleted. Current users: {users}")
    return jsonify({"message": "Account deleted successfully."}), 200

@app.route('/api/logout', methods=['POST'])
def api_logout():
    """
    API Endpoint 5: Log out the current user.
    Clears the session.
    """
    if 'logged_in_user' in session:
        username = session.pop('logged_in_user', None)
        print(f"User {username} logged out via API.")
        return jsonify({"message": "Logged out successfully."}), 200
    else:
        return jsonify({"message": "No active session to log out."}), 400


if __name__ == '__main__':
    # Make sure a 'templates' folder exists in the same directory as app.py
    # and put login.html inside it.
    app.run(debug=True) # debug=True allows for automatic reloading and debugging