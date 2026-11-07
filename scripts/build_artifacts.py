"""Usage: python scripts/build_artifacts.py (from the repository root)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from olist_shop.artifacts import ARTIFACT, build_artifacts

if __name__ == "__main__":
    bundle = build_artifacts()
    print(f"Saved {len(bundle['engine'].catalog):,} products to {ARTIFACT}")
    print("Source hashes verified. Startup loads artifacts without retraining.")
