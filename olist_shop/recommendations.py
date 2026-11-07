"""Frozen content geometry, plus clearly separated application shelves."""
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP

import numpy as np
import pandas as pd
from scipy import sparse
from sklearn.preprocessing import OneHotEncoder, normalize


def to_cents(value):
    return int((Decimal(str(value)) * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def money(cents):
    return f"R$ {cents / 100:,.2f}"


@dataclass
class RecommendationEngine:
    users: pd.Index
    catalog: pd.DataFrame
    history: sparse.csr_matrix
    vectors: sparse.csr_matrix
    popularity: np.ndarray
    shared_buyers: sparse.csr_matrix
    cutoff: pd.Timestamp

    @classmethod
    def fit(cls, items, products, cutoff):
        historical = items.loc[items.order_purchase_timestamp.lt(pd.Timestamp(cutoff))]
        pairs = historical[["customer_unique_id", "product_id"]].drop_duplicates()
        users = pd.Index(sorted(pairs.customer_unique_id.unique()))
        ids = pd.Index(sorted(pairs.product_id.unique()))
        matrix = sparse.csr_matrix((np.ones(len(pairs)), (users.get_indexer(pairs.customer_unique_id), ids.get_indexer(pairs.product_id))), shape=(len(users), len(ids)))
        catalog = products.set_index("product_id").reindex(ids)[["category_label"]].copy()
        catalog["historical_price"] = historical.groupby("product_id").price.median().reindex(ids)
        breaks = np.unique(catalog.historical_price.quantile([.25, .5, .75]).to_numpy())
        fields = pd.DataFrame(index=ids)
        fields["category_label"] = catalog.category_label.astype("string").fillna("unknown")
        fields["price_band"] = pd.cut(catalog.historical_price, [-np.inf, *breaks, np.inf], labels=[f"price_band_{j+1}" for j in range(len(breaks)+1)]).astype("string").fillna("unknown_price")
        encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=True)
        encoded = encoder.fit_transform(fields)
        weights = np.array([2. if x.startswith("category_label_") else 1. for x in encoder.get_feature_names_out()])
        vectors = normalize(encoded.multiply(weights).tocsr())
        popularity = pairs.groupby("product_id").size().reindex(ids).to_numpy(float)
        shared = (matrix.T @ matrix).tocsr()
        shared.setdiag(0); shared.eliminate_zeros()
        catalog["price_cents"] = catalog.historical_price.map(to_cents)
        catalog["category"] = catalog.category_label.str.replace("_", " ")
        catalog["label"] = [f"{category.title()} · {item[:6].upper()}" for item, category in zip(ids, catalog.category)]
        return cls(users, catalog, matrix, vectors, popularity, shared, pd.Timestamp(cutoff))

    def seen(self, user):
        index = self.users.get_indexer([user])[0]
        return set() if index < 0 else set(self.catalog.index[self.history.getrow(index).indices])

    def _rank(self, scores, exclude, n, reason, fallback=False):
        scores = np.asarray(scores, dtype=float).copy()
        positions = self.catalog.index.get_indexer(list(exclude))
        scores[positions[positions >= 0]] = -np.inf
        eligible = np.flatnonzero(np.isfinite(scores))
        order = np.lexsort((self.catalog.index.to_numpy(str)[eligible], -self.popularity[eligible], -scores[eligible]))
        selected = eligible[order[:n]]
        frame = self.catalog.iloc[selected].copy()
        frame.index.name = "product_id"
        frame["score"] = scores[selected]
        frame["reason"] = reason
        if fallback:
            frame.loc[frame.score.le(0), "reason"] = "Popular historical alternative"
        return frame.reset_index()

    def recommend(self, user, n=5, interests=(), purchased=(), cart=(), mode="personalized", extra_exclude=()):
        if mode not in {"personalized", "popular", "cart"}:
            raise ValueError("Unknown recommendation mode")
        if not isinstance(n, int) or isinstance(n, bool) or not 1 <= n <= 100:
            raise ValueError("n must be between 1 and 100")
        seen = self.seen(user) | set(purchased)
        exclude = seen | set(cart) | set(extra_exclude)
        profile_ids = set(cart) if mode == "cart" else seen | set(interests)
        positions = self.catalog.index.get_indexer(sorted(profile_ids))
        positions = positions[positions >= 0]
        if mode == "popular" or not len(positions):
            return self._rank(self.popularity, exclude, n, "Popular with historical shoppers")
        profile = normalize(sparse.csr_matrix(np.ones((1, len(positions)))) @ self.vectors[positions])
        score = (self.vectors @ profile.T).toarray().ravel()
        reason = "Related to items in your cart" if mode == "cart" else ("Based on purchases and saved interests" if interests else "Based on your purchase history")
        return self._rank(score, exclude, n, reason, fallback=True)

    def similar(self, product, n=4, exclude=()):
        index = self.catalog.index.get_indexer([product])[0]
        if index < 0:
            raise ValueError("Unknown product")
        scores = (self.vectors @ self.vectors.getrow(index).T).toarray().ravel()
        return self._rank(scores, set(exclude) | {product}, n, "Similar category and historical price band")

    def also_bought(self, product, n=4, exclude=(), min_buyers=2):
        index = self.catalog.index.get_indexer([product])[0]
        if index < 0:
            raise ValueError("Unknown product")
        counts = self.shared_buyers.getrow(index).toarray().ravel()
        scores = np.full(len(counts), -np.inf)
        mask = counts >= min_buyers
        scores[mask] = counts[mask] / np.sqrt(self.popularity[index] * self.popularity[mask])
        result = self._rank(scores, set(exclude) | {product}, n, "Shared historical buyers")
        result["shared_buyers"] = [int(counts[self.catalog.index.get_loc(item)]) for item in result.product_id]
        return result
