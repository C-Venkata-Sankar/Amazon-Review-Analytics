import streamlit as st
import os
import json
import time
from all_reviews import scrape_reviews, extract_asin
from revenue_engine import scrape_product_details

OUTPUT_DIR = "reviews_data"

# ---------- CONFIG ----------
st.set_page_config(
    page_title="Review Analaytics",
    page_icon="🧠",
    layout="wide"
)

# ---------- SESSION STATE ----------
if "results" not in st.session_state:
    st.session_state.results = []

if "ai_output" not in st.session_state:
    st.session_state.ai_output = None

if "scraping_done" not in st.session_state:
    st.session_state.scraping_done = False


# ---------- STYLE ----------
st.markdown("""
<style>

.title {
    font-size: 42px;
    font-weight: 700;
}

.subtitle {
    color: #555;
}

.section {
    margin-top: 25px;
    font-size: 22px;
    font-weight: 600;
}

.card {
    padding: 18px;
    border-radius: 14px;
    background: linear-gradient(135deg, #e8f5ff, #e0f7fa);
    border: 1px solid #cde7ff;
    margin-bottom: 12px;
}

.log-box {
    background: #f6f8fa;
    padding: 12px;
    border-radius: 10px;
    font-size: 14px;
    height: 200px;
    overflow-y: auto;
}

/* Animated progress */
.progress-bar {
    height: 18px;
    border-radius: 20px;
    background: linear-gradient(270deg, #4facfe, #00f2fe, #4facfe);
    background-size: 400% 400%;
    animation: gradientMove 2s ease infinite;
}

@keyframes gradientMove {
    0% { background-position: 0% }
    50% { background-position: 100% }
    100% { background-position: 0% }
}

</style>
""", unsafe_allow_html=True)


# ---------- HELPERS ----------
def ensure_folder():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)


def save_reviews(asin, reviews, tag):
    file_path = os.path.join(OUTPUT_DIR, f"{tag}_{asin}.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(reviews, f, indent=2, ensure_ascii=False)
    return file_path


# ---------- HEADER ----------
st.markdown('<div class="title">🧠 Review Analaytics</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Scrape → Analyze → Compare → Win</div>', unsafe_allow_html=True)

ensure_folder()


# ---------- SIDEBAR ----------
st.sidebar.header("📥 Input Products")

your_url = st.sidebar.text_input("Your Product")

competitor_urls = []
for i in range(10):
    url = st.sidebar.text_input(f"Competitor {i+1}", key=f"comp_{i}")
    if url:
        competitor_urls.append(url)

start = st.sidebar.button("🚀 Start Analysis")


# ---------- SCRAPING ----------
if start:

    st.session_state.results = []
    st.session_state.ai_output = None
    st.session_state.scraping_done = False

    urls = []

    if your_url.strip():
        urls.append(("your", your_url.strip(), "Your Product"))

    for idx, u in enumerate(competitor_urls):
        urls.append(("competitor", u.strip(), f"Competitor {idx+1}"))

    total = len(urls)

    progress = st.progress(0)
    status = st.empty()
    log_box = st.empty()

    logs = []

    def log(msg):
        logs.append(msg)
        log_box.markdown(
            '<div class="log-box">' + "<br>".join(logs[-12:]) + "</div>",
            unsafe_allow_html=True
        )

    st.markdown("## ⚙️ Scraping in progress...")

    for i, (tag, url, label) in enumerate(urls):

        percent = int((i / total) * 100)
        progress.progress(percent)

        status.markdown(f"### 🔄 Processing {label}")

        log("🔗 Connecting to Amazon...")
        time.sleep(0.2)

        asin = extract_asin(url)

        if not asin:
            log("❌ Invalid URL")
            continue

        log("📦 Fetching reviews...")

        try:
            reviews = scrape_reviews(url)

            log(f"🧠 Extracted {len(reviews)} reviews")

            # 🔥 NEW: fetch product revenue data
            log("💰 Fetching product metrics...")
            product_info = scrape_product_details(url)

            file_path = save_reviews(asin, reviews, tag)

            st.session_state.results.append({
                "title": product_info.get("title") or label,
                "tag": tag,
                "count": len(reviews),
                "file": file_path,

                # 🔥 NEW FIELDS
                "price": product_info.get("price"),
                "bsr": product_info.get("bsr"),
                "sales": product_info.get("estimated_sales"),
                "revenue": product_info.get("estimated_revenue")
            })
            log(f"✅ Done: {label}")

        except Exception as e:
            log(f"❌ Error: {str(e)}")

        progress.progress(int(((i + 1) / total) * 100))

    st.session_state.scraping_done = True
    status.success("✅ Scraping Completed!")


# ---------- SHOW RESULTS ----------
if st.session_state.results:

    st.markdown("---")
    st.subheader("📊 Overview")

    col1, col2, col3 = st.columns(3)

    total_products = len(st.session_state.results)
    total_reviews = sum(r["count"] for r in st.session_state.results)
    your_reviews = sum(r["count"] for r in st.session_state.results if r["tag"] == "your")

    col1.metric("Products", total_products)
    col2.metric("Total Reviews", total_reviews)
    col3.metric("Your Reviews", your_reviews)

    st.markdown("---")

    st.subheader("📦 Products")

    for r in st.session_state.results:
        st.markdown(f"""
        <div class="card">
            <b>{r['title']}</b><br>

            📝 Reviews: {r['count']}
            💰 Price: ₹{r.get('price', 'N/A')}
            📦 Sales (est): {r.get('sales', 'N/A')}
            📈 Revenue: ₹{r.get('revenue', 'N/A')}
        </div>
        """, unsafe_allow_html=True)


# ---------- AI ----------
if st.session_state.scraping_done:

    st.markdown("---")
    st.subheader("🧠 AI Insights")

    if st.button("⚡ Generate AI Insights"):

        from ai_engine import run_ai_pipeline

        progress = st.progress(0)
        status = st.empty()
        log_box = st.empty()

        ai_logs = []

        # 🔥 Better log styling
        def log_ai(msg):
            ai_logs.append(f"⚡ {msg}")
            log_box.markdown(
                '<div class="log-box">' + "<br>".join(ai_logs[-12:]) + "</div>",
                unsafe_allow_html=True
            )

        # 🔹 Prepare inputs
        file_inputs = [
            {
                "path": r["file"],
                "tag": r["tag"],
                "name": r["title"]
            }
            for r in st.session_state.results
        ]

        # 🔥 Dynamic status
        status.markdown("🤖 Warming up AI engine...")

        # 🔥 RUN AI (REAL PROGRESS + REAL LOGS)
        ai_output = run_ai_pipeline(
            file_inputs,
            progress_callback=lambda x: progress.progress(x),
            log_callback=log_ai
        )

        # 🔥 Final UI
        progress.progress(100)
        status.success("✅ AI Analysis Complete!")

        st.session_state.ai_output = ai_output


# ---------- DISPLAY AI ----------
if st.session_state.ai_output:

    st.markdown("## 📊 AI Results")

    for item in st.session_state.ai_output["individual_analysis"]:
        st.markdown(f"### 🔍 {item['name']}")
        st.write(item["analysis"])

    st.markdown("---")
    st.markdown("## ⚔️ Competitor Insights")
    st.write(st.session_state.ai_output["comparison"])