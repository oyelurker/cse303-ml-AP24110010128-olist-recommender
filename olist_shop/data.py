"""Preparation and historical features extracted from notebook Sections 3 and 5.

Only the six source tables needed for these features are loaded. Payment and
geolocation audits remain in the notebook; neither is a selected predictor.
"""
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

NUMERIC = [
    "recency_days", "historical_order_count", "distinct_products", "distinct_sellers",
    "log1p_merchandise_spend", "log1p_average_order_value", "freight_ratio",
    "known_review_count", "mean_known_review_score", "known_delivery_count",
    "mean_known_delivery_days",
]
REDUCED_NUMERIC = [name for name in NUMERIC if name != "log1p_average_order_value"]
FEATURES = NUMERIC + ["customer_state"]
BASE_DATE = pd.Timestamp("2018-06-01")


@dataclass
class PreparedData:
    orders: pd.DataFrame
    items: pd.DataFrame
    products: pd.DataFrame


def load_data(raw_dir: Path) -> PreparedData:
    def read(name, **kwargs):
        return pd.read_csv(raw_dir / name, **kwargs)

    orders = read("olist_orders_dataset.csv")
    customers = read("olist_customers_dataset.csv", dtype={"customer_zip_code_prefix": "string"})
    items = read("olist_order_items_dataset.csv")
    reviews = read("olist_order_reviews_dataset.csv")
    products = read("olist_products_dataset.csv")
    translation = read("product_category_name_translation.csv")
    for column in ["order_purchase_timestamp", "order_approved_at", "order_delivered_carrier_date",
                   "order_delivered_customer_date", "order_estimated_delivery_date"]:
        orders[column] = pd.to_datetime(orders[column], format="%Y-%m-%d %H:%M:%S", errors="coerce")
    for column in ["review_creation_date", "review_answer_timestamp"]:
        reviews[column] = pd.to_datetime(reviews[column], format="%Y-%m-%d %H:%M:%S", errors="coerce")
    if items.duplicated(["order_id", "order_item_id"]).any():
        raise ValueError("Duplicate order-item keys require investigation.")
    if items[["price", "freight_value"]].isna().any().any() or (items[["price", "freight_value"]] < 0).any().any():
        raise ValueError("Missing or negative item amounts.")
    products = products.merge(translation, on="product_category_name", how="left", validate="many_to_one")
    products["category_label"] = products.product_category_name_english.fillna(
        "untranslated__" + products.product_category_name
    ).fillna("unknown")
    purchase_times = orders.set_index("order_id").order_purchase_timestamp
    reviews["associated_purchase_at"] = reviews.order_id.map(purchase_times)
    eligible = reviews.loc[reviews.associated_purchase_at.notna() &
                           reviews.review_answer_timestamp.ge(reviews.associated_purchase_at)].copy()
    if reviews.duplicated(["review_id", "order_id"]).any() or reviews.review_answer_timestamp.isna().any():
        raise ValueError("Review keys/availability require investigation.")
    first_review = eligible.sort_values(
        ["order_id", "review_answer_timestamp", "review_creation_date", "review_id"], kind="stable"
    ).drop_duplicates("order_id")[["order_id", "review_score", "review_answer_timestamp"]].rename(columns={
        "review_score": "first_review_score", "review_answer_timestamp": "first_review_available_at",
    })
    summary = items.groupby("order_id", as_index=False).agg(
        item_count=("order_item_id", "size"), items_value=("price", "sum"), freight_total=("freight_value", "sum"),
    )
    facts = orders.merge(customers[["customer_id", "customer_unique_id", "customer_state"]],
                         on="customer_id", how="left", validate="many_to_one")
    facts = facts.merge(summary, on="order_id", how="left", validate="one_to_one").merge(
        first_review, on="order_id", how="left", validate="one_to_one"
    )
    facts = facts.loc[facts.item_count.notna() & facts.order_purchase_timestamp.lt("2018-09-01")].copy()
    events = items.merge(facts[["order_id", "customer_unique_id", "order_purchase_timestamp"]],
                         on="order_id", how="inner", validate="many_to_one").merge(
        products[["product_id", "category_label"]], on="product_id", how="left", validate="many_to_one"
    )
    return PreparedData(facts, events, products)


def retention_dataset(data: PreparedData) -> pd.DataFrame:
    """Reproduce the notebook's fixed-age, full-follow-up research dataset."""
    first = data.orders.groupby("customer_unique_id").order_purchase_timestamp.min()
    snapshots = first.rename("first_observed_purchase_at").to_frame()
    snapshots["snapshot_at"] = snapshots.first_observed_purchase_at + pd.Timedelta(days=30)
    snapshots["outcome_end"] = snapshots.snapshot_at + pd.Timedelta(days=90)
    snapshots = snapshots.loc[snapshots.snapshot_at.ge("2017-01-01") & snapshots.outcome_end.lt("2018-09-01")].reset_index()
    events = data.orders.merge(snapshots, on="customer_unique_id", how="inner", validate="many_to_one")
    history = events.loc[events.order_purchase_timestamp.le(events.snapshot_at)].sort_values(
        ["customer_unique_id", "order_purchase_timestamp", "order_id"]
    ).copy()
    future = events.loc[events.order_purchase_timestamp.gt(events.snapshot_at) & events.order_purchase_timestamp.le(events.outcome_end)]
    snapshots["repeat_90d"] = snapshots.customer_unique_id.map(future.groupby("customer_unique_id").order_id.nunique()).fillna(0).gt(0).astype(int)
    purchase = history.groupby("customer_unique_id").agg(
        historical_order_count=("order_id", "nunique"), merchandise_spend=("items_value", "sum"),
        average_order_value=("items_value", "mean"), historical_freight=("freight_total", "sum"),
        latest_historical_purchase_at=("order_purchase_timestamp", "max"), customer_state=("customer_state", "first"),
    ).reset_index()
    history_items = data.items.merge(history[["order_id", "customer_unique_id", "snapshot_at"]],
                                    on=["order_id", "customer_unique_id"], how="inner", validate="many_to_one")
    breadth = history_items.groupby("customer_unique_id").agg(
        distinct_products=("product_id", "nunique"), distinct_sellers=("seller_id", "nunique")
    ).reset_index()
    known_review = history.first_review_available_at.notna() & history.first_review_available_at.le(history.snapshot_at)
    known_delivery = history.order_delivered_customer_date.notna() & history.order_delivered_customer_date.le(history.snapshot_at) & history.order_delivered_customer_date.ge(history.order_purchase_timestamp)
    history["known_review_score"] = history.first_review_score.where(known_review)
    history["known_delivery_days"] = (history.order_delivered_customer_date.where(known_delivery) - history.order_purchase_timestamp).dt.total_seconds() / 86400
    known = history.groupby("customer_unique_id").agg(
        known_review_count=("known_review_score", "count"), mean_known_review_score=("known_review_score", "mean"),
        known_delivery_count=("known_delivery_days", "count"), mean_known_delivery_days=("known_delivery_days", "mean"),
    ).reset_index()
    result = snapshots.merge(purchase, on="customer_unique_id", validate="one_to_one").merge(
        breadth, on="customer_unique_id", validate="one_to_one"
    ).merge(known, on="customer_unique_id", validate="one_to_one")
    result["recency_days"] = (result.snapshot_at - result.latest_historical_purchase_at).dt.total_seconds() / 86400
    result["freight_ratio"] = result.historical_freight / result.merchandise_spend
    result["log1p_merchandise_spend"] = np.log1p(result.merchandise_spend)
    result["log1p_average_order_value"] = np.log1p(result.average_order_value)
    return result


def rfm_snapshot(orders: pd.DataFrame, cutoff) -> pd.DataFrame:
    history = orders.loc[orders.order_purchase_timestamp.lt(pd.Timestamp(cutoff))]
    frame = history.groupby("customer_unique_id").agg(
        frequency_orders=("order_id", "nunique"), monetary_brl=("items_value", "sum"),
        last_order_at=("order_purchase_timestamp", "max"),
    ).sort_index()
    frame["recency_days"] = (pd.Timestamp(cutoff) - frame.last_order_at).dt.total_seconds() / 86400
    return frame[["recency_days", "frequency_orders", "monetary_brl"]]
