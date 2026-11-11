import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from pathlib import Path

from olist_shop.rewards import eligible_rule, discount_cents, RULES
from olist_shop.store import Store


class RewardTests(unittest.TestCase):
    def test_boundaries_and_caps(self):
        now = datetime(2018, 6, 1)
        self.assertEqual(eligible_rule([], now)[0].kind, "welcome")
        self.assertIsNone(eligible_rule([now-timedelta(days=60)], now)[0])
        self.assertEqual(eligible_rule([now-timedelta(days=61)], now)[0].kind, "winback")
        self.assertIsNone(eligible_rule([now]*3, now)[0])
        times = [now-timedelta(days=90), now-timedelta(days=1), now]
        self.assertEqual(eligible_rule(times, now)[0].kind, "loyalty")
        self.assertIsNone(eligible_rule([now-timedelta(days=91), now-timedelta(days=1), now], now)[0])
        self.assertEqual(discount_cents(RULES["welcome"], 9999), 0)
        self.assertEqual(discount_cents(RULES["welcome"], 10000), 500)
        self.assertEqual(discount_cents(RULES["loyalty"], 100000), 2500)


class StoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.store = Store(Path(self.temp.name)/"test.sqlite")
        self.store.ensure_customer("a", "Alice")
        self.store.ensure_customer("b", "Bob")
        self.prices = {"p": 20000, "q": 50000}

    def tearDown(self):
        self.temp.cleanup()

    def add(self, user="a", product="p"):
        self.store.change_cart(user, product, 1, self.prices)

    def test_atomic_idempotent_checkout_and_isolation(self):
        self.add(); self.add("b", "q")
        coupon = self.store.offer("a", [])
        receipt = self.store.checkout("a", "one-request", self.prices, [], coupon["id"])
        self.assertEqual(receipt["discount"], 1000)
        self.assertEqual(receipt["total"], 19000)
        repeated = self.store.checkout("a", "one-request", self.prices, [], coupon["id"])
        self.assertEqual(receipt["id"], repeated["id"])
        self.assertEqual(len(self.store.orders("a")), 1)
        self.assertEqual(self.store.cart("a"), {})
        self.assertEqual(self.store.cart("b"), {"q": 1})
        self.assertEqual(self.store.receipt_items("b", receipt["id"]), [])
        self.store.cancel_order("a", receipt["id"])
        self.assertEqual(self.store.purchased_products("a"), set())
        self.assertIsNone(self.store.offer("a", []))  # redeemed welcome is not restored by cancellation

    def test_wrong_owner_expiry_and_minimum_rollback(self):
        self.add("b")
        coupon = self.store.offer("a", [])
        with self.assertRaises(ValueError):
            self.store.checkout("b", "bad-owner", self.prices, [], coupon["id"])
        self.assertEqual(len(self.store.orders("b")), 0)
        self.assertEqual(self.store.cart("b"), {"p": 1})
        self.add()
        self.store.advance(7)
        with self.assertRaises(ValueError):
            self.store.checkout("a", "expired", self.prices, [], coupon["id"])
        self.assertEqual(self.store.cart("a"), {"p": 1})
        fresh = self.store.offer("a", [])
        with self.assertRaises(ValueError):
            self.store.checkout("a", "minimum", {"p": 5000}, [], fresh["id"])
        self.assertEqual(len(self.store.orders("a")), 0)

    def test_loyalty_cooldown_and_cancellation_eligibility(self):
        historical = [datetime(2018, 5, 29), datetime(2018, 5, 30), datetime(2018, 5, 31)]
        coupon = self.store.offer("a", historical)
        self.assertEqual(coupon["kind"], "loyalty")
        self.add()
        receipt = self.store.checkout("a", "loyalty", self.prices, historical, coupon["id"])
        self.assertIsNone(self.store.offer("a", historical))
        self.store.advance(30)
        self.assertEqual(self.store.offer("a", historical)["kind"], "loyalty")
        with self.assertRaises(ValueError):
            self.store.cancel_order("b", receipt["id"])

    def test_invalid_quantity_and_cross_customer_interests(self):
        with self.assertRaises(ValueError):
            self.store.change_cart("a", "unknown", 1, self.prices)
        with self.assertRaises(ValueError):
            self.store.change_cart("a", "p", 11, self.prices)
        self.store.toggle_interest("a", "p", self.prices)
        self.assertEqual(self.store.interests("a"), {"p"})
        self.assertEqual(self.store.interests("b"), set())
        self.assertEqual(Store(self.store.path).interests("a"), {"p"})

    def test_concurrent_duplicate_request_creates_one_order(self):
        self.add()
        with ThreadPoolExecutor(max_workers=2) as executor:
            results = list(executor.map(lambda _: self.store.checkout("a", "same-key", self.prices, []), range(2)))
        self.assertEqual(results[0]["id"], results[1]["id"])
        self.assertEqual(len(self.store.orders("a")), 1)

    def test_create_shopper_normalizes_and_reuses_name(self):
        first = self.store.create_shopper("  Test   User 1  ")
        second = self.store.create_shopper("test user 1")
        self.assertTrue(first["created"])
        self.assertFalse(second["created"])
        self.assertEqual(first["id"], second["id"])
        self.assertEqual(first["label"], "Test User 1")
        with self.assertRaises(ValueError):
            self.store.create_shopper("   ")
        self.assertEqual(len(self.store.customers()), 3)

    def test_concurrent_shopper_creation_and_legacy_profiles(self):
        with ThreadPoolExecutor(max_workers=2) as executor:
            profiles = list(executor.map(lambda _: self.store.create_shopper("Review shopper"), range(2)))
        self.assertEqual(profiles[0]["id"], profiles[1]["id"])
        self.assertEqual(sum(profile["created"] for profile in profiles), 1)
        self.store.ensure_customer("demo-old-first", "Legacy user")
        self.store.ensure_customer("demo-old-second", "Legacy user")
        reused = self.store.create_shopper("LEGACY USER")
        self.assertEqual(reused["id"], "demo-old-first")
        self.assertFalse(reused["created"])
        self.assertEqual(len(self.store.customers()), 5)


if __name__ == "__main__":
    unittest.main()
