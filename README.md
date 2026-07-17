# Amazon Review Analytics

> AI-powered review intelligence platform that transforms Amazon product reviews into actionable business insights using Large Language Models, browser automation, and analytics.

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Playwright](https://img.shields.io/badge/Playwright-Automation-2EAD33?style=for-the-badge&logo=playwright&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini-AI-4285F4?style=for-the-badge&logo=google&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-success?style=for-the-badge)

---

# Overview

Amazon Review Analytics is an AI-powered data pipeline that automatically collects Amazon product reviews, performs Large Language Model (LLM)-based sentiment analysis, and generates business-oriented insights including customer satisfaction, purchasing behavior, revenue impact, and product improvement recommendations.

Instead of manually reading thousands of reviews, this system converts unstructured customer feedback into structured intelligence that can support product managers, marketing teams, founders, and business analysts.

The project combines modern browser automation, AI reasoning, and data analytics into a modular architecture designed for scalability and future expansion.

---

# Architecture

```
                    Amazon Product

                           │
                           ▼

                Playwright Web Scraper
                (Authenticated Session)

                           │

                           ▼

                 Review Extraction Engine

                           │

                           ▼

                Data Cleaning & Processing

                           │

                           ▼

                AI Sentiment Engine
          (Google Gemini / OpenAI Compatible)

                           │

             ┌─────────────┴──────────────┐

             ▼                            ▼

      Customer Insights           Revenue Analytics

             ▼                            ▼

          JSON Reports        Business Recommendations

                     ▼

            Final Structured Output
```

---

# Key Features

## Intelligent Review Scraping

- Automated review extraction using Playwright
- Handles dynamic page loading
- Supports authenticated sessions
- Persistent browser login
- CAPTCHA-safe login workflow
- Structured review collection

---

## AI-Powered Sentiment Analysis

Uses Large Language Models to classify reviews into:

- Positive
- Neutral
- Negative

Along with:

- Confidence Score
- Customer Intent
- Product Strengths
- Product Weaknesses
- Pain Points
- Suggested Improvements

The AI layer is provider-agnostic and can easily be configured for:

- Google Gemini
- OpenAI GPT
- Azure OpenAI
- Claude
- Local LLMs

---

## Business Intelligence

Beyond sentiment analysis, the system extracts:

- Customer purchasing patterns
- Most common complaints
- Frequently appreciated features
- Product quality trends
- Customer satisfaction metrics
- Review distribution
- Revenue impact estimation

This enables businesses to make data-driven product decisions instead of relying on manual review analysis.

---

## Modular Architecture

The project follows a separation-of-concerns design.

Each component is responsible for a single task:

- Authentication
- Scraping
- AI Processing
- Revenue Analysis
- Report Generation

This makes the codebase maintainable, scalable, and easy to extend.

---

# Project Structure

```
Amazon-Review-Analytics/

│
├── app.py                     # Application entry point
├── main.py                    # Pipeline orchestrator
├── scraper.py                 # Amazon scraping engine
├── ai_engine.py               # LLM sentiment analysis
├── revenue_engine.py          # Revenue analytics
├── all_reviews.py             # Review aggregation
├── step5_login_session.py     # Login session creation
│
├── reviews_data/              # Raw scraped reviews
├── reviews.json               # Processed AI output
├── amazon_session.json        # Browser session
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Technology Stack

| Category | Technologies |
|----------|--------------|
| Language | Python 3.11+ |
| Browser Automation | Playwright |
| AI | Google Gemini |
| Data Processing | JSON |
| Authentication | Persistent Browser Sessions |
| Environment | Virtual Environment |
| Package Management | pip |

---

# Installation

## Clone Repository

```bash
git clone https://github.com/C-Venkata-Sankar/Amazon-Review-Analytics.git

cd Amazon-Review-Analytics
```

---

## Create Virtual Environment

Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Install Playwright

```bash
playwright install
```

---

# Configuration

## Step 1 — Create Amazon Session

Run

```bash
python step5_login_session.py
```

A Chromium browser will open.

Login manually.

After successful authentication, the application stores:

```
amazon_session.json
```

This session is reused for future scraping without requiring repeated logins.

---

## Step 2 — Configure AI

Create a `.env`

```
GEMINI_API_KEY=YOUR_API_KEY
```

Never commit:

```
.env

amazon_session.json
```

to version control.

---

# Running the Project

Execute

```bash
python main.py
```

Pipeline execution

```
Authenticate

↓

Scrape Reviews

↓

Clean Data

↓

AI Analysis

↓

Revenue Analytics

↓

Generate JSON Output
```

---

# Sample Output

```
reviews.json
```

Example

```json
{
  "rating": 5,
  "sentiment": "Positive",
  "confidence": 98,
  "strengths": [
      "Excellent battery",
      "Premium build quality"
  ],
  "weaknesses": [],
  "summary": "Customers consistently praise battery life and durability."
}
```

---

# Design Principles

This project follows modern software engineering practices.

- Modular Architecture
- Separation of Concerns
- Single Responsibility Principle
- AI Provider Abstraction
- Reusable Components
- Extensible Pipeline
- Clean Code Practices

---

# Future Roadmap

Planned improvements include:

- REST API using FastAPI
- React Dashboard
- PostgreSQL Integration
- Historical Trend Analysis
- Product Comparison Engine
- Batch Processing
- Multi-product Analytics
- Report Export (PDF / Excel)
- Vector Database Support
- RAG-powered Customer Insights
- Interactive Business Dashboard
- Docker Support
- CI/CD Pipeline
- Cloud Deployment
- Multi-threaded Review Processing

---

# Performance Considerations

The project is designed with scalability in mind.

Future optimizations include:

- Parallel scraping
- Async AI requests
- Distributed workers
- Caching
- Incremental scraping
- Streaming analytics
- Queue-based processing

---

# Security

Sensitive files are intentionally excluded.

```
.env

amazon_session.json

__pycache__/

*.pyc
```

API credentials should always be stored using environment variables.

---

# Contributing

Contributions are welcome.

If you have ideas for improving the analytics engine, AI pipeline, or scraping performance, feel free to fork the repository and submit a pull request.

---

# License

This project is released under the MIT License.

---

# Author

## C. Venkata Sankar

**Software Engineer**

Specializing in:

- AI Systems
- Full-Stack Development
- FastAPI
- React
- Node.js
- PostgreSQL
- LLM Applications
- AI Agents
- Analytics Platforms
- Scalable Backend Systems

---

# Support

If you found this project useful,

⭐ Consider giving it a star.

It helps others discover the project and motivates future development.
