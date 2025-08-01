import pytest
import re
from playwright.sync_api import Page, expect
import os

@pytest.fixture(scope="session")
def browser_type_launch_args():
    return {"headless": False}

if not os.path.exists("screenshots"):
    os.makedirs("screenshots")

def test_login_success(page: Page):
    page.goto("http://127.0.0.1:5000/")
    page.fill("input[name='username']", "user123")
    page.fill("input[name='password']", "password123")
    page.click("button[type='submit']")
    expect(page).to_have_url("http://127.0.0.1:5000/dashboard", timeout=2000)
    expect(page.locator("h1")).to_have_text("Welcome to the Dashboard!", timeout=2000)
    # Only take a screenshot at the end
    page.screenshot(path="screenshots/dashboard_success.png")

def test_login_failure(page: Page):
    page.goto("http://127.0.0.1:5000/")
    page.fill("input[name='username']", "invaliduser")
    page.fill("input[name='password']", "wrongpass")
    page.click("button[type='submit']")
    expect(page).to_have_url("http://127.0.0.1:5000/", timeout=2000)
    expect(page.locator("li.bg-red-100.text-red-700")).to_have_text(
        "Invalid Username or Password. Please try again.", timeout=2000
    )
    page.screenshot(path="screenshots/login_failure_message.png")

def test_login_empty_fields(page: Page):
    page.goto("http://127.0.0.1:5000/")
    page.click("button[type='submit']")
    expect(page).to_have_url("http://127.0.0.1:5000/", timeout=2000)
    page.screenshot(path="screenshots/login_empty_submit_attempt.png")