import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv


load_dotenv()


API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("ERROR: GEMINI_API_KEY missing from environment configurations!")

print("Success: API connection configurations secured.")


ai_client = genai.Client()




def generate_live_guru_insights(total_spend: float, top_merchant: str, top_merchant_amt: float, food_spend: float) -> str:
    """
    Sends localized dashboard spend parameters to Gemini 3.5 Flash 
    to generate targeted behavioral advice.
    """
    prompt = f"""
    You are 'The Guru', an embedded financial analyst engine inside a premium payment application.
    Analyze these localized workspace metrics:
    - Total monthly tracked spending: ₹{total_spend:,.2f}
    - Highest individual merchant drain: {top_merchant} (₹{top_merchant_amt:,.2f})
    - Total Food & Dining platform leak: ₹{food_spend:,.2f}
    
    Generate an elite, clean financial intelligence report.
    You must format the response as a point-by-point vertical stack.
    
    Structure the layout EXACTLY like this:
    
    <strong>CONSUMPTION REPORT CARD</strong><br>
    • <strong>Total Volume:</strong> Short single sentence tracking aggregate outflow speed.<br>
    • <strong>Primary Leakage Vector:</strong> Single concise line isolating the structural damage from {top_merchant}.<br><br>
    
    <strong>STRATEGIC INTERVENTION</strong><br>
    • <strong>Action Item:</strong> Give a clear 1-sentence behavioral rule calculating exactly how much capital can be reclaimed by sweeping 20% of their {top_merchant} habit into compounding assets.
    
    Rules:
    - Never use markdown text formatting like asterisks (**), hashtags, or markdown bullet points (- or *). 
    - Use ONLY the raw text characters or the exact HTML bold tags <strong></strong> provided above for structure.
    - Keep every line short, crisp, and clean. Do not group multiple headers or items into dense paragraphs.
    """
    try:
        response = ai_client.models.generate_content(
            model='gemini-3.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.1)
        )
        return response.text
    except Exception as e:
        return f"Error generating live financial insights: {e}"


def generate_global_predictive_runway(total_spend: float, daily_avg: float, liquid_cash: float) -> str:
    """
    Leverages Gemini 3.5 Flash to compute cross-border predictive runway risk 
    and simulate autonomous capital preservation rules.
    """
    math_runway_days = int(liquid_cash / daily_avg) if daily_avg > 0 else 90
    
    prompt = f"""
    You are a predictive liquidity engineering core built inside a global fintech middleware.
    Analyze these cross-platform ledger account parameters:
    - Total Liquid Capital Runway Available: ₹{liquid_cash:,.2f}
    - Aggregated 30-Day Velocity Outflow: ₹{total_spend:,.2f}
    - True Daily Consumption Burn Rate: ₹{daily_avg:,.2f}
    - Baseline Mathematical Exhaustion: {math_runway_days} Days
    
    Generate a minimal, enterprise-grade risk card.
    You must format the output as a clean, beautifully aligned vertical key-value list.
    
    Structure the layout EXACTLY like this:
    
    <strong>PREDICTIVE METRICS SUMMARY</strong><br>
    • <strong>System Daily Burn Rate:</strong> ₹{daily_avg:,.2f} per day<br>
    • <strong>Baseline Account Runway:</strong> {math_runway_days} Days of reserve liquidity<br><br>
    
    <strong>SYSTEMIC RISK WARNING</strong><br>
    • <strong>Downstream Friction:</strong> Identify how overlapping subscription bills compress their true cash window down to a narrow 30-day window.<br><br>
    
    <strong>AUTONOMOUS CAPITAL SAFEGUARDS</strong><br>
    • <strong>Liquidity Rebalancing:</strong> Provide 1 simple, clear structural step to execute an automated cross-account save-to-spend sweep to patch this deficit.
    
    Rules:
    - Strictly avoid dense prose or massive word wraps.
    - Never write markdown symbols like asterisks (**), hashtags, or markdown bullet layouts.
    - Rely entirely on the clean vertical HTML line breaks (<br>) and <strong></strong> configurations to ensure a premium, minimal mobile-app appearance.
    """
    try:
        response = ai_client.models.generate_content(
            model='gemini-3.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.1)
        )
        return response.text
    except Exception as e:
        return f"Predictive Liquidity Engine Offline. Error: {e}"
    
def simulate_smart_payout_routing(transfer_amount: float, source_currency: str, target_currency: str) -> str:
    """
    Leverages Gemini 3.5 Flash to simulate real-time AI smart-routing optimization 
    across multi-currency cross-border payment corridors.
    """
    prompt = f"""
    You are a high-performance smart-routing optimization engine for a global remittance infrastructure.
    Analyze this outbound payment request configuration:
    - Base Transfer Volume: {transfer_amount:,.2f} {source_currency}
    - Target Corridor Execution: {source_currency} to {target_currency}
    
    Simulate real-time network conditions across three concurrent global payment nodes:
    Node A (Traditional Correspondent Rail): High fee, 48-hour lag, stable execution.
    Node B (Open Banking Liquidity Pool): Low fee, volatile spot FX pricing, temporary target bank congestion.
    Node C (Next-Gen Tokenized Clearing Layer): Near-zero fee, optimized spot rate, zero settlement latency.
    
    Generate an elite, clear 'Smart Path Optimization Analysis'.
    You must format the response as a point-by-point vertical summary.
    
    Structure the layout EXACTLY like this:
    
    <strong>CROSS-BORDER CORRIDOR MAP</strong><br>
    • <strong>Optimal Path Selected:</strong> Identify Node C as the clear winner and specify why.<br>
    • <strong>FX Conversion Shielding:</strong> State the precise, optimal moment to finalize exchange to lock in minimal spread volatility.<br><br>
    
    <strong>AUTONOMOUS COMPLIANCE & FALLBACK</strong><br>
    • <strong>Pre-Validation Check:</strong> Confirm that automated anti-money laundering (AML) and sanctions screening checks have cleared instantly upfront.<br>
    • <strong>Failover Protocol:</strong> State the clear fallback node option if Node C drops offline unexpectedly mid-transaction.
    
    Rules:
    - Never use markdown text formatting like asterisks (**), hashtags, or markdown bullet points (- or *).
    - Use ONLY raw text characters or the exact HTML bold tags <strong></strong> provided above for structure.
    - Keep every line short, crisp, and clean. Do not group multiple headers or items into dense paragraphs.
    """
    try:
        response = ai_client.models.generate_content(
            model='gemini-3.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.1)
        )
        return response.text
    except Exception as e:
        return f"Smart Routing Engine Offline. Error: {e}"
    
def simulate_institutional_investment_strategy(portfolio_summary_json: str) -> str:
    """
    Leverages Gemini 3.5 Flash to simulate Wall Street style portfolio risk stress-testing
    and Big-Four style tax-loss harvesting logic.
    """
    prompt = f"""
    You are an institutional portfolio risk quant and corporate tax architect.
    Analyze this asset allocation registry array:
    {portfolio_summary_json}
    
    Run a high-end algorithmic simulation mapping two distinct enterprise briefs:
    Brief 1: JPMorgan Stress Test. Simulate a macro event (e.g., a 15% energy sector spike + 50bps rate shift). Project specific risk vulnerability across their equities vs fixed deposits.
    Brief 2: KPMG Tax Optimization. Isolate asset gains and deliver a clear tax-loss harvesting sweep strategy to minimize capital gains liability.
    
    Generate a clean, professional corporate executive briefing.
    You must format the output as a clean, beautifully aligned vertical key-value list with line breaks.
    
    Structure the layout EXACTLY like this:
    
    <strong>MACRO RISK STRESS-TEST</strong><br>
    • <strong>Volatility Impact Projection:</strong> State the estimated systemic portfolio value draw-down percentage under a sudden macro contraction scenario.<br>
    • <strong>Vulnerability Concentration:</strong> Identify which asset category or platform carries the highest correlation risk.<br><br>
    
    <strong>TAX INTELLIGENCE STRATEGY</strong><br>
    • <strong>Tax-Loss Harvesting Offset:</strong> Provide a direct 1-sentence balancing recommendation to offset realized gains by harvesting embedded capital losses.<br>
    • <strong>Forward Capital Shielding:</strong> Suggest a structured shift into a higher-yield tax-exempt target framework to protect next-quarter interest compounding.
    
    Rules:
    - Strictly avoid dense paragraphs or long, clustered walls of prose.
    - Never write markdown symbols like asterisks (**), hashtags, or markdown bullet points (- or *).
    - Rely entirely on the clean vertical HTML line breaks (<br>) and <strong></strong> configurations to match the premium, minimal dashboard interface layout.
    """
    try:
        response = ai_client.models.generate_content(
            model='gemini-3.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.1)
        )
        return response.text
    except Exception as e:
        return f"Institutional Risk Engine Offline. Error: {e}"