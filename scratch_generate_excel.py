import pandas as pd
import os

# 1. Market Overview Data (New Sheet)
market_overview_data = {
    "Category": ["Total Ad Market (2025E)", "Digital Ad Market (2025E)"],
    "Market Size (KRW)": ["~ 17.2 Trillion KRW", "~ 10.3 Trillion KRW (60% share)"],
    "YoY Growth": ["~ 2.8%", "Low single-digit (Maturity stage)"],
    "Key Trends": ["Digital & DOOH leading growth", "AI adoption & Retail Media expansion"]
}

vertical_spend_data = {
    "Industry Vertical": ["E-Commerce & Retail", "Gaming & Mobile Apps", "Travel & OTA", "Finance & Fintech"],
    "Est. Share of Digital Spend": ["35-40%", "20-25%", "10-15%", "10-15%"],
    "Ad-Tech Focus": ["Dynamic Retargeting, ROAS, Retail Media", "App Install, LTV, ROAS, Re-engagement", "Search, Dynamic Retargeting, Contextual", "Lead Gen, Secure Acquisition, Branding"]
}

key_players_data = {
    "Player (Platform/AdTech)": ["Naver", "Google / YouTube Korea", "Kakao", "Meta (Facebook/Instagram) Korea", "Criteo Korea", "RTB House Korea", "Moloco"],
    "Est. Korea Ad Revenue (KRW)": ["~ 3.5 Trillion+", "~ 2.5 - 3 Trillion", "~ 1.5 Trillion+", "~ 1 Trillion+", "~ 70B - 120B (Est.)", "~ 15B - 20B (Est.)", "Global: $1B+ (Korea growing fast)"],
    "Core Strength": ["Search & Local Display", "Video (YouTube) & Programmatic (GDN)", "Messenger-based Display (Bizboard)", "Social Display & Advanced Targeting", "Commerce Media & Retargeting dominance", "100% Deep Learning, Performance niche", "Machine Learning for Mobile App UA"]
}

# 2. Strategy Data
strategy_data = {
    "Category": ["High-Level Strategy", "High-Level Strategy", "High-Level Strategy", "Top Prospective Clients", "Top Prospective Clients", "Top Prospective Clients"],
    "Focus Area / Client": ["E-Commerce & Retail", "Travel (OTA)", "Gaming & App", "Coupang, Musinsa, Kurly", "Yanolja, MyRealTrip", "NCSOFT, Netmarble"],
    "Rationale & Strategy": [
        "Highly sensitive to ROAS and incrementality. Deep Learning excels in complex catalog environments.",
        "High AOV and long conversion paths. Perfect for DL-based predictive targeting.",
        "Need for high LTV user acquisition. In-app retargeting is a massive growth lever.",
        "A/B Testing against Criteo (Head-to-head). Prove iROAS and win budget share.",
        "Pitch cookieless readiness and dynamic ad personalization based on user travel intent.",
        "Offer predictive LTV modeling and in-app event optimization to boost ARPU."
    ]
}

# 3. Metrics Data
metrics_data = {
    "Quarter": ["Q1 (Baseline)", "Q2 (Ramp Up)", "Q3 (Scaling)", "Q4 (Peak Season)"],
    "Target New Campaigns": [30, 50, 75, 120],
    "Est. Value per Salesperson (Quarterly)": ["$200,000", "$350,000", "$500,000", "$800,000"],
    "Key Focus (Sales & Ops)": [
        "Pipeline generation & Cookieless educational webinars",
        "A/B test launches & Case study creation",
        "Upselling video ads & In-app retargeting",
        "Max budget capture during Black Friday/Holiday season"
    ]
}

# 4. Ops Data
ops_data = {
    "Activity Type": ["Employer Branding", "Innovative Solution Selling", "Market Education", "Client Success"],
    "Action Plan": [
        "Position RTB House as a premium 'AI & Deep Learning' tech company. Host tech-talks to attract top talent.",
        "Beyond standard display: Push Video Ads, Social Banners, and Cookieless solutions proactively.",
        "Publish whitepapers and articles on 'Incrementality vs Attribution' to change market perception.",
        "Implement quarterly QBRs focusing on true Causal Lift, moving away from simple Last-Click ROAS."
    ]
}

df_market_overview = pd.DataFrame(market_overview_data)
df_vertical_spend = pd.DataFrame(vertical_spend_data)
df_key_players = pd.DataFrame(key_players_data)
df_strategy = pd.DataFrame(strategy_data)
df_metrics = pd.DataFrame(metrics_data)
df_ops = pd.DataFrame(ops_data)

output_path = "/Users/wook/Downloads/RTB_House_Korea_3Year_Strategy_v2.xlsx"

with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
    # Write Market Overview sheets
    df_market_overview.to_excel(writer, sheet_name='1. Market Size', index=False)
    df_vertical_spend.to_excel(writer, sheet_name='2. Vertical Breakdown', index=False)
    df_key_players.to_excel(writer, sheet_name='3. Key Players Revenue', index=False)
    
    # Write Strategy & Ops sheets
    df_strategy.to_excel(writer, sheet_name='4. Strategy & Focus', index=False)
    df_metrics.to_excel(writer, sheet_name='5. Execution & Metrics', index=False)
    df_ops.to_excel(writer, sheet_name='6. Operational Activities', index=False)

print(f"Excel file successfully created at: {output_path}")
