# app/services/lifeform_generator.py
import json
import os
import random
import hashlib
from datetime import datetime

from app.extensions import db
try:
    from app.models import LifeForm
except Exception:
    LifeForm = None

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "config", "universe.json")
if not os.path.exists(CONFIG_PATH):
    CONFIG_PATH = os.path.join(os.getcwd(), "config", "universe.json")

def _short_hash(s: str) -> str:
    return hashlib.md5(s.encode()).hexdigest()[:10]

class SyntheticLifeGenerator:
    def __init__(self, rng: random.Random = None):
        self.rng = rng or random.Random()
        self.domains = ["eukarya", "bacteria", "archaea", "synthetica", "exobiota"]
        self.abilities = ["bioluminescence", "regeneration", "telepathy", "phase_shifting", "camouflage"]

    def generate(self, biome_type: str = "generic"):
        prefix = biome_type.title().split("_")[0]
        name = f"{prefix}_life_{_short_hash(str(self.rng.random()))}"
        domain = self.rng.choice(self.domains)
        trophic = self.rng.choice(["autotroph","herbivore","carnivore","omnivore","detritivore"])
        meta = {"biome_type": biome_type, "generated_at": datetime.utcnow().isoformat()}
        special = self.rng.sample(self.abilities, self.rng.randint(0,2))
        return {
            "id": f"life_{_short_hash(name+str(self.rng.random()))}",
            "name": name,
            "domain": domain,
            "trophic": trophic,
            "meta": meta,
            "special_abilities": special
        }

def generate_and_persist_lifeform(biome_type: str = "generic", rng: random.Random = None):
    rng = rng or random.Random()
    gen = SyntheticLifeGenerator(rng=rng)
    l = gen.generate(biome_type=biome_type)

    if LifeForm is None:
        return l

    existing = LifeForm.query.filter_by(name=l["name"]).first()
    if existing:
        return existing

    obj = LifeForm(id=l["id"], name=l["name"], domain=l["domain"], meta=l["meta"])
    db.session.add(obj)
    try:
        db.session.commit()
        return obj
    except Exception:
        db.session.rollback()
        return l
