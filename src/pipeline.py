
import argparse
import pandas as pd
from .feature_engineering import build_features
from .benefit_engine import compute_benefits
from .nlg import generate_push
from .utils import to_kzt

PRODUCT_ORDER = [
    "Карта для путешествий",
    "Премиальная карта",
    "Кредитная карта",
    "Обмен валют",
    "Кредит наличными",
    "Депозит мультивалютный",
    "Депозит сберегательный",
    "Депозит накопительный",
    "Инвестиции (брокерский счёт)",
    "Золотые слитки"
]

def main(args):
    clients = pd.read_csv(args.clients)
    tx = pd.read_csv(args.transactions)
    tr = pd.read_csv(args.transfers)

    # Для месяца в пуше — возьмем последнюю дату транзакции на клиента
    tx["_date"] = pd.to_datetime(tx["date"])
    last_tx = tx.sort_values("_date").groupby("client_code")["_date"].last().rename("_last_tx_date").astype(str)

    feat = build_features(clients, tx, tr).set_index("client_code")
    feat = feat.join(last_tx, how="left")

    # Сохраним фичи для диагностики
    if args.features_out:
        feat.to_parquet(args.features_out, index=True)

    # Выгоды и Top-4
    benefits_df = pd.DataFrame([compute_benefits(row) for _,row in feat.iterrows()], index=feat.index)
    # Сохраним Top-4 для проверки
    top4 = benefits_df.apply(lambda s: list(s.sort_values(ascending=False).index[:4]), axis=1)
    top4_out = pd.DataFrame({"client_code": top4.index, "top1": top4.str[0], "top2": top4.str[1], "top3": top4.str[2], "top4": top4.str[3]})
    if args.top4_out:
        top4_out.to_csv(args.top4_out, index=False)

    # Победитель и пуш
    winners = benefits_df.idxmax(axis=1)
    best_vals = benefits_df.max(axis=1)

    rows = []
    for cid, product in winners.items():
        row = feat.loc[cid]
        benefit_est = float(best_vals.loc[cid])
        push = generate_push(product, row, benefit_est)
        rows.append({"client_code": cid, "product": product, "push_notification": push})

    out = pd.DataFrame(rows).sort_values("client_code")
    out.to_csv(args.out, index=False)
    print(f"Wrote {args.out} (rows={len(out)})")
    if args.top4_out:
        print(f"Wrote {args.top4_out}")
    if args.features_out:
        print(f"Wrote {args.features_out}")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--clients", required=True)
    p.add_argument("--transactions", required=True)
    p.add_argument("--transfers", required=True)
    p.add_argument("--out", default="submission.csv")
    p.add_argument("--top4_out", default="top4.csv")
    p.add_argument("--features_out", default="features.parquet")
    main(p.parse_args())
