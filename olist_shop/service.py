"""Customer-facing operations shared by the UI and bounded assistant."""
import re

import numpy as np
import pandas as pd

from .recommendations import money


class ShopService:
    def __init__(self, bundle, store):
        self.bundle = bundle
        self.engine = bundle["engine"]
        self.store = store

    def historical_orders(self, customer):
        now = pd.Timestamp(self.store.clock())
        orders = self.bundle["orders"]
        return orders.loc[orders.customer_unique_id.eq(customer) & orders.order_purchase_timestamp.lt(now)].copy()

    def qualifying_history(self, customer):
        orders = self.historical_orders(customer)
        known = orders.order_delivered_customer_date.le(pd.Timestamp(self.store.clock())) & orders.order_delivered_customer_date.ge(orders.order_purchase_timestamp)
        return [time.to_pydatetime() for time in orders.loc[known].order_purchase_timestamp]

    def offer(self, customer):
        return self.store.offer(customer, self.qualifying_history(customer))

    def recommend(self, customer, n=5, mode="personalized"):
        return self.engine.recommend(customer, n, interests=self.store.interests(customer),
                                     purchased=self.store.purchased_products(customer), cart=self.store.cart(customer), mode=mode)

    def history_products(self, customer):
        items = self.bundle["items"]
        orders = self.historical_orders(customer)
        known = orders.order_delivered_customer_date.le(pd.Timestamp(self.store.clock())) & orders.order_delivered_customer_date.ge(orders.order_purchase_timestamp)
        completed_ids = set(orders.loc[known].order_id)
        history = items.loc[items.customer_unique_id.eq(customer) & items.order_id.isin(completed_ids)].groupby("product_id").order_purchase_timestamp.max()
        ids = list(history.sort_values(ascending=False).index)
        demo = self.store.purchased_products(customer)
        ids = sorted(demo) + [item for item in ids if item not in demo]
        return self.engine.catalog.reindex([item for item in ids if item in self.engine.catalog.index]).rename_axis("product_id").reset_index()

    def category_summary(self, customer):
        products = self.history_products(customer)
        if products.empty:
            return pd.Series(dtype="int64", name="products")
        return products.groupby("category").size().sort_values(ascending=False).rename("distinct_products")

    def insights(self, customer):
        history = self.historical_orders(customer)
        demo = [order for order in self.store.orders(customer) if order["status"] == "completed"]
        order_count = len(history) + len(demo)
        spend = float(history.items_value.sum()) + sum(order["subtotal"] for order in demo)/100
        times = list(history.order_purchase_timestamp) + [pd.Timestamp(order["at"]) for order in demo]
        if not times:
            return {"orders": 0, "spend": 0., "segment": None, "recency": None, "risk": None}
        recency = (pd.Timestamp(self.store.clock()) - max(times)).total_seconds()/86400
        rfm = pd.DataFrame([[recency, order_count, spend]], columns=["recency_days", "frequency_orders", "monetary_brl"])
        segment = int(self.bundle["rfm_model"].predict(self.bundle["rfm_scaler"].transform(np.log1p(rfm)))[0])
        risk = None
        if customer in self.bundle["risk"].index:
            row = self.bundle["risk"].loc[customer]
            if row.snapshot_at <= pd.Timestamp(self.store.clock()):
                risk = {"score": float(row.score), "snapshot": row.snapshot_at}
        return {"orders": order_count, "spend": spend, "segment": segment, "recency": recency, "risk": risk}

    def checkout(self, customer, request_key, use_offer):
        offer = self.offer(customer) if use_offer else None
        if use_offer and offer is None:
            raise ValueError("The selected reward is no longer available. Review your cart before checkout.")
        return self.store.checkout(customer, request_key, self.engine.catalog.price_cents.to_dict(),
                                   self.qualifying_history(customer), offer["id"] if offer else None)

    def reply(self, customer, message):
        """No external model: every numeric answer comes from the same service methods."""
        text = re.sub(r"[^a-z0-9 ]", " ", message.lower())
        if any(word in text for word in ["discount", "offer", "coupon", "reward"]):
            offer = self.offer(customer)
            if not offer:
                return "There is no eligible reward right now. Eligibility uses completed orders and redemption cooldowns, not page visits."
            rule = offer["rule"]
            return (f"{rule.title}: {rule.basis_points/100:g}% off, minimum cart {money(rule.minimum_cents)}, "
                    f"maximum saving {money(rule.cap_cents)}. {offer['reason']} Expires {offer['expires'][:10]}. "
                    "This is a demo offer, not an optimized retention intervention.")
        if any(word in text for word in ["why", "explain", "reason"]):
            recommendations = self.recommend(customer, 1)
            if recommendations.empty:
                return "There are no eligible products to explain."
            row = recommendations.iloc[0]
            return f"{row.label}: {row.reason}. Category has weight 2 and historical price band weight 1. The score is similarity, not purchase probability."
        if any(word in text for word in ["history", "before", "again", "bought"]):
            history = self.history_products(customer).head(5)
            return "No purchase history yet. Try a simulated order." if history.empty else "Previously purchased: " + "; ".join(history.label) + ". Buy again is a history shortcut, separate from discovery recommendations."
        if any(word in text for word in ["segment", "summary", "customer", "insight"]):
            result = self.insights(customer)
            return ("No purchase history yet, so no RFM segment is assigned." if result["segment"] is None else
                    f"{result['orders']} observed placed/demo orders; merchandise value R$ {result['spend']:,.2f}; "
                    f"RFM segment {result['segment']}. Groups describe history and do not prove future loyalty.")
        if any(word in text for word in ["repeat", "risk", "score", "predict"]):
            risk = self.insights(customer)["risk"]
            return ("No evaluated fixed-age historical score is available for this customer." if risk is None else
                    f"Experimental score {risk['score']:.4f}, calculated at the original 30-day customer-age snapshot on {risk['snapshot']:%Y-%m-%d}. "
                    "It predicts a next-90-day placed-order target. Test ROC-AUC was 0.4746, so it is not a reliable current retention forecast.")
        if any(word in text for word in ["recommend", "suggest", "similar", "cart"]):
            recommendations = self.recommend(customer, 3, "cart" if "cart" in text else "personalized")
            return "Suggestions: " + "; ".join(f"{row.label} ({money(row.price_cents)})" for row in recommendations.itertuples()) + ". These use historical prices and demo preferences."
        return "I can recommend products, explain a suggestion, summarize purchase history or a segment, and check reward eligibility. Try: ‘What offer can I use?’"
