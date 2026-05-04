import os
import json
from all_reviews import scrape_reviews, extract_asin

OUTPUT_DIR = "reviews_data"


def ensure_folder():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)


def save_reviews(asin, reviews, tag):
    file_path = os.path.join(OUTPUT_DIR, f"{tag}_{asin}.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(reviews, f, indent=2, ensure_ascii=False)

    print(f"[FILE] Saved: {file_path}")


def process_product(url, tag):
    asin = extract_asin(url)

    if not asin:
        print("❌ Invalid or empty URL. Skipping...")
        return None

    print(f"[INFO] {tag.upper()} PRODUCT ASIN: {asin}")

    try:
        reviews = scrape_reviews(url)

        if not reviews:
            print("⚠️ No reviews found")
            return None

        save_reviews(asin, reviews, tag)

        return {
            "asin": asin,
            "tag": tag,
            "reviews_count": len(reviews)
        }

    except Exception as e:
        print(f"❌ Error scraping {asin}: {e}")
        return None


if __name__ == "__main__":
    ensure_folder()

    print("========================================")
    print(" Amazon Review Analytics Scraper")
    print("========================================\n")

    # 🔹 YOUR PRODUCT
    print("👉 Enter YOUR product URL (or press ENTER to skip):")
    your_url = input().strip()

    your_product = None
    if your_url:
        your_product = process_product(your_url, "your")
    else:
        print("⚠️ Skipped YOUR product\n")

    # 🔹 COMPETITORS
    print("\n👉 Enter up to 9 COMPETITOR URLs")
    print("👉 Press ENTER anytime to stop input\n")

    competitor_data = []

    for i in range(1, 10):
        url = input(f"Competitor {i}: ").strip()

        if not url:
            print("⏹️ Stopping competitor input\n")
            break

        data = process_product(url, "competitor")

        if data:
            competitor_data.append(data)

    # 🔹 FINAL SUMMARY
    print("\n========================================")
    print("✅ SCRAPING COMPLETE")
    print("========================================\n")

    if your_product:
        print(f"Your Product: {your_product['asin']} ({your_product['reviews_count']} reviews)")
    else:
        print("Your Product: Not provided")

    print(f"Competitors scraped: {len(competitor_data)}")

    if competitor_data:
        for c in competitor_data:
            print(f" - {c['asin']} ({c['reviews_count']} reviews)")

    print("\n📁 All files saved inside 'reviews_data/' folder")