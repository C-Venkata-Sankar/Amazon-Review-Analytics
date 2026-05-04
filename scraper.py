import re
import time
from playwright.sync_api import sync_playwright

SESSION_FILE = "amazon_session.json"


def extract_asin(url):
    match = re.search(r"/dp/([A-Z0-9]{10})", url)
    return match.group(1) if match else None


def scrape_reviews(url):
    with sync_playwright() as p:
        print("[LOG] Launching browser with session...")

        browser = p.chromium.launch(headless=False)

        context = browser.new_context(
            storage_state=SESSION_FILE
        )

        page = context.new_page()

        asin = extract_asin(url)
        product_url = f"https://www.amazon.in/dp/{asin}"

        print(f"[LOG] Opening product page: {product_url}")
        page.goto(product_url, timeout=60000)

        time.sleep(3)

        print("\n[LOG] Starting controlled scroll...\n")

        reviews_found = False

        for i in range(20):
            print(f"[SCROLL] Step {i+1}")

            page.mouse.wheel(0, 1200)
            time.sleep(1)

            scroll_y = page.evaluate("window.scrollY")
            print(f"[DEBUG] Scroll Y position: {scroll_y}")

            # ✅ FIXED SELECTOR (li instead of div)
            review_count = page.locator("li[data-hook='review']").count()
            print(f"[DEBUG] Review elements found so far: {review_count}")

            see_all = page.locator("a[data-hook='see-all-reviews-link-foot']").count()
            print(f"[DEBUG] 'See all reviews' button present: {see_all}")

            if review_count > 0:
                print("\n[LOG] Reviews detected on page ✅")
                reviews_found = True
                break

        if not reviews_found:
            print("\n[ERROR] Reviews NOT found after scrolling ❌")
            print("[DEBUG] Page snippet:\n", page.content()[:1000])
            browser.close()
            return []

        # 🔥 Extract reviews
        review_blocks = page.locator("li[data-hook='review']").all()
        print(f"\n[LOG] Extracting {len(review_blocks)} reviews...\n")

        reviews = []

        for r in review_blocks[:10]:
            try:
                # ✅ FIXED TEXT PATH
                text = r.locator("span[data-hook='review-body'] span").first.inner_text().strip()

                # ✅ FIXED RATING PATH
                rating = r.locator("i[data-hook='review-star-rating'] span").first.inner_text()

                reviews.append({
                    "text": text,
                    "rating": rating
                })
            except:
                continue

        browser.close()
        return reviews


if __name__ == "__main__":
    url = input("Enter Amazon product URL: ").strip()

    reviews = scrape_reviews(url)

    print("\n✅ FINAL OUTPUT:\n")

    for r in reviews:
        print(r)
        print("-" * 50)

    print(f"\nTotal reviews extracted: {len(reviews)}")