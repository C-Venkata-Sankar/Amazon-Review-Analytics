import re
from playwright.sync_api import sync_playwright


def extract_price_from_page(page):
    try:
        # Try full price first (BEST)
        price = page.locator("span.a-price span.a-offscreen").first.inner_text()
        return int(re.sub(r"[^\d]", "", price))
    except:
        pass

    try:
        # Fallback
        whole = page.locator("span.a-price-whole").first.inner_text()
        frac = page.locator("span.a-price-fraction").first.inner_text()
        return int((whole + frac).replace(",", ""))
    except:
        return None


def extract_bsr_from_page(page):
    try:
        # Try main bullets section
        text = page.locator("#detailBulletsWrapper_feature_div").inner_text()
    except:
        try:
            text = page.locator("#detailBullets_feature_div").inner_text()
        except:
            try:
                text = page.locator("#productDetails_detailBullets_sections1").inner_text()
            except:
                return None

    try:
        match = re.search(r"#([\d,]+)\s+in", text)
        return int(match.group(1).replace(",", ""))
    except:
        return None


def estimate_sales_from_bsr(bsr):
    if not bsr:
        return 0

    if bsr < 100:
        return 30000
    elif bsr < 500:
        return 15000
    elif bsr < 1000:
        return 8000
    elif bsr < 5000:
        return 3000
    elif bsr < 10000:
        return 1500
    elif bsr < 50000:
        return 500
    else:
        return 100


def scrape_product_details(url, session_file="amazon_session.json"):

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(storage_state=session_file)
        page = context.new_page()

        page.goto(url, timeout=60000)
        page.wait_for_timeout(3000)

        # ---------- TITLE ----------
        try:
            title = page.locator("#productTitle").inner_text().strip()
        except:
            title = "Unknown Product"

        # ---------- PRICE ----------
        price = extract_price_from_page(page)

        # ---------- BSR ----------
        bsr = extract_bsr_from_page(page)

        browser.close()

        # ---------- SALES ----------
        sales = estimate_sales_from_bsr(bsr)

        # ---------- REVENUE ----------
        revenue = price * sales if price and sales else 0

        return {
            "title": title,
            "price": price or 0,
            "bsr": bsr or 0,
            "estimated_sales": sales,
            "estimated_revenue": revenue
        }