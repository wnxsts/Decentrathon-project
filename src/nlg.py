
from .utils import fmt_money_kzt, month_name_in_ru

def pick_month_for_row(row) -> str:
    # Если есть последняя дата транзакции, возьмем её месяц, иначе пусто.
    last_date = row.get("_last_tx_date", "")
    m = month_name_in_ru(last_date) if last_date else ""
    return m or "последнее время"

def generate_push(product: str, row, benefit_est: float) -> str:
    name = str(row.get("name", "")).strip() or "Клиент"
    balance = row.get("avg_monthly_balance_KZT", 0)
    cat1, cat2, cat3 = row.get("cat1","Категория"), row.get("cat2","Категория"), row.get("cat3","Категория")
    month = pick_month_for_row(row)

    # Заранее посчитанные суммы из FE
    travel_amt = sum([row.get("spend_Путешествия",0), row.get("spend_Отели",0), row.get("spend_Такси",0)])
    taxi_cnt = int(row.get("taxi_cnt", 0))

    if product == "Карта для путешествий":
        text = f"{name}, в {month} у вас {taxi_cnt} поездок и траты на поездки {fmt_money_kzt(travel_amt)}. С картой для путешествий часть расходов вернулась бы кешбэком ≈{fmt_money_kzt(benefit_est)}. Открыть карту."
    elif product == "Премиальная карта":
        tier_pct = "4%" if balance >= 2_000_000 else ("3%" if balance >= 1_000_000 else "2%")
        text = f"{name}, у вас стабильный остаток {fmt_money_kzt(balance)} и траты в ресторанах/косметике. Премиальная карта даст до {tier_pct} кешбэка и бесплатные снятия. Оформить сейчас."
    elif product == "Кредитная карта":
        text = f"{name}, ваши топ-категории — {cat1}, {cat2}, {cat3}. Кредитная карта даёт до 10% в любимых категориях и на онлайн-сервисы. Оформить карту."
    elif product == "Обмен валют":
        text = f"{name}, вы часто платите в USD/EUR. В приложении — выгодный обмен и авто-покупка по целевому курсу. Настроить обмен."
    elif product in ["Депозит сберегательный","Депозит накопительный","Депозит мультивалютный"]:
        text = f"{name}, свободные средства {fmt_money_kzt(balance)} можно разместить на вкладе — удобно копить и получать вознаграждение. Открыть вклад."
    elif product == "Инвестиции (брокерский счёт)":
        text = f"{name}, попробуйте инвестиции с низким порогом входа и без комиссий на старт. Открыть счёт."
    elif product == "Кредит наличными":
        text = f"{name}, если нужен запас на крупные траты — можно оформить кредит наличными с гибкими выплатами. Узнать лимит."
    else:  # Золотые слитки
        text = f"{name}, для диверсификации части средств подойдут золотые слитки. Посмотреть условия."

    # Ограничиваем 220 символов мягко
    if len(text) > 220:
        text = text[:217].rstrip() + "…"
    return text
