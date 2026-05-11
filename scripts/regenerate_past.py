import os
import sys
import json
from datetime import datetime, timezone, timedelta
from unittest.mock import patch
from gf2_auto_blogger import run_gemini_search_blogger
from daily_digest import merge_and_create_digest

def run_for_date(target_date_str):
    print(f"\n--- Regenerating for {target_date_str} ---")
    target_date = datetime.strptime(target_date_str, "%Y-%m-%d").date()
    now_kst = datetime.combine(target_date, datetime.min.time()).replace(tzinfo=timezone(timedelta(hours=9)))
    
    # Mock datetime.now
    class MockDatetime(datetime):
        @classmethod
        def now(cls, tz=None):
            return now_kst
            
    # Mocking in gf2_auto_blogger
    with patch('gf2_auto_blogger.datetime', MockDatetime):
        run_gemini_search_blogger()
        
    # Mocking in daily_digest.py
    # Empty daily_articles.json so that it only uses the deep research
    state_dir = os.path.join(os.path.dirname(__file__), 'state')
    os.makedirs(state_dir, exist_ok=True)
    daily_articles_path = os.path.join(state_dir, 'daily_articles.json')
    
    # Save empty articles
    empty_articles = {
        "date": target_date_str,
        "generated_at": now_kst.isoformat(),
        "total_articles": 0,
        "articles": []
    }
    with open(daily_articles_path, 'w', encoding='utf-8') as f:
        json.dump(empty_articles, f, ensure_ascii=False, indent=2)
        
    with patch('daily_digest.datetime', MockDatetime):
        merge_and_create_digest()

if __name__ == "__main__":
    run_for_date("2026-05-09")
    run_for_date("2026-05-10")
    run_for_date("2026-05-11")
