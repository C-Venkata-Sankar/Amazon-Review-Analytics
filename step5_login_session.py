from playwright.sync_api import sync_playwright

SESSION_FILE = "amazon_session.json"


def save_login_session():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        )

        page = context.new_page()

        print("👉 Opening Amazon homepage...")
        page.goto("https://www.amazon.in", timeout=60000)

        page.wait_for_timeout(3000)

        # 🔹 Click Sign In (more reliable than direct URL)
        try:
            print("👉 Clicking Sign In...")
            page.locator("#nav-link-accountList").click()
        except:
            print("⚠️ Could not find Sign In button. Try manually navigating.")
        
        print("\n⚠️ LOGIN MANUALLY in the browser")
        print("After login completes (you see your name on top), press ENTER...\n")

        input()

        # 🔹 Save session
        context.storage_state(path=SESSION_FILE)

        print(f"✅ Session saved to {SESSION_FILE}")

        browser.close()


if __name__ == "__main__":
    save_login_session()