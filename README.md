
# Hisaab Kitaab — Personal Finance Terminal

Hisaab Kitaab is a personal finance dashboard and automation application built using Python and Streamlit. The application aggregates personal financial metrics, tracks stock and gold market performance in real time, processes raw bank statements, and automatically syncs digital receipts directly from your email inbox using the Google Gmail API. It also integrates Google's Gemini 3.5 Flash model to provide structured insights on spending behaviors, cash runway, and investment risks.

---

##  Tech Stack & Core Modules

* **User Interface:** Streamlit (Configured with a custom high-density dark navigation panel and clean light-themed metric modules).
* **Data Processing & Engineering:** Pandas and NumPy (For column cleaning, currency text filtering, and aggregate arithmetic arrays).
* **Live Ingestion Channels:** Google Gmail API (OAuth 2.0 authentication) and Python Regular Expressions (`re`).
* **Real-Time Data Feeds:** Yahoo Finance (`yfinance`) API.
* **AI Engine:** Google GenAI SDK (`gemini-3.5-flash`).
* **Data Visualizations:** Plotly Express (High-density bar charts).

---

##  Code Architecture & Component Breakdown

The application is modularized into three core Python files to prevent code dependency errors:

```text
├── app.py              # Main user interface layout, navigation router, and visual canvas
├── data_engine.py      # Live data harvesting, CSV parsing, and Gmail OAuth integration
└── api_connection.py   # AI prompt templates, model configurations, and response parsing

```

### 1. User Interface & Page Flow (`app.py`)

This file drives the layout, styles the visual theme using HTML/CSS overrides, tracks user state changes, and updates dashboard pages.

* **State Persistence:** Initializes `st.session_state` keys (`real_user_data`, `ai_spend_cache`, etc.) at the absolute top of the file. This stops the application from crashing or losing data when a user triggers an update or switches tabs.
* **Page 1: Dashboard:** Aggregates overall net worth metrics, builds asset allocation graphs, and houses the automated "Sync Gmail-ID" engine button.
* **Page 2: Assets:** Displays current portfolio valuations, tracks live gains/losses, and shows asset distribution cards specifically broken down by platform (e.g., Upstox).
* **Page 3: Analytics:** Houses the interactive interface to trigger individual Gemini model calls for cash tracking, risk simulation, and cross-border routing.
* **Page 4: Ledger:** Features a file drop zone that processes physical statement logs and categorizes rows down to explicit clearing states like `RECONCILED`, `LEAKAGE`, or `UNMATCHED` suspense files.

### 2. Ingestion & Extraction Engine (`data_engine.py`)

This file acts as the network and data routing layer of the application. It handles external connections and cleans raw unformatted inputs.

* **Live Market Ticker Hub (`get_live_asset_price`):** Uses `yfinance` to scrape active market closing metrics for equity strings like `RELIANCE.NS` and global commodities like `GC=F` (Gold).
* **Forensic CSV Normalizer (`process_real_client_statement`):** Takes messy user-uploaded bank sheets, strips away accidental whitespaces in column strings, and re-maps alternate naming conventions (like *Txn Date* or *Narration*) to standard unified table keys.
* **Gmail OAuth Authentication (`authenticate_gmail_session`):** Initiates a secure local server authentication handshake using `credentials.json` tokens. Once confirmed, it caches a secure `token.json` credential profile locally to prevent repetitive logins.
* **Automated Inbox Parser (`fetch_live_email_receipts`):** Queries the user's live Gmail account for major consumer spending keywords (*Swiggy, Zomato, Uber, Ola, Amazon, PhonePe, Paytm*). It processes up to 50 recent email rows, decodes base64 HTML payloads, uses BeautifulSoup to pull text strings, and outputs a drop-duplicate Pandas DataFrame.
* **Regular Expression Data Extractor (`extract_amount_from_text`):** Scans raw unformatted text blocks using pre-defined regex layouts:
```python
r'(?:Rs\.|INR|₹)\s*([\d,]+(?:\.\d{2})?)'

```


It captures financial values linked to currency tags, evaluates if the numbers fall in a realistic personal spending threshold, and extracts the final transactional value.

### 3. AI Inference Module (`api_connection.py`)

This module initializes the Google GenAI Client and coordinates text generations with `gemini-3.5-flash`. It maps specific database analytics parameters straight into system prompt templates.

* **Behavioral Spend Analyst (`generate_live_guru_insights`):** Takes total monthly outflow data, highest individual merchant drain, and food platform leaks to generate a concise point-by-point consumption scorecard.
* **Liquidity Risk Calculator (`generate_global_predictive_runway`):** Evaluates daily burn rates against liquid cash pools to mathematically forecast operational runway limits in explicit days.
* **Cross-Border Payout Optimizer (`simulate_smart_payout_routing`):** Evaluates multi-currency remittance parameters and simulates real-time network conditions across banking nodes to select the path with minimal spot FX volatility.
* **Portfolio Stress-Tester (`simulate_institutional_investment_strategy`):** Converts active stock allocations from a JSON format into an institutional analysis brief, testing asset valuations against simulated interest rate spikes and tax liabilities.
* **Formatting Controls:** Every model endpoint contains explicit instructions to output raw text or clean HTML structures (`<strong>`, `<br>`) while strictly banning markdown layouts (``, `#`, `-`) to maintain layout safety inside Streamlit's rendering frame.

---

## Credentials

* **Credential Isolation:** Core private API credentials (`credentials.json`), user session permissions (`token.json`), and system environment configurations (`.env`) are explicitly isolated out of the source control repository using a `.gitignore` profile to prevent public leakage.
* **Environment Configuration:** The AI connection securely loads private system keys at runtime via standard `.env` variables using `load_dotenv()` hooks.

---

##  Local Installation & Run Guide

Follow these steps to run this personal finance terminal locally on your computer:

### 1. Clone the Workspace

```bash
git clone https://github.com/YOUR_USERNAME/Hisaab-Kitaab.git
cd Hisaab-Kitaab

```

### 2. Configure Your Environment Variables

Create a `.env` file in the root project folder and append your Google AI Studio API key:

```text
GEMINI_API_KEY="your_actual_gemini_api_key_here"

```

### 3. Install Required Dependencies

Install the required system packages using your terminal:

```bash
pip install streamlit pandas numpy plotly yfinance beautifulsoup4 google-auth-oauthlib google-api-python-client google-auth-httplib2 python-dotenv google-genai

```

### 4. Setup Google Cloud API Credentials

1. Go to the Google Cloud Console, enable the **Gmail API**, and configure an **OAuth Consent Screen** with your email as a test user.
2. Download your desktop OAuth client credentials, rename the file exactly to `credentials.json`, and place it in the root folder alongside `app.py`.

### 5. Launch the Portal

```bash
streamlit run app.py

```

Why I built this:

As a student, tracking expenses across five different payment apps is a headache.
I wanted to build a "single screen" solution that tells me my current bank balance and warns me if I'm spending too much too fast.
