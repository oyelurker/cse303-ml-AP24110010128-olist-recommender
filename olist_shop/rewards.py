"""Illustrative reward policy. It does not optimize or predict discount response."""
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass(frozen=True)
class OfferRule:
    kind: str
    title: str
    basis_points: int
    minimum_cents: int
    cap_cents: int
    cooldown_days: int | None


RULES = {
    "welcome": OfferRule("welcome", "Your first order", 500, 10000, 2000, None),
    "winback": OfferRule("winback", "Welcome back", 800, 15000, 3000, 60),
    "loyalty": OfferRule("loyalty", "Thanks for shopping with us", 700, 15000, 2500, 30),
}


def eligible_rule(purchase_times, now: datetime):
    times = [time for time in purchase_times if time <= now]
    if not times:
        return RULES["welcome"], "No completed orders yet."
    if now - max(times) > timedelta(days=60):
        return RULES["winback"], "Your last completed purchase was more than 60 days ago."
    recent = [time for time in times if time >= now-timedelta(days=90)]
    if len(recent) >= 3 and len({time.date() for time in recent}) >= 2:
        return RULES["loyalty"], "At least three completed orders in 90 days, across two or more dates."
    return None, "Keep exploring. No automatic reward applies to this order history."


def discount_cents(rule, subtotal):
    if rule is None or subtotal < rule.minimum_cents:
        return 0
    return min(rule.cap_cents, (subtotal * rule.basis_points + 5000) // 10000)
