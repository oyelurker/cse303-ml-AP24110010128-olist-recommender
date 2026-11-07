import tempfile
import unittest
from pathlib import Path
import pandas as pd

from olist_shop.artifacts import load_artifacts
from olist_shop.service import ShopService
from olist_shop.store import Store


class ServiceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bundle = load_artifacts()

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.store = Store(Path(self.temp.name)/"shop.sqlite")
        self.store.ensure_customer("new", "New")
        self.service = ShopService(self.bundle, self.store)

    def tearDown(self):
        self.temp.cleanup()

    def test_interest_purchase_and_cancel_flow(self):
        engine = self.service.engine
        before = self.service.recommend("new").product_id.tolist()
        product = engine.catalog.loc[engine.catalog.category.eq("stationery")].index[0]
        self.store.toggle_interest("new", product, engine.catalog.index)
        after = self.service.recommend("new")
        self.assertNotEqual(before, after.product_id.tolist())
        self.assertTrue(after.category.eq("stationery").all())
        self.store.change_cart("new", product, 1, engine.catalog.index)
        self.assertNotIn(product, self.service.recommend("new").product_id.tolist())
        receipt = self.service.checkout("new", "once", False)
        self.assertIn(product, self.service.history_products("new").product_id.tolist())
        self.assertNotIn(product, self.service.recommend("new").product_id.tolist())
        self.store.cancel_order("new", receipt["id"])
        self.assertTrue(self.service.history_products("new").empty)

    def test_persona_rewards_and_evidence(self):
        for persona in self.bundle["personas"]:
            self.store.ensure_customer(persona["id"], persona["label"])
            offer = self.service.offer(persona["id"])
            if persona["label"] == "Frequent shopper": self.assertEqual(offer["kind"], "loyalty")
            if persona["label"] == "Returning after a break": self.assertEqual(offer["kind"], "winback")
        source = self.bundle["featured_product"]
        result = self.service.engine.also_bought(source)
        self.assertFalse(result.empty)
        self.assertTrue(result.shared_buyers.ge(2).all())
        self.assertNotIn(source, result.product_id.tolist())

    def test_assistant_uses_same_offer_and_no_fabricated_score(self):
        offer = self.service.offer("new")
        answer = self.service.reply("new", "What offer can I use?")
        self.assertIn("5%", answer)
        self.assertIn(offer["reason"], answer)
        self.assertIn("No evaluated", self.service.reply("new", "repeat score"))
        self.assertIn("No purchase history", self.service.reply("new", "What did I buy before?"))

    def test_buy_again_waits_for_known_completion(self):
        products = list(self.service.engine.catalog.index[:2])
        bundle = dict(self.bundle)
        bundle["orders"] = pd.DataFrame({
            "customer_unique_id": ["new", "new"], "order_id": ["done", "pending"],
            "order_purchase_timestamp": pd.to_datetime(["2018-05-20", "2018-05-25"]),
            "order_delivered_customer_date": pd.to_datetime(["2018-05-25", "2018-06-02"]),
        })
        bundle["items"] = pd.DataFrame({
            "customer_unique_id": ["new", "new"], "order_id": ["done", "pending"], "product_id": products,
            "order_purchase_timestamp": pd.to_datetime(["2018-05-20", "2018-05-25"]),
        })
        service = ShopService(bundle, self.store)
        self.assertEqual(service.history_products("new").product_id.tolist(), products[:1])
        self.store.advance(7)
        self.assertEqual(set(service.history_products("new").product_id), set(products))


if __name__ == "__main__":
    unittest.main()
