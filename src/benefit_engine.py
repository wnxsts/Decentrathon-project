
import pandas as pd
from .config import PREMIUM_TIERS, LIMITS, PROXIES, ELIGIBILITY, CATS

def _premium_tier(balance: float) -> float:
    for thr, pct in PREMIUM_TIERS:
        if balance >= thr:
            return pct
    return PREMIUM_TIERS[-1][1]

def _sum_cats(row, names):
    return sum([row.get(f"spend_{n}", 0) for n in names])

def compute_benefits(feat_row: pd.Series) -> dict:
    r = feat_row
    spend_total = r.get("spend_total", 0.0)
    balance = r.get("avg_monthly_balance_KZT", 0.0)

    # Travel
    travel_spend = _sum_cats(r, CATS["travel"])
    taxi_spend = _sum_cats(r, CATS["taxi"])
    travel_benefit = min(0.04 * (travel_spend + taxi_spend), LIMITS["travel_cb"]) \
                   + min(0.01 * r.get("fx_spend_usd_eur", 0.0), LIMITS["travel_fx_bonus"])

    # Premium
    tier = _premium_tier(balance)
    premium_benefit = min(tier * spend_total, LIMITS["premium_base"]) \
        + min(0.04 * (_sum_cats(r, CATS["jewelry"]) + _sum_cats(r, CATS["cosmetics"]) + _sum_cats(r, CATS["restaurants"])), LIMITS["premium_boost"]) \
        + min(r.get("atm_withdrawal_cnt", r.get("atm_cnt", 0)) * 300, LIMITS["atm_saving"]) \
        + min((r.get("p2p_out_cnt", r.get("p2p_cnt", 0)) + r.get("card_out_cnt", 0)) * 100, LIMITS["transfer_saving"])

    # Credit card
    fav_spend = sum([r.get(f"spend_{r.get('cat1','')}",0), r.get(f"spend_{r.get('cat2','')}",0), r.get(f"spend_{r.get('cat3','')}",0)])
    cc_benefit = min(0.10 * fav_spend, LIMITS["cc_fav"]) \
               + min(0.10 * _sum_cats(r, CATS["online_home"]), LIMITS["cc_online"]) \
               + (PROXIES["grace_proxy"] * spend_total if (bool(r.get("has_installments", False)) or bool(r.get("has_cc", False))) else 0)

    # FX
    fx_benefit = min(PROXIES["fx_spread_saving"] * r.get("fx_spend_usd_eur", 0.0), LIMITS["fx_total"])

    # Cash loan (бинарная релевантность)
    loan_elig = (r.get("cash_gap_ratio", 0) >= ELIGIBILITY["cash_loan"]["gap_ratio_min"]) and (balance < ELIGIBILITY["cash_loan"]["balance_max"])
    loan_benefit = 1 if loan_elig else 0

    # Multi-currency deposit
    mc_elig = (balance >= ELIGIBILITY["mc_deposit"]["balance_min"]) and (r.get("fx_spend_usd_eur", 0) > 0)
    mc_benefit = min(PROXIES["mc_rate"] * balance, LIMITS["mc_deposit"]) if mc_elig else 0

    # Saving deposit (заморозка) — волатильности может не быть, ставим прокси 0.1 если неизвестно
    volatility = r.get("volatility", 0.10)
    save_elig = (balance >= ELIGIBILITY["save_deposit"]["balance_min"]) and (volatility <= ELIGIBILITY["save_deposit"]["volatility_max"])
    save_benefit = min(PROXIES["save_rate"] * balance, LIMITS["save_deposit"]) if save_elig else 0

    # Accumulating deposit
    acc_elig = (ELIGIBILITY["acc_deposit"]["balance_min"] <= balance < ELIGIBILITY["acc_deposit"]["balance_max"]) and (r.get("inflows",0) > 0)
    acc_benefit = min(PROXIES["acc_rate"] * balance, LIMITS["acc_deposit"]) if acc_elig else 0

    # Investments
    online_home = _sum_cats(r, CATS["online_home"])
    online_share = (online_home / spend_total) if spend_total > 0 else 0
    invest_elig = (balance >= ELIGIBILITY["invest"]["balance_min"]) and (online_share < ELIGIBILITY["invest"]["online_share_max"])
    invest_benefit = 3_000 if invest_elig else 0

    # Gold
    glam = _sum_cats(r, CATS["jewelry"]) + _sum_cats(r, CATS["cosmetics"])
    glam_share = (glam / spend_total) if spend_total > 0 else 0
    gold_elig = (balance >= ELIGIBILITY["gold"]["balance_min_or"]) or (glam_share > ELIGIBILITY["gold"]["glam_share_min_or"])
    gold_benefit = 2_000 if gold_elig else 0

    return {
        "Карта для путешествий": travel_benefit,
        "Премиальная карта": premium_benefit,
        "Кредитная карта": cc_benefit,
        "Обмен валют": fx_benefit,
        "Кредит наличными": loan_benefit,
        "Депозит мультивалютный": mc_benefit,
        "Депозит сберегательный": save_benefit,
        "Депозит накопительный": acc_benefit,
        "Инвестиции (брокерский счёт)": invest_benefit,
        "Золотые слитки": gold_benefit,
    }
