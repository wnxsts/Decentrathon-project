
# Параметры и лимиты выгод/кешбэка/экономии

# Границы премиум-уровней по остатку
PREMIUM_TIERS = [
    (2_000_000, 0.04),  # ≥ 2 000 000 -> 4%
    (1_000_000, 0.03),  # ≥ 1 000 000 -> 3%
    (0,         0.02),  # иначе -> 2%
]

# Лимиты кешбэка/экономии по продуктам (в ₸ в мес)
LIMITS = {
    "travel_cb": 15_000,
    "travel_fx_bonus": 5_000,
    "premium_base": 20_000,
    "premium_boost": 15_000,
    "atm_saving": 6_000,
    "transfer_saving": 4_000,
    "cc_fav": 18_000,
    "cc_online": 10_000,
    "fx_total": 12_000,
    "mc_deposit": 18_000,
    "save_deposit": 30_000,
    "acc_deposit": 16_000,
}

# Процентные параметры (прокси)
PROXIES = {
    "fx_spread_saving": 0.003,     # 0.3%
    "grace_proxy": 0.002,          # 0.2% от total spend
    "mc_rate": 0.012,              # 1.2%/мес
    "save_rate": 0.015,            # 1.5%/мес
    "acc_rate": 0.013,             # 1.3%/мес
}

# Условия релевантности некоторых продуктов
ELIGIBILITY = {
    "cash_loan": {
        "gap_ratio_min": 1.3,
        "balance_max": 300_000
    },
    "mc_deposit": {
        "balance_min": 600_000
    },
    "save_deposit": {
        "balance_min": 1_000_000,
        "volatility_max": 0.15
    },
    "acc_deposit": {
        "balance_min": 200_000,
        "balance_max": 1_000_000
    },
    "invest": {
        "balance_min": 400_000,
        "online_share_max": 0.20
    },
    "gold": {
        "balance_min_or": 1_500_000,
        "glam_share_min_or": 0.10
    }
}

# Категории-алиасы
CATS = {
    "restaurants": ["Кафе и рестораны"],
    "cosmetics": ["Косметика и Парфюмерия"],
    "jewelry": ["Ювелирные украшения"],
    "online_home": ["Едим дома", "Смотрим дома", "Играем дома"],
    "travel": ["Путешествия", "Отели"],
    "taxi": ["Такси"],
}

# Выбор месяцев в NLG (локализация родительного падежа)
MONTHS_IN = ["январе","феврале","марте","апреле","мае","июне","июле","августе","сентябре","октябре","ноябре","декабре"]
