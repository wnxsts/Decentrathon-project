
import pandas as pd
import numpy as np
from .utils import to_kzt

def build_features(clients: pd.DataFrame, tx: pd.DataFrame, tr: pd.DataFrame) -> pd.DataFrame:
    # Приведение типов и KZT
    tx = tx.copy()
    tr = tr.copy()
    tx["amt_kzt"] = tx.apply(lambda r: to_kzt(r["amount"], str(r["currency"])), axis=1)
    tr["amt_kzt"] = tr.apply(lambda r: to_kzt(r["amount"], str(r["currency"])), axis=1)

    # Суммы по категориям
    tx_cat = tx.groupby(["client_code","category"])["amt_kzt"].sum().unstack(fill_value=0)
    tx_cat.columns = [f"spend_{c}" for c in tx_cat.columns]

    # Общие расходы
    spend_total = tx.groupby("client_code")["amt_kzt"].sum().rename("spend_total")

    # Счетчики
    taxi_cnt = (tx[tx["category"]=="Такси"].groupby("client_code")["category"].count()
                .rename("taxi_cnt"))

    # USD/EUR траты (в KZT-эквиваленте уже)
    fx_spend = (tx[tx["currency"].isin(["USD","EUR"])].groupby("client_code")["amt_kzt"].sum()
                .rename("fx_spend_usd_eur"))

    # Transfers агрегаты
    def cnt(type_name):
        return (tr[tr["type"]==type_name].groupby("client_code")["type"].count()
                .rename(f"{type_name}_cnt"))

    atm_cnt = cnt("atm_withdrawal")
    p2p_cnt = cnt("p2p_out")
    card_out_cnt = cnt("card_out")
    has_installments = (tr[tr["type"]=="installment_payment_out"].groupby("client_code")["type"].count()>0).rename("has_installments")
    has_cc = (tr[tr["type"]=="cc_repayment_out"].groupby("client_code")["type"].count()>0).rename("has_cc")

    inflows = tr[tr["direction"]=="in"].groupby("client_code")["amt_kzt"].sum().rename("inflows")
    outflows = tr[tr["direction"]=="out"].groupby("client_code")["amt_kzt"].sum().rename("outflows")
    io = pd.concat([inflows, outflows], axis=1).fillna(0)
    io["cash_gap_ratio"] = io["outflows"] / io["inflows"].replace(0, 1)

    # Сборка фич
    feat = (clients.set_index("client_code")
            .join([tx_cat, spend_total, taxi_cnt, fx_spend, atm_cnt, p2p_cnt, card_out_cnt, has_installments, has_cc, io], how="left")
            .fillna(0))

    # Вычислим топ-3 категории (названия и суммы)
    cat_cols = [c for c in feat.columns if c.startswith("spend_")]
    def top3(row):
        pairs = sorted([(c[6:], row[c]) for c in cat_cols], key=lambda kv: -kv[1])
        top = [p[0] for p in pairs[:3]] + ["", "", ""]
        return pd.Series({"cat1": top[0], "cat2": top[1], "cat3": top[2]})
    feat = pd.concat([feat, feat.apply(top3, axis=1)], axis=1)

    return feat.reset_index()
