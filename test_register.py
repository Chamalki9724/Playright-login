import re
import time # Import time for unique username generation
from playwright.sync_api import Page, expect
import os # Import os to create directory

# Create a directory for screenshots if it doesn't exist
if not os.path.exists("screenshots"):
    os.makedirs("screenshots")

def test_registration_success(page: Page):
    """
    Tests successful user registration and takes screenshots.
    """
    page.goto("http://127.0.0.1:5000/register")
    page.screenshot(path="screenshots/register_page.png")

    # Generate a unique username for each test run to avoid conflicts
    new_username = f"newuser_{int(time.time())}"
    new_password = "newpassword123"

    # Fill in the registration form
    page.fill("input[name='username']", new_username)
    page.fill("input[name='password']", new_password)
    page.screenshot(path="screenshots/register_filled.png")

    # Click the register button
    page.click("button[type='submit']")

    # Assert successful registration - check for redirect to login page and success flash message
    expect(page).to_have_url("http://127.0.0.1:5000/")
    expect(page.locator("li.bg-green-100.text-green-700")).to_have_text("Registration successful! You can now log in.")
    page.screenshot(path="screenshots/registration_success_login_page.png")

def test_registration_existing_username(page: Page):
    """
    Tests registration attempt with an already existing username and takes screenshots.
    """
    page.goto("http://127.0.0.1:5000/register")
    page.screenshot(path="screenshots/register_page_existing_user.png")

    # Use an existing username from the app.py (e.g., "user123")
    page.fill("input[name='username']", "user123")
    page.fill("input[name='password']", "anypassword")
    page.screenshot(path="screenshots/register_filled_existing_user.png")

    # Click the register button
    page.click("button[type='submit']")

    # Assert that registration fails and an error message is displayed
    expect(page).to_have_url("http://127.0.0.1:5000/register") # Should remain on the registration page
    expect(page.locator("li.bg-red-100.text-red-700")).to_have_text("Username already exists. Please choose a different one.")
    page.screenshot(path="screenshots/registration_existing_user_error.png")

def test_registration_empty_fields(page: Page):
    """
    Tests registration attempt with empty fields and takes screenshots.
    """
    page.goto("http://127.0.0.1:5000/register")
    page.screenshot(path="screenshots/register_empty_initial.png")

    # Attempt to register with empty username and password
    page.click("button[type='submit']")

    # Assert that registration fails and an error message is displayed
    expect(page).to_have_url("http://127.0.0.1:5000/register") # Should remain on the registration page
    expect(page.locator("li.bg-red-100.text-red-700")).to_have_text("Please fill out all fields to register.")
    page.screenshot(path="screenshots/registration_empty_fields_error.png")

def test_password_visibility_toggle(page: Page):
    """
    Tests the password visibility toggle functionality on the registration page and takes screenshots.
    """
    page.goto("http://127.0.0.1:5000/register")
    page.screenshot(path="screenshots/password_toggle_initial.png")

    password_input = page.locator("input[name='password']")
    eye_icon = page.locator("#eye-icon")
    eye_slash_icon = page.locator("#eye-slash-icon")

    # Initially, the password input should be type 'password' and eye icon visible
    expect(password_input).to_have_attribute("type", "password")
    expect(eye_icon).to_be_visible()
    expect(eye_slash_icon).to_be_hidden()

    # Click the eye icon to show password
    eye_icon.click()
    page.screenshot(path="screenshots/password_toggle_visible.png")
    expect(password_input).to_have_attribute("type", "text")
    expect(eye_icon).to_be_hidden()
    expect(eye_slash_icon).to_be_visible()

    # Click the eye-slash icon to hide password
    eye_slash_icon.click()
    page.screenshot(path="screenshots/password_toggle_hidden.png")
    expect(password_input).to_have_attribute("type", "password")
    expect(eye_icon).to_be_visible()
    expect(eye_slash_icon).to_be_hidden()