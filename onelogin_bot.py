#!/usr/bin/env python3

import os
import sys
from dotenv import load_dotenv
from playwright.sync_api import Playwright, sync_playwright, expect

load_dotenv()

one_login_site = os.getenv("ONELOGIN_SITE")
one_login_pass = os.getenv("ONELOGIN_PASS")
user_is_active = False

def run(playwright: Playwright, one_login_account):
   
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()

    # Open new page
    page = context.new_page()

    # Go to prescribed OneLogin site
    page.goto(one_login_site)

    # Click [data-testid="username"]
    page.locator("[data-testid=\"username\"]").click()

    # Fill [data-testid="username"]
    page.locator("[data-testid=\"username\"]").fill(one_login_account)

    # Click button:has-text("Continue")
    page.locator("button:has-text(\"Continue\")").click()

    # Click input[name="password"]
    page.locator("input[name=\"password\"]").click()

    # Fill input[name="password"]
    page.locator("input[name=\"password\"]").fill(one_login_pass)

    # Click button:has-text("Continue")
    page.locator("button:has-text(\"Continue\")").click()

    # Check if the page now says that the user needs to two factor authenticate.
    try:
        page.locator("text=2-factor authentication is required to secure your account.")
        user_is_active = True
        return f"{one_login_account} is an active account. Closing"
    except:
        return f"The user is not active, or the website did not load correctly"

    # ---------------------
    context.close()
    browser.close()

def run_playwright():
    with sync_playwright() as playwright:
        run(playwright)