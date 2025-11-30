# app/services/biome_generator.py
import json
import os
import random
import hashlib
from datetime import datetime

from app.extensions import db
try:
    from app.models import Biome
except Exception:
    # If your model is named differently, adjust here
    Biome = None

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "config", "universe.json")
if not os.path.exists(CONFIG_PATH):
    # allow relative path fallback
    CONFIG_PATH = os.path.join(os.getcwd(), "config", "universe.json")

def _load_config():
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def _short_hash(s: str) -> str:
    return hashlib.md5(s.encode()).hexdigest()[:10]

class SyntheticBiomeGenerator:
    """Lightweight biome generator that returns a dict describing a biome."""
    def __init__(self, rng: random.Random = None):
        self.rng = rng or random.Random()

        self.base_types = [
            "forest", "grassland", "wetland", "desert", "alpine", "marine",
            "volcanic", "cavernous", "crystalline", "fungal", "luminous", "floating"
        ]
        self.features = [
            "bioluminescent_flora", "crystalline_outcrops", "gravity_anomalies",
            "time_dilation_pockets", "magnetic_storms", "floating_islands",
            "prismatic_fogs", "echoing_valleys"
        ]

    def generate(self, name_seed: str = None):
        base_type = self.rng.choice(self.base_types)
        name_seed = name_seed or str(self.rng.random())
        name = f"{base_type.title()}-{_short_hash(name_seed)}"
        special = self.rng.sample(self.features, self.rng.randint(0,2))
        climate = {
            "temperature": [round(self.rng.uniform(-40,60),1), round(self.rng.uniform(-40,60),1)],
            "precipitation_mm": [round(self.rng.uniform(0,1000),1), round(self.rng.uniform(0,8000),1)],
            "humidity": round(self.rng.uniform(0.0,1.0),2)
        }
        meta = {"special_features": special, "generated_at": datetime.utcnow().isoformat()}
        return {
            "id": f"biome_{_short_hash(name+str(self.rng.random()))}",
            "name": name,
            "base_type": base_type,
            "meta": meta,
            "climate": climate
        }

def generate_and_persist_biome(name_seed: str = None, rng: random.Random = None):
    """Generates a biome and persists it to DB (if Biome model exists). Returns Biome instance or a dict."""
    cfg = _load_config()
    rng = rng or random.Random()
    gen = SyntheticBiomeGenerator(rng=rng)
    b = gen.generate(name_seed=name_seed)

    # Try to persist using app.models.Biome
    if Biome is None:
        return b

    # reuse if exists by name
    existing = Biome.query.filter_by(name=b["name"]).first()
    if existing:
        return existing

    obj = Biome(id=b["id"], name=b["name"], base_type=b["base_type"], meta=b["meta"])
    db.session.add(obj)
    try:
        db.session.commit()
        return obj
    except Exception:
        db.session.rollback()
        # fallback return dict
        return b
