from playwright.sync_api import sync_playwright
import subprocess
import time
import os

def verify():
    # Start server
    server = subprocess.Popen(["python3", "-m", "http.server", "8080"], cwd="app")
    time.sleep(2)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            page.goto("http://localhost:8080")

            # Wait for content
            page.wait_for_selector(".nav-item")

            # 1. Mark page 1 as finished
            page.click("#mark-complete")
            time.sleep(0.5)

            # 2. Search for "Noun"
            page.fill("#search", "Noun")
            page.wait_for_selector("#search-results:not(.hidden)")

            # Take screenshot
            os.makedirs("/home/jules/verification", exist_ok=True)
            page.screenshot(path="/home/jules/verification/final_app.png")
            print("Final verification screenshot taken")

        finally:
            browser.close()
            server.terminate()

if __name__ == "__main__":
    verify()
