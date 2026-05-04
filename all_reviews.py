import re
import time
import json
from playwright.sync_api import sync_playwright

SESSION_FILE = "amazon_session.json"
OUTPUT_FILE = "reviews.json"


def extract_asin(url):
    match = re.search(r"/dp/([A-Z0-9]{10})", url)
    return match.group(1) if match else None


def scrape_reviews(url):
    with sync_playwright() as p:
        print("[LOG] Launching browser with session...")

        browser = p.chromium.launch(headless=True)  # 🔥 important
        context = browser.new_context(storage_state=SESSION_FILE)
        page = context.new_page()

        asin = extract_asin(url)

        review_url = f"https://www.amazon.in/product-reviews/{asin}"
        print(f"[LOG] Opening review page: {review_url}")

        page.goto(review_url, timeout=60000)
        page.wait_for_selector("li[data-hook='review']")
        time.sleep(2)

        all_reviews = []
        seen_ids = set()

        # CLEAR FILE
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)

        page_count = 1

        while True:
            print(f"\n[PAGE] Extracting page {page_count}")

            review_blocks = page.locator("li[data-hook='review']").all()
            print(f"[DEBUG] Reviews visible: {len(review_blocks)}")

            page_reviews = []

            for r in review_blocks:
                try:
                    review_id = r.get_attribute("id")

                    if review_id in seen_ids:
                        continue

                    seen_ids.add(review_id)

                    text = r.locator("span[data-hook='review-body'] span").first.inner_text().strip()
                    rating = r.locator("i[data-hook='review-star-rating'] span").first.inner_text()

                    review_data = {
                        "id": review_id,
                        "text": text,
                        "rating": rating,
                        "page": page_count
                    }

                    all_reviews.append(review_data)
                    page_reviews.append(review_data)

                except:
                    continue

            # SAVE AFTER EACH PAGE
            with open(OUTPUT_FILE, "r+", encoding="utf-8") as f:
                existing = json.load(f)
                existing.extend(page_reviews)
                f.seek(0)
                json.dump(existing, f, indent=2, ensure_ascii=False)

            print(f"[LOG] Saved {len(page_reviews)} new reviews")

            # 🔥 CLICK "SHOW MORE REVIEWS"
            show_more = page.locator("a[data-hook='show-more-button']")

            if show_more.count() == 0:
                print("[LOG] No more pages left ❌")
                break

            try:
                print("[ACTION] Clicking 'Show more reviews'...")
                show_more.first.click()

                # WAIT FOR NEW CONTENT (IMPORTANT)
                time.sleep(3)

                page_count += 1

            except Exception as e:
                print("[ERROR] Failed to click show more:", e)
                break

        browser.close()
        return all_reviews


if __name__ == "__main__":
    url = input("Enter Amazon product URL: ").strip()

    reviews = scrape_reviews(url)

    print("\n✅ FINAL OUTPUT:\n")

    for r in reviews[:10]:
        print(r)
        print("-" * 50)

    print(f"\nTotal UNIQUE reviews extracted: {len(reviews)}")
    print(f"[FILE] Saved to {OUTPUT_FILE}")