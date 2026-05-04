import json
import os
import math
import time
from collections import Counter
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

API_KEY = os.getenv("Your-API-KEY-HERE")
genai.configure(api_key=API_KEY)

MODEL = "gemini-flash-lite-latest"


# ---------- LOAD REVIEWS ----------
def load_reviews(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


# ---------- GENERIC TEXT ANALYSIS ----------
def basic_text_stats(reviews):
    texts = [r["text"] for r in reviews if r.get("text")]

    word_counter = Counter()

    for text in texts:
        words = text.lower().split()
        word_counter.update(words)

    common_words = word_counter.most_common(20)

    avg_length = sum(len(t.split()) for t in texts) / max(len(texts), 1)

    return {
        "total_reviews": len(texts),
        "avg_review_length": round(avg_length, 2),
        "top_words": common_words
    }


# ---------- RATING DISTRIBUTION ----------
def rating_distribution(reviews):
    dist = Counter()

    for r in reviews:
        try:
            rating = r["rating"][0]  # first char: 5 from "5.0..."
            dist[rating] += 1
        except:
            continue

    return dict(dist)


# ---------- CHUNKING ----------
def chunk_reviews(reviews, chunk_size=40):
    for i in range(0, len(reviews), chunk_size):
        yield reviews[i:i + chunk_size]


# ---------- CALL GEMINI ----------
def call_gemini(prompt):
    model = genai.GenerativeModel(MODEL)
    response = model.generate_content(prompt)
    return response.text


# ---------- ANALYZE SINGLE PRODUCT ----------
def analyze_product(file_path, name, log_callback=None):

    reviews = load_reviews(file_path)

    if not reviews:
        return {
            "name": name,
            "analysis": "No reviews found",
            "meta": {}
        }

    stats = basic_text_stats(reviews)
    ratings = rating_distribution(reviews)

    chunks = list(chunk_reviews(reviews))

    partial_outputs = []

    for i, chunk in enumerate(chunks):
        if log_callback:
            log_callback(f"🧩 Processing chunk {i+1}/{len(chunks)} for {name}")

        chunk_text = "\n".join([r["text"] for r in chunk if r.get("text")])

        prompt = f"""
You are a product research expert.

Analyze these customer reviews and extract:

1. What users LOVE
2. What users HATE
3. Common complaints
4. Buying triggers
5. Repeated themes or patterns

REVIEWS:
{chunk_text}
"""

        try:
            output = call_gemini(prompt)
            partial_outputs.append(output)
        except Exception as e:
            partial_outputs.append(f"ERROR: {str(e)}")

    # ---------- FINAL MERGE ----------
    final_prompt = f"""
You are a senior product strategist.

Combine the following chunk-level insights into ONE clean structured report.

Also consider:
- Total reviews: {stats['total_reviews']}
- Average review length: {stats['avg_review_length']}
- Rating distribution: {ratings}

CHUNK INSIGHTS:
{chr(10).join(partial_outputs)}

Give:
- Love summary
- Hate summary
- Key problems (ranked)
- Buying triggers
- Final positioning
"""

    final_output = call_gemini(final_prompt)

    return {
        "name": name,
        "analysis": final_output,
        "meta": {
            "stats": stats,
            "ratings": ratings
        }
    }


# ---------- COMPETITOR COMPARISON ----------
def compare_products(all_outputs, log_callback=None):

    combined_text = "\n\n".join([
        f"{o['name']}:\n{o['analysis']}"
        for o in all_outputs
    ])

    prompt = f"""
You are a market analyst.

Compare these products and give:

1. Who wins overall
2. Strength of each product
3. Weakness of each product
4. Market gaps
5. What "your product" should improve

DATA:
{combined_text}
"""

    return call_gemini(prompt)


# ---------- MAIN PIPELINE ----------
def run_ai_pipeline(file_inputs, progress_callback=None, log_callback=None):

    results = []

    total = len(file_inputs)

    for i, item in enumerate(file_inputs):

        if log_callback:
            log_callback(f"🔍 Analyzing {item['name']}")

        output = analyze_product(
            item["path"],
            item["name"],
            log_callback
        )

        results.append(output)

        if progress_callback:
            progress_callback(int(((i + 1) / total) * 70))

    # ---------- COMPARISON ----------
    if log_callback:
        log_callback("⚔️ Running competitor comparison...")

    comparison = compare_products(results)

    if progress_callback:
        progress_callback(100)

    return {
        "individual_analysis": results,
        "comparison": comparison
    }