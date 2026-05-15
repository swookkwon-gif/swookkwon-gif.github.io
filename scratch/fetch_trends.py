import pandas as pd
from pytrends.request import TrendReq
import time

pytrends = TrendReq(hl='en-US', tz=360)
kw_list = ["Criteo", "RTB house"]

countries = {
    'Global': '',
    'United States': 'US',
    'Japan': 'JP',
    'South Korea': 'KR',
    'Singapore': 'SG',
    'Indonesia': 'ID',
    'Thailand': 'TH',
    'Taiwan': 'TW',
    'Hong Kong': 'HK',
    'United Kingdom': 'GB',
    'France': 'FR',
    'Germany': 'DE',
    'Italy': 'IT',
    'Spain': 'ES',
    'Netherlands': 'NL',
    'Poland': 'PL',
    'Vietnam': 'VN',
    'Malaysia': 'MY',
    'Philippines': 'PH',
    'India': 'IN',
    'Australia': 'AU'
}

results = []

for name, geo in countries.items():
    try:
        pytrends.build_payload(kw_list, cat=0, timeframe='today 5-y', geo=geo, gprop='')
        df = pytrends.interest_over_time()
        if not df.empty:
            mean_criteo = df['Criteo'].mean()
            mean_rtb = df['RTB house'].mean()
            results.append({
                'Country': name,
                'Criteo_Avg': mean_criteo,
                'RTB_House_Avg': mean_rtb
            })
            print(f"Success: {name} (Criteo: {mean_criteo:.2f}, RTB: {mean_rtb:.2f})")
        else:
            print(f"Empty data for {name}")
    except Exception as e:
        print(f"Error for {name}: {e}")
    time.sleep(2) # To avoid rate limits

df_results = pd.DataFrame(results)
print("\n--- Summary ---")
print(df_results)
