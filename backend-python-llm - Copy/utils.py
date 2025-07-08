import re
from datetime import datetime, timedelta

def normalize_currency(text):
    """
    Extract currency pairs like EUR/USD or USD/JPY from text.
    """
    match = re.search(r'[A-Z]{3}/[A-Z]{3}', text.upper())
    return match.group(0) if match else None

def parse_date(text):
    """
    Very basic parsing for 'today' or 'tomorrow'.
    Extend with NLP or dateparser later.
    """
    today = datetime.now().date()

    if "tomorrow" in text.lower():
        return str(today + timedelta(days=1))
    elif "today" in text.lower():
        return str(today)

    return None
