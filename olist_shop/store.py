"""SQLite persistence and atomic, idempotent simulated checkout."""
from contextlib import contextmanager
from datetime import datetime, timedelta
from pathlib import Path
import json
import sqlite3
import uuid

from .rewards import RULES, eligible_rule, discount_cents


class Store:
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.connection() as db:
            db.executescript("""
                CREATE TABLE IF NOT EXISTS customers(id TEXT PRIMARY KEY, label TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS settings(key TEXT PRIMARY KEY, value TEXT NOT NULL);
                INSERT OR IGNORE INTO settings VALUES('clock','2018-06-01T00:00:00');
                CREATE TABLE IF NOT EXISTS cart(customer TEXT, product TEXT, qty INTEGER CHECK(qty BETWEEN 1 AND 10), PRIMARY KEY(customer,product));
                CREATE TABLE IF NOT EXISTS interests(customer TEXT, product TEXT, PRIMARY KEY(customer,product));
                CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY, customer TEXT, type TEXT, product TEXT, at TEXT, detail TEXT);
                CREATE TABLE IF NOT EXISTS orders(id TEXT PRIMARY KEY, customer TEXT NOT NULL, at TEXT NOT NULL,
                    status TEXT NOT NULL CHECK(status IN ('completed','cancelled')), subtotal INTEGER NOT NULL,
                    discount INTEGER NOT NULL, total INTEGER NOT NULL, request_key TEXT NOT NULL,
                    UNIQUE(customer,request_key));
                CREATE TABLE IF NOT EXISTS order_items(order_id TEXT REFERENCES orders(id), product TEXT, qty INTEGER,
                    price INTEGER, PRIMARY KEY(order_id,product));
                CREATE TABLE IF NOT EXISTS coupons(id TEXT PRIMARY KEY, customer TEXT NOT NULL, kind TEXT NOT NULL,
                    issued TEXT NOT NULL, expires TEXT NOT NULL, redeemed_order TEXT REFERENCES orders(id));
            """)

    @contextmanager
    def connection(self, write=False):
        db = sqlite3.connect(self.path, timeout=10)
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA foreign_keys=ON")
        try:
            if write:
                db.execute("BEGIN IMMEDIATE")
            yield db
            db.commit()
        except BaseException:
            db.rollback()
            raise
        finally:
            db.close()

    def clock(self):
        with self.connection() as db:
            return datetime.fromisoformat(db.execute("SELECT value FROM settings WHERE key='clock'").fetchone()[0])

    def advance(self, days):
        if not isinstance(days, int) or isinstance(days, bool) or days <= 0:
            raise ValueError("Advance by a positive whole number of days.")
        with self.connection(write=True) as db:
            now = self._clock(db) + timedelta(days=days)
            if now > datetime(2018, 8, 30):
                raise ValueError("The demo timeline ends on 30 August 2018.")
            db.execute("UPDATE settings SET value=? WHERE key='clock'", (now.isoformat(),))
        return now

    @staticmethod
    def _clock(db):
        return datetime.fromisoformat(db.execute("SELECT value FROM settings WHERE key='clock'").fetchone()[0])

    @staticmethod
    def _event(db, customer, kind, now, product=None, detail=None):
        db.execute("INSERT INTO events(customer,type,product,at,detail) VALUES(?,?,?,?,?)",
                   (customer, kind, product, now.isoformat(), json.dumps(detail or {})))

    def ensure_customer(self, customer, label):
        with self.connection() as db:
            db.execute("INSERT OR IGNORE INTO customers VALUES(?,?)", (customer, label))

    def create_shopper(self, nickname):
        """Create once per normalized demo nickname, including concurrent submissions.

        Existing duplicate profiles are preserved; reuse the earliest matching one.
        Historical customer personas are outside this demo-name lookup.
        """
        label = " ".join(nickname.split())
        if not label or len(label) > 40:
            raise ValueError("Enter a shopper nickname between 1 and 40 characters.")
        with self.connection(write=True) as db:
            for row in db.execute("SELECT id,label FROM customers WHERE id LIKE 'demo-%' ORDER BY rowid"):
                if " ".join(row["label"].split()).casefold() == label.casefold():
                    return {"id": row["id"], "label": row["label"], "created": False}
            customer = "demo-" + uuid.uuid4().hex[:12]
            db.execute("INSERT INTO customers VALUES(?,?)", (customer, label))
            return {"id": customer, "label": label, "created": True}

    def customers(self):
        with self.connection() as db:
            return [dict(row) for row in db.execute("SELECT * FROM customers ORDER BY rowid")]

    def cart(self, customer):
        with self.connection() as db:
            return {row["product"]: row["qty"] for row in db.execute("SELECT product,qty FROM cart WHERE customer=? ORDER BY product", (customer,))}

    def change_cart(self, customer, product, delta, valid_products):
        if product not in valid_products or not isinstance(delta, int) or isinstance(delta, bool):
            raise ValueError("Unknown product or invalid quantity.")
        with self.connection(write=True) as db:
            row = db.execute("SELECT qty FROM cart WHERE customer=? AND product=?", (customer, product)).fetchone()
            qty = (row[0] if row else 0) + delta
            if qty > 10 or qty < 0:
                raise ValueError("Quantity must be between zero and ten.")
            if qty == 0:
                db.execute("DELETE FROM cart WHERE customer=? AND product=?", (customer, product))
            else:
                db.execute("INSERT INTO cart VALUES(?,?,?) ON CONFLICT(customer,product) DO UPDATE SET qty=excluded.qty", (customer, product, qty))
            self._event(db, customer, "cart_add" if delta > 0 else "cart_remove", self._clock(db), product)

    def interests(self, customer):
        with self.connection() as db:
            return {row[0] for row in db.execute("SELECT product FROM interests WHERE customer=?", (customer,))}

    def toggle_interest(self, customer, product, valid_products):
        if product not in valid_products:
            raise ValueError("Unknown product.")
        with self.connection(write=True) as db:
            exists = db.execute("SELECT 1 FROM interests WHERE customer=? AND product=?", (customer, product)).fetchone()
            if exists:
                db.execute("DELETE FROM interests WHERE customer=? AND product=?", (customer, product))
            else:
                db.execute("INSERT INTO interests VALUES(?,?)", (customer, product))
            self._event(db, customer, "interest_remove" if exists else "interest", self._clock(db), product)

    def viewed(self, customer, product):
        with self.connection() as db:
            self._event(db, customer, "view", self._clock(db), product)

    def events(self, customer, limit=30):
        with self.connection() as db:
            return [dict(row) for row in db.execute("SELECT * FROM events WHERE customer=? ORDER BY id DESC LIMIT ?", (customer, limit))]

    def orders(self, customer):
        with self.connection() as db:
            return [dict(row) for row in db.execute("SELECT * FROM orders WHERE customer=? ORDER BY at DESC,id", (customer,))]

    def purchased_products(self, customer):
        with self.connection() as db:
            return {row[0] for row in db.execute("SELECT DISTINCT product FROM order_items JOIN orders ON order_items.order_id=orders.id WHERE customer=? AND status='completed'", (customer,))}

    @staticmethod
    def _purchase_times(db, customer, historical_times, now):
        times = list(historical_times)
        times.extend(datetime.fromisoformat(row[0]) for row in db.execute(
            "SELECT at FROM orders WHERE customer=? AND status='completed' AND at<=?", (customer, now.isoformat())))
        return times

    @staticmethod
    def _rule_available(db, customer, rule, now):
        redemptions = db.execute("SELECT o.at FROM coupons c JOIN orders o ON c.redeemed_order=o.id WHERE c.customer=? AND c.kind=? ORDER BY o.at DESC", (customer, rule.kind)).fetchall()
        if not redemptions:
            return True
        if rule.cooldown_days is None:
            return False
        return now - datetime.fromisoformat(redemptions[0][0]) >= timedelta(days=rule.cooldown_days)

    def offer(self, customer, historical_times):
        with self.connection(write=True) as db:
            now = self._clock(db)
            rule, reason = eligible_rule(self._purchase_times(db, customer, historical_times, now), now)
            if rule is None or not self._rule_available(db, customer, rule, now):
                return None
            coupon = db.execute("SELECT * FROM coupons WHERE customer=? AND kind=? AND redeemed_order IS NULL AND expires>? ORDER BY issued DESC LIMIT 1",
                                (customer, rule.kind, now.isoformat())).fetchone()
            if coupon is None:
                coupon_id = uuid.uuid4().hex
                db.execute("INSERT INTO coupons VALUES(?,?,?,?,?,NULL)",
                           (coupon_id, customer, rule.kind, now.isoformat(), (now+timedelta(days=7)).isoformat()))
                coupon = db.execute("SELECT * FROM coupons WHERE id=?", (coupon_id,)).fetchone()
            return {**dict(coupon), "reason": reason, "rule": rule}

    def checkout(self, customer, request_key, price_map, historical_times, coupon_id=None):
        """All prices come from the server catalog. Repeated request keys return the same order."""
        if not request_key:
            raise ValueError("Checkout request key is required.")
        with self.connection(write=True) as db:
            prior = db.execute("SELECT * FROM orders WHERE customer=? AND request_key=?", (customer, request_key)).fetchone()
            if prior is not None:
                return dict(prior)
            now = self._clock(db)
            cart = db.execute("SELECT product,qty FROM cart WHERE customer=? ORDER BY product", (customer,)).fetchall()
            if not cart:
                raise ValueError("Your cart is empty.")
            if any(row["product"] not in price_map for row in cart):
                raise ValueError("A cart product is no longer in the demo catalog.")
            subtotal = sum(int(price_map[row["product"]])*row["qty"] for row in cart)
            discount = 0
            if coupon_id:
                coupon = db.execute("SELECT * FROM coupons WHERE id=? AND customer=?", (coupon_id, customer)).fetchone()
                current_rule, _ = eligible_rule(self._purchase_times(db, customer, historical_times, now), now)
                if coupon is None or coupon["redeemed_order"] or coupon["expires"] <= now.isoformat():
                    raise ValueError("This offer is unavailable or expired.")
                if current_rule is None or current_rule.kind != coupon["kind"] or not self._rule_available(db, customer, current_rule, now):
                    raise ValueError("Your current order history does not qualify for this offer.")
                discount = discount_cents(current_rule, subtotal)
                if not discount:
                    raise ValueError("The offer minimum cart value has not been reached.")
            order_id = uuid.uuid4().hex
            db.execute("INSERT INTO orders VALUES(?,?,?,'completed',?,?,?,?)",
                       (order_id, customer, now.isoformat(), subtotal, discount, subtotal-discount, request_key))
            db.executemany("INSERT INTO order_items VALUES(?,?,?,?)", [(order_id, row["product"], row["qty"], int(price_map[row["product"]])) for row in cart])
            if coupon_id:
                db.execute("UPDATE coupons SET redeemed_order=? WHERE id=?", (order_id, coupon_id))
            db.execute("DELETE FROM cart WHERE customer=?", (customer,))
            self._event(db, customer, "checkout", now, detail={"order": order_id})
            return dict(db.execute("SELECT * FROM orders WHERE id=?", (order_id,)).fetchone())

    def cancel_order(self, customer, order_id):
        with self.connection(write=True) as db:
            result = db.execute("UPDATE orders SET status='cancelled' WHERE id=? AND customer=? AND status='completed'", (order_id, customer))
            if result.rowcount != 1:
                raise ValueError("Completed demo order not found.")
            # A cancelled order does not restore an already redeemed coupon or grant a new one.
            self._event(db, customer, "cancel_order", self._clock(db), detail={"order": order_id})

    def receipt_items(self, customer, order_id):
        with self.connection() as db:
            return [dict(row) for row in db.execute("SELECT product,qty,price FROM order_items JOIN orders ON order_items.order_id=orders.id WHERE orders.customer=? AND orders.id=?", (customer, order_id))]
