import pandas as pd
import yfinance as yf
import requests
import os
import re
import base64
import pandas as pd
from bs4 import BeautifulSoup
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


# Define the security permissions needed to read messages
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail_session():
    """Handles the secure OAuth2 user login handshake and caches tokens."""
    creds = None
    # token.json stores your login session configuration parameters locally
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def extract_amount_from_text(text_body: str) -> float:
    """Enhanced regex parser that handles diverse formatting styles."""
    # Clean up massive spaces to make regex matching easier
    cleaned_text = " ".join(text_body.split())
    
    patterns = [
        # Looks for currency symbols directly attached to numbers (e.g., ₹450, Rs. 320.50)
        r'(?:Rs\.|INR|₹)\s*([\d,]+(?:\.\d{2})?)',
        # Looks for words like 'Total Paid' or 'Amount' followed by numbers
        r'(?:Total|Paid|Amount|Settled)\s*(?:Amount|Paid)?\s*(?::|—)?\s*(?:Rs\.|INR|₹)?\s*([\d,]+(?:\.\d{2})?)'
    ]
    
    found_amounts = []
    for pattern in patterns:
        matches = re.findall(pattern, cleaned_text, re.IGNORECASE)
        for m in matches:
            try:
                val = float(m.replace(',', ''))
                if 10 < val < 10000:  # Sensible range for personal food orders
                    found_amounts.append(val)
            except ValueError:
                continue
                
    # If we found amounts, return the highest one (typically the final bill total)
    return max(found_amounts) if found_amounts else 0.0

def fetch_live_email_receipts() -> pd.DataFrame:
    """Connects to Gmail with an expanded consumer network query and deep email scanning."""
    try:
        service = authenticate_gmail_session()
        
        # WIDER NET: Capture standard Indian digital spending confirmation emails
        keywords = ["Swiggy", "Zomato", "Uber", "Ola", "Paytm", "PhonePe", "Amazon", "Netflix", "Spotify"]
        query = " OR ".join(keywords)
        
        # Increase maxResults from 10 to 50 to parse deeper into your recent transaction history
        result = service.users().messages().list(userId='me', q=query, maxResults=50).execute()
        messages = result.get('messages', [])
        
        parsed_records = []
        
        for msg in messages:
            msg_data = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
            payload = msg_data.get('payload', {})
            headers = payload.get('headers', [])
            
            subject_str = next((h['value'] for h in headers if h['name'] == 'Subject'), "No Subject").lower()
            date_str = next((h['value'] for h in headers if h['name'] == 'Date'), "")
            
            # ── DYNAMIC MERCHANT IDENTITY MAP ──
            merchant_name = "Other Utility"
            category = "General Utilities"
            
            if "swiggy" in subject_str:
                merchant_name = "Swiggy"
                category = "Food & Dining"
            elif "zomato" in subject_str:
                merchant_name = "Zomato"
                category = "Food & Dining"
            elif "uber" in subject_str:
                merchant_name = "Uber Cabs"
                category = "Travel & Transit"
            elif "ola" in subject_str:
                merchant_name = "Ola Rides"
                category = "Travel & Transit"
            elif "amazon" in subject_str:
                merchant_name = "Amazon"
                category = "Shopping"
            elif "paytm" in subject_str or "phonepe" in subject_str:
                merchant_name = "UPI Transfer"
                category = "Peer Transfer"
            elif "netflix" in subject_str or "spotify" in subject_str:
                merchant_name = "Entertainment Subscription"
                category = "Subscriptions"
            
            # Decode email body text
            body = ""
            if 'parts' in payload:
                for part in payload['parts']:
                    if part['mimeType'] in ['text/plain', 'text/html']:
                        data = part['body'].get('data', '')
                        body += base64.urlsafe_b64decode(data.encode('UTF-8')).decode('UTF-8')
            else:
                data = payload['body'].get('data', '')
                body = base64.urlsafe_b64decode(data.encode('UTF-8')).decode('UTF-8')
            
            soup = BeautifulSoup(body, "html.parser")
            clean_text = soup.get_text()
            
            final_amount = extract_amount_from_text(clean_text)
            
            if final_amount > 0:
                parsed_records.append({
                    'Date': pd.to_datetime(date_str, errors='coerce'),
                    'Merchant': merchant_name,
                    'Amount (₹)': final_amount,
                    'Category': category
                })
                
        if parsed_records:
            df = pd.DataFrame(parsed_records).sort_values(by='Date', ascending=False)
            # Remove any duplicate rows that might hit the script loop twice
            df = df.drop_duplicates()
            return df
        return pd.DataFrame()
        
    except Exception as e:
        print(f"[GMAIL ERROR LOG]: {e}")
        return pd.DataFrame()

# ── 1. LIVE MARKET DATA ENGINE ──
def get_live_asset_price(ticker: str) -> float:
    """
    Fetches real-time market data from public asset feeds.
    Example tickers: 'RELIANCE.NS' (NSE), 'BTC-USD' (Crypto), 'GC=F' (Gold)
    """
    try:
        asset = yf.Ticker(ticker)
        todays_data = asset.history(period='1d')
        if not todays_data.empty:
            return float(todays_data['Close'].iloc[-1])
        return 0.0
    except Exception:
        return 0.0

# ── 2. FORENSIC CSV INGESTION ENGINE ──
def process_real_client_statement(uploaded_file) -> pd.DataFrame:
    """
    Takes an actual raw CSV statement uploaded by your team,
    normalizes the columns, and preps it for the audit matrix.
    """
    try:
        # Read the real CSV file
        df = pd.read_csv(uploaded_file)
        
        # Clean whitespaces from string column headers
        df.columns = df.columns.str.strip()
        
        # Standardize core column names regardless of bank format
        # Maps common statement variations to unified system keys
        rename_map = {
            'Transaction Date': 'Date', 'Txn Date': 'Date',
            'Description': 'Merchant', 'Narration': 'Merchant',
            'Amount': 'Amount (₹)', 'Transaction Amount': 'Amount (₹)'
        }
        df = df.rename(columns=rename_map)
        
        # Convert date strings to actual datetime objects cleanly
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df['Amount (₹)'] = pd.to_numeric(df['Amount (₹)'].astype(str).str.replace(',', ''), errors='coerce')
        
        # Drop rows that don't contain valid amounts
        df = df.dropna(subset=['Amount (₹)'])
        return df
    except Exception as e:
        return pd.DataFrame() # Return empty layout frame on parse failure