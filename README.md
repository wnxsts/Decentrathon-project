
# Personalized Push Marketing — Solution

Готовый проект для кейса: рассчитать выгоду по продуктам, выбрать лучший и сгенерировать персональный пуш.

## Структура
```
personalized_marketing_project/
├─ data/
│  ├─ clients.csv                 # вход: клиенты
│  ├─ transactions.csv            # вход: транзакции (3 мес)
│  ├─ transfers.csv               # вход: переводы (3 мес)
├─ src/
│  ├─ config.py                   # параметры, лимиты, маппинги категорий
│  ├─ utils.py                    # конвертация валют, форматирование
│  ├─ feature_engineering.py      # агрегации и признаки
│  ├─ benefit_engine.py           # расчет выгод по всем продуктам
│  ├─ nlg.py                      # генерация пуш-сообщений
│  ├─ pipeline.py                 # CLI: читает вход, пишет submission.csv
├─ requirements.txt
└─ README.md
```

## Быстрый старт
1. Поместите **ваши** 3 файла в папку `data/` (схемы — ниже).
2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
3. Запустите пайплайн:
   ```bash
   python -m src.pipeline --clients data/clients.csv --transactions data/transactions.csv --transfers data/transfers.csv --out submission.csv
   ```
4. На выходе получите `submission.csv` с колонками: `client_code,product,push_notification`.
   Дополнительно создаются `top4.csv` (Top-4 продуктов) и `features.parquet` (диагностика фич).

## Схемы входных файлов
**clients.csv**
- `client_code` (int)
- `name` (str)
- `status` (Студент | Зарплатный клиент | Премиальный клиент | Стандартный клиент)
- `age` (int)
- `city` (str)
- `avg_monthly_balance_KZT` (float/int)

**transactions.csv**
- `date` (YYYY-MM-DD)
- `category` (строго из списка в ТЗ)
- `amount` (число)
- `currency` (KZT|USD|EUR)
- `client_code` (int)

**transfers.csv**
- `date` (YYYY-MM-DD)
- `type` (salary_in, stipend_in, family_in, cashback_in, refund_in, card_in, p2p_out, card_out, atm_withdrawal, utilities_out, loan_payment_out, cc_repayment_out, installment_payment_out, fx_buy, fx_sell, invest_out, invest_in, deposit_topup_out, deposit_fx_topup_out, deposit_fx_withdraw_in, gold_buy_out, gold_sell_in)
- `direction` (in|out)
- `amount` (число)
- `currency` (KZT|USD|EUR)
- `client_code` (int)

## Проверка качества
- Точность выбора продукта: сверить Top-1/Top-4 с эталоном.
- Качество пуша (4×5): персонализация, тон, ясность/CTA, редполитика.
- В `src/config.py` вы можете подстраивать лимиты/пороговые значения — логика стабильная и не привязана к открытому/скрытому сетам.

Удачи на сдаче! 💪
