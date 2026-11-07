"""Run with: python -m streamlit run app.py"""
import os
from pathlib import Path
import uuid

import pandas as pd
import streamlit as st

from olist_shop.artifacts import ARTIFACT, ROOT, build_artifacts, load_artifacts
from olist_shop.recommendations import money
from olist_shop.rewards import discount_cents
from olist_shop.service import ShopService
from olist_shop.store import Store

st.set_page_config(page_title="Olist Studio · Your next good pick", page_icon="◒", layout="wide")
st.markdown("""<style>
 .block-container {max-width:1350px;padding-top:2rem;padding-bottom:3rem}
 h1,h2,h3 {letter-spacing:-.035em} h1 {font-size:3rem !important}
 [data-testid="stVerticalBlockBorderWrapper"] {border-radius:16px}
 [data-testid="stMetricValue"] {font-size:1.8rem}
 .eyebrow {font-size:.76rem;letter-spacing:.18em;font-weight:700;color:#66786D}
 .hero {background:#E8EDE3;padding:28px 32px;border-radius:20px;margin:12px 0 24px}
 .hero h1 {margin:0}.hero p {color:#52665C;margin-bottom:0}
 .brand {font-weight:800;font-size:1.65rem;letter-spacing:-.06em;color:#19312B}
 .small-label {color:#69796F;font-size:.8rem}
 </style>""", unsafe_allow_html=True)


@st.cache_resource
def resources(modified, database):
    return load_artifacts(), Store(database)


if not ARTIFACT.exists():
    st.title("Prepare your Olist shopping demo")
    st.write("Build the local catalog and saved models once from the CSVs in data/raw. Normal app startup then loads the saved artifacts.")
    if st.button("Prepare local demo", type="primary"):
        with st.spinner("Preparing the historical catalog and fitted models…"):
            try:
                build_artifacts()
                st.rerun()
            except (OSError, ValueError) as error:
                st.error(str(error))
    st.stop()

database = os.environ.get("OLIST_DEMO_DB", str(ROOT / ".app_data" / "shop.sqlite"))
bundle, store = resources(ARTIFACT.stat().st_mtime_ns, database)
service = ShopService(bundle, store)
engine = service.engine
for persona in bundle["personas"]:
    store.ensure_customer(persona["id"], persona["label"])
if "customer_picker" not in st.session_state:
    guest = "demo-" + uuid.uuid4().hex[:12]
    store.ensure_customer(guest, "New shopper")
    st.session_state.customer_picker = guest


def customer_changed():
    st.session_state.pop("selected_product", None)


def create_profile():
    label = st.session_state.get("new_profile_name", "").strip()[:40] or "New shopper"
    customer_id = "demo-" + uuid.uuid4().hex[:12]
    store.ensure_customer(customer_id, label)
    st.session_state.customer_picker = customer_id
    st.session_state.pop("selected_product", None)


def choose_featured():
    persona = next((row for row in bundle["personas"] if row["label"] == "Explore shared-buyer suggestions"), None)
    if persona:
        st.session_state.customer_picker = persona["id"]
    st.session_state.selected_product = bundle["featured_product"]
    st.session_state.navigation = "Shop"


with st.sidebar:
    st.markdown('<div class="brand">◒ olist studio</div>', unsafe_allow_html=True)
    st.caption("A shopping demo that remembers your choices.")
    customers = store.customers()
    labels = {row["id"]: row["label"] for row in customers}
    st.selectbox("Demo customer", list(labels), format_func=lambda value: f"{labels[value]} · {value[:6]}",
                 key="customer_picker", on_change=customer_changed)
    st.caption("Demo identities only. No real account sign-in.")
    with st.expander("Create a fresh shopper"):
        with st.form("new_profile"):
            st.text_input("Shopper nickname", key="new_profile_name", max_chars=40)
            st.form_submit_button("Create shopper", on_click=create_profile)
    st.radio("Explore", ["Shop", "Cart", "Orders & rewards", "Insights", "Assistant"], key="navigation", label_visibility="collapsed")
    sidebar_cart = store.cart(st.session_state.customer_picker)
    st.caption(f"Cart · {sum(sidebar_cart.values())} items · {money(sum(int(engine.catalog.loc[item, 'price_cents'])*qty for item, qty in sidebar_cart.items()))}")
    st.divider()
    st.caption(f"DEMO DATE · {store.clock():%d %b %Y}")
    with st.expander("Move the demo forward"):
        st.caption("The shared clock advances for all demo shoppers. Historical catalog data stays fixed; new orders are simulated.")
        days = st.selectbox("Advance by", [1, 7, 30, 61], format_func=lambda value: f"{value} day{'s' if value != 1 else ''}")
        if st.button("Advance demo date"):
            try:
                store.advance(days)
                st.rerun()
            except ValueError as error:
                st.warning(str(error))
    if bundle["featured_product"]:
        st.button("Try shared-buyer example", on_click=choose_featured, width="stretch")
    st.caption("Historical Olist catalog · Reference prices in BRL · Simulated orders and rewards")

customer = st.session_state.customer_picker
page = st.session_state.navigation
cart = store.cart(customer)
interests = store.interests(customer)
demo_purchases = store.purchased_products(customer)
offer = service.offer(customer)


def change_cart(product, delta):
    try:
        store.change_cart(customer, product, delta, engine.catalog.index)
        st.rerun()
    except ValueError as error:
        st.warning(str(error))


def icon(category):
    for term, emoji in [("stationery", "✏️"), ("computer", "💻"), ("electronic", "🔌"),
                        ("furniture", "🪑"), ("bed", "🛏️"), ("fashion", "🧥"),
                        ("sport", "⚽"), ("beauty", "🧴"), ("toy", "🧸"), ("garden", "🌱"),
                        ("kitchen", "🍽️"), ("book", "📚"), ("auto", "🚗")]:
        if term in category:
            return emoji
    return "📦"


def render_cards(frame, prefix, columns=3):
    if frame.empty:
        st.caption("No products match this section right now.")
        return
    for start in range(0, len(frame), columns):
        cols = st.columns(columns)
        for col, row in zip(cols, frame.iloc[start:start+columns].itertuples()):
            with col, st.container(border=True):
                st.markdown(f"### {icon(row.category)}")
                st.markdown(f"**{row.label}**")
                st.write(money(row.price_cents))
                if hasattr(row, "shared_buyers"):
                    st.caption(f"Both items appear in {row.shared_buyers} historical shoppers’ order records.")
                elif hasattr(row, "reason"):
                    st.caption(row.reason)
                else:
                    st.caption("Demo label · Historical reference price")
                buttons = st.columns(2)
                if buttons[0].button("View", key=f"view_{prefix}_{row.product_id}", width="stretch"):
                    store.viewed(customer, row.product_id)
                    st.session_state.selected_product = row.product_id
                    st.rerun()
                if buttons[1].button("Add to cart", key=f"add_{prefix}_{row.product_id}", width="stretch"):
                    change_cart(row.product_id, 1)
                saved = row.product_id in interests
                if st.button("♥ Interest saved" if saved else "♡ Save interest", key=f"interest_{prefix}_{row.product_id}", width="stretch"):
                    store.toggle_interest(customer, row.product_id, engine.catalog.index)
                    st.rerun()


def render_offer():
    if not offer:
        st.caption("Rewards use completed purchases, with expiry and redemption limits. Browsing and page visits do not earn order rewards.")
        return
    rule = offer["rule"]
    with st.container(border=True):
        st.markdown(f"**{rule.title} · {rule.basis_points/100:g}% off**")
        st.write(offer["reason"])
        st.caption(f"Minimum {money(rule.minimum_cents)} · Save up to {money(rule.cap_cents)} · Expires {offer['expires'][:10]} · One use · Demo offer")


def product_detail(product):
    if product not in engine.catalog.index:
        st.warning("Product not found in the historical catalog.")
        return
    if st.button("← Back to shopping"):
        st.session_state.pop("selected_product", None)
        st.rerun()
    row = engine.catalog.loc[product]
    left, right = st.columns([1, 2])
    with left, st.container(border=True):
        st.markdown(f"# {icon(row.category)}")
        st.caption("Category illustration")
    with right:
        st.caption(row.category.upper())
        st.header(row.label)
        st.subheader(money(row.price_cents))
        st.caption("Historical reference price. The source provides anonymized IDs and categories, so this is a demo label, not a verified product title or live inventory listing.")
        if st.button("Add this item to cart", type="primary"):
            change_cart(product, 1)
        if st.button("Remove saved interest" if product in interests else "Save this interest"):
            store.toggle_interest(customer, product, engine.catalog.index)
            st.rerun()
    exclude = engine.seen(customer) | demo_purchases | set(cart)
    st.subheader("Other shoppers also bought")
    together = engine.also_bought(product, 3, exclude)
    if together.empty:
        st.info("This item has too little shared-buyer evidence for an ‘also bought’ claim.")
        st.caption("Popular alternatives")
        render_cards(engine.recommend(customer, 3, mode="popular", purchased=demo_purchases, cart=cart, extra_exclude={product}), "detailpopular")
    else:
        st.caption("Each pair has at least two shared historical buyers. Purchases may be from different orders; this does not establish same-basket buying or compatibility.")
        render_cards(together, "alsobought")
    st.subheader("Similar category & price band")
    render_cards(engine.similar(product, 3, exclude), "similar")


if page == "Shop":
    selected = st.session_state.get("selected_product")
    if selected:
        product_detail(selected)
    else:
        st.markdown('<div class="eyebrow">YOUR SHOPPING SPACE</div><div class="hero"><h1>Find your next good pick.</h1><p>Discover familiar categories, save an interest, and make the next suggestion more yours.</p></div>', unsafe_allow_html=True)
        render_offer()
        st.subheader("Picked for you" if engine.seen(customer) or interests or demo_purchases else "Popular places to start")
        st.caption("Purchase history and saved interests shape these suggestions. Purchased and cart items are excluded.")
        render_cards(service.recommend(customer, 3), "personal")
        categories = service.category_summary(customer)
        if not categories.empty:
            st.write("**Your familiar categories**")
            st.caption(" · ".join(f"{name.title()} ({count} distinct products)" for name, count in categories.head(4).items()))
        recent = []
        for event in store.events(customer):
            if event["type"] == "view" and event["product"] in engine.catalog.index and event["product"] not in recent:
                recent.append(event["product"])
        if recent:
            with st.expander("Recently viewed"):
                render_cards(engine.catalog.reindex(recent[:3]).rename_axis("product_id").reset_index(), "recent")
        st.divider()
        st.subheader("Explore the catalog")
        filters = st.columns([2, 2, 1])
        query = filters[0].text_input("Search category or product ID", placeholder="Try stationery, garden or a product ID")
        category = filters[1].selectbox("Category", ["All categories"] + sorted(engine.catalog.category.unique()))
        price_range = filters[2].selectbox("Price range", ["Any price", "Under R$ 50", "R$ 50–150", "Over R$ 150"])
        catalog = engine.catalog.copy()
        catalog["historical_buyers"] = engine.popularity
        if query:
            catalog = catalog.loc[catalog.label.str.contains(query, case=False, regex=False) | catalog.index.to_series().str.contains(query, case=False, regex=False)]
        if category != "All categories":
            catalog = catalog.loc[catalog.category.eq(category)]
        if price_range == "Under R$ 50": catalog = catalog.loc[catalog.price_cents < 5000]
        elif price_range == "R$ 50–150": catalog = catalog.loc[catalog.price_cents.between(5000, 15000)]
        elif price_range == "Over R$ 150": catalog = catalog.loc[catalog.price_cents > 15000]
        catalog = catalog.sort_values(["historical_buyers", "label"], ascending=[False, True])
        pages = max(1, (len(catalog)+8)//9)
        page_number = st.number_input("Catalog page", min_value=1, max_value=pages, value=1)
        st.caption(f"{len(catalog):,} matching products · page {page_number} of {pages}")
        render_cards(catalog.iloc[(page_number-1)*9:page_number*9].rename_axis("product_id").reset_index(), "browse")

elif page == "Cart":
    st.title("Your cart")
    st.caption("Simulated checkout. No payment, shipment or real discount is created.")
    if not cart:
        st.info("Your cart is empty. Find a product you like in Shop.")
        receipt = st.session_state.get(f"receipt_{customer}")
        if receipt:
            st.success(f"Demo order {receipt['id'][:8].upper()} confirmed · Total {money(receipt['total'])} · Saved {money(receipt['discount'])}")
    else:
        subtotal = 0
        for product, quantity in cart.items():
            row = engine.catalog.loc[product]
            subtotal += int(row.price_cents)*quantity
            with st.container(border=True):
                columns = st.columns([5, 1, 1, 1])
                columns[0].write(f"**{row.label}** · {money(row.price_cents)} each")
                if columns[1].button("−", key=f"minus_{product}"):
                    change_cart(product, -1)
                columns[2].write(f"Qty {quantity}")
                if columns[3].button("+", key=f"plus_{product}"):
                    change_cart(product, 1)
        render_offer()
        use_offer = False
        if offer:
            eligible_discount = discount_cents(offer["rule"], subtotal)
            use_offer = st.checkbox("Apply this demo offer", disabled=not eligible_discount, key=f"coupon_{offer['id']}")
            if not eligible_discount:
                st.caption(f"Add {money(max(0, offer['rule'].minimum_cents-subtotal))} more to activate the offer.")
        saving = discount_cents(offer["rule"], subtotal) if offer and use_offer else 0
        columns = st.columns(3)
        columns[0].metric("Merchandise subtotal", money(subtotal))
        columns[1].metric("Demo discount", money(saving))
        columns[2].metric("Total", money(subtotal-saving))
        if st.button("Place simulated order", type="primary"):
            key = st.session_state.setdefault(f"checkout_key_{customer}", uuid.uuid4().hex)
            try:
                receipt = service.checkout(customer, key, use_offer)
                st.session_state[f"receipt_{customer}"] = receipt
                st.session_state[f"checkout_key_{customer}"] = uuid.uuid4().hex
                st.rerun()
            except ValueError as error:
                st.error(str(error))
        st.subheader("Related to your cart")
        st.caption("Temporary cart-context suggestions; separate from evaluated purchase-history recommendations.")
        render_cards(service.recommend(customer, 3, "cart"), "cart")

elif page == "Orders & rewards":
    st.title("Your history, your next visit")
    render_offer()
    st.subheader("Buy again")
    st.caption("A shortcut to earlier purchases. This shelf intentionally includes purchased items.")
    render_cards(service.history_products(customer).head(6), "again")
    st.subheader("Simulated orders")
    orders = store.orders(customer)
    if not orders:
        st.caption("No simulated orders yet.")
    for order in orders:
        with st.expander(f"{order['id'][:8].upper()} · {order['at'][:10]} · {money(order['total'])} · {order['status']}"):
            rows = store.receipt_items(customer, order["id"])
            for row in rows:
                st.write(f"{engine.catalog.loc[row['product'], 'label']} × {row['qty']} · {money(row['price']*row['qty'])}")
            st.caption(f"Subtotal {money(order['subtotal'])} · Reward {money(order['discount'])}")
            if order["status"] == "completed" and st.button("Cancel demo order", key=f"cancel_{order['id']}"):
                store.cancel_order(customer, order["id"])
                st.rerun()
    with st.expander("Original historical orders"):
        history = service.historical_orders(customer).sort_values("order_purchase_timestamp", ascending=False).head(20)
        if history.empty:
            st.caption("This demo shopper has no original Olist orders.")
        else:
            known = history.order_delivered_customer_date.le(pd.Timestamp(store.clock())) & history.order_delivered_customer_date.ge(history.order_purchase_timestamp)
            view = pd.DataFrame({"Purchase date": history.order_purchase_timestamp.dt.strftime("%Y-%m-%d"),
                                 "Merchandise BRL": history.items_value, "Completion known": known})
            st.dataframe(view, hide_index=True, width="stretch")

elif page == "Insights":
    st.title("Customer insights")
    st.caption("Descriptive history and the course models behind this shopping demo.")
    summary = service.insights(customer)
    columns = st.columns(3)
    columns[0].metric("Observed placed / demo orders", summary["orders"])
    columns[1].metric("Merchandise value", f"R$ {summary['spend']:,.2f}")
    columns[2].metric("RFM segment", "Not available" if summary["segment"] is None else str(summary["segment"]))
    st.info("Segments describe observed behavior. The notebook's two historical groups separated single-order and multiple-order histories; they do not prove future loyalty.")
    categories = service.category_summary(customer)
    if not categories.empty:
        st.subheader("Purchased categories")
        st.bar_chart(categories.head(8), color="#53796A")
    st.subheader("Experimental repeat-purchase score")
    if summary["risk"] is None:
        st.write("No evaluated fixed-age historical snapshot is available for this shopper. We do not create an arbitrary-age forecast.")
    else:
        risk = summary["risk"]
        st.metric("Historical model score", f"{risk['score']:.4f}")
        st.caption(f"Snapshot {risk['snapshot']:%Y-%m-%d}, 30 days after first observed order; target is another placed order within the next 90 days.")
    st.warning("Test AP 0.0153 · ROC-AUC 0.4746. Repeat scores are experimental and are not used to decide discounts.")
    with st.expander("Recommendation evidence and evaluation"):
        st.write("Content uses category weight 2 and historical price-band weight 1. Shared-buyer shelves require at least two historical buyers of both products. Buy again is a history shortcut, and interests/cart personalization are separately labeled application extensions.")
        st.write("Notebook content test Recall@5: 0.0567; NDCG@5: 0.0348, across 97 eligible warm customers out of 6,121 future shoppers. Live demo actions do not alter those results.")
    with st.expander("Your recent demo activity"):
        events = store.events(customer)
        if events:
            st.dataframe(pd.DataFrame(events)[["type", "product", "at"]], hide_index=True, width="stretch")

elif page == "Assistant":
    st.title("Your shopping assistant")
    st.caption("Ask about suggestions, purchase history, segments or reward eligibility. Answers use this customer's current demo data.")
    chat_key = f"chat_{customer}"
    messages = st.session_state.setdefault(chat_key, [])
    examples = st.columns(3)
    for col, question in zip(examples, ["Recommend products", "What offer can I use?", "Why this suggestion?"]):
        if col.button(question):
            messages.extend([{"role": "user", "content": question}, {"role": "assistant", "content": service.reply(customer, question)}])
            st.rerun()
    for message in messages[-20:]:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    if prompt := st.chat_input("Ask about your shopping…"):
        messages.extend([{"role": "user", "content": prompt}, {"role": "assistant", "content": service.reply(customer, prompt)}])
        st.rerun()
