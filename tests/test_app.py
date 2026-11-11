"""Actual Streamlit page interactions; database is isolated from the user's demo."""
import os
from pathlib import Path
import tempfile
import unittest

from streamlit.testing.v1 import AppTest
from olist_shop.artifacts import load_artifacts
from olist_shop.store import Store


class AppFlowTests(unittest.TestCase):
    def test_create_shopper_clears_confirms_and_blocks_duplicates(self):
        with tempfile.TemporaryDirectory() as directory:
            old = os.environ.get("OLIST_DEMO_DB")
            database = Path(directory)/"creation.sqlite"
            os.environ["OLIST_DEMO_DB"] = str(database)
            try:
                at = AppTest.from_file(Path(__file__).resolve().parents[1]/"app.py", default_timeout=30).run()
                store = Store(database)
                initial_count = len(store.customers())
                at.text_input(key="new_profile_name").set_value("Review shopper")
                at.button(key="create_shopper_submit").click().run()
                self.assertEqual(len(at.exception), 0)
                selected = at.session_state["customer_picker"]
                self.assertEqual(at.text_input(key="new_profile_name").value, "")
                self.assertTrue(any("Created Review shopper" in message.value for message in at.success))
                self.assertEqual(len(store.customers()), initial_count+1)
                # The now-empty form must not create a generic shopper on another click.
                at.button(key="create_shopper_submit").click().run()
                self.assertEqual(len(at.exception), 0)
                self.assertEqual(len(store.customers()), initial_count+1)
                self.assertEqual(at.session_state["customer_picker"], selected)
                at.text_input(key="new_profile_name").set_value("  review SHOPPER  ")
                at.button(key="create_shopper_submit").click().run()
                self.assertEqual(len(at.exception), 0)
                self.assertEqual(len(store.customers()), initial_count+1)
                self.assertEqual(at.session_state["customer_picker"], selected)
                self.assertTrue(any("already exists" in message.value for message in at.info))
                at.text_input(key="new_profile_name").set_value("Separate shopper")
                at.button(key="create_shopper_submit").click().run()
                self.assertEqual(len(at.exception), 0)
                self.assertEqual(len(store.customers()), initial_count+2)
            finally:
                if old is None: os.environ.pop("OLIST_DEMO_DB", None)
                else: os.environ["OLIST_DEMO_DB"] = old

    def test_shopping_checkout_history_and_assistant(self):
        with tempfile.TemporaryDirectory() as directory:
            old = os.environ.get("OLIST_DEMO_DB")
            os.environ["OLIST_DEMO_DB"] = str(Path(directory)/"ui.sqlite")
            try:
                at = AppTest.from_file(Path(__file__).resolve().parents[1] / "app.py", default_timeout=30).run()
                self.assertEqual(len(at.exception), 0)
                customer = at.session_state["customer_picker"]
                catalog = load_artifacts()["engine"].catalog
                product = catalog.loc[catalog.price_cents.between(10000, 20000)].index[0]
                next(field for field in at.text_input if field.label == "Search category or product ID").set_value(product).run()
                add = at.button(key=f"add_browse_{product}")
                add.click().run()
                self.assertEqual(len(at.exception), 0)
                at.radio(key="navigation").set_value("Cart").run()
                self.assertEqual(len(at.exception), 0)
                self.assertTrue(at.checkbox)
                at.checkbox[0].check().run()
                checkout = next(button for button in at.button if button.label == "Place simulated order")
                checkout.click().run()
                self.assertEqual(len(at.exception), 0)
                self.assertTrue(any("confirmed" in message.value for message in at.success))
                self.assertGreater(at.session_state[f"receipt_{customer}"]["discount"], 0)
                at.radio(key="navigation").set_value("Orders & rewards").run()
                self.assertEqual(len(at.exception), 0)
                self.assertTrue(any(button.key == f"add_again_{product}" for button in at.button))
                at.radio(key="navigation").set_value("Insights").run()
                self.assertEqual(len(at.exception), 0)
                at.radio(key="navigation").set_value("Assistant").run()
                next(button for button in at.button if button.label == "What offer can I use?").click().run()
                self.assertEqual(len(at.exception), 0)
                self.assertIn("reward", str(at.session_state[f"chat_{customer}"][-1]["content"]).lower())
                at.radio(key="navigation").set_value("Shop").run()
                next(button for button in at.button if button.label == "Try shared-buyer example").click().run()
                self.assertEqual(len(at.exception), 0)
                self.assertTrue(any("Other shoppers also bought" in heading.value for heading in at.subheader))
                # Change customer: no prior product-detail state or cart crosses identities.
                options = at.selectbox(key="customer_picker").options
                self.assertGreater(len(options), 1)
                at.selectbox(key="customer_picker").set_value(customer).run()
                self.assertEqual(len(at.exception), 0)
                self.assertNotIn("selected_product", at.session_state)
            finally:
                if old is None: os.environ.pop("OLIST_DEMO_DB", None)
                else: os.environ["OLIST_DEMO_DB"] = old


if __name__ == "__main__":
    unittest.main()
