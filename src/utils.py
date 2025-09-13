
from datetime import datetime
from .config import MONTHS_IN

# Заглушка конвертации: можно расширить реальными курсами при наличии
def to_kzt(amount: float, currency: str) -> float:
    rates = {"KZT": 1.0, "USD": 470.0, "EUR": 510.0}  
    return float(amount) * rates.get(currency, 1.0)

def month_name_in_ru(dt_str: str) -> str:
    try:
        m = datetime.fromisoformat(dt_str[:10]).month
        return MONTHS_IN[m-1]
    except Exception:
        return ""

def fmt_money_kzt(x: float) -> str:
    # Формат: разряды пробелом и знак валюты: "27 400 ₸"
    s = f"{int(round(x)):,}".replace(",", " ")
    return f"{s} ₸"
