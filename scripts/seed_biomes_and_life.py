# run with: python -m scripts.seed_biomes_and_life
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app import create_app
from app.extensions import db
from app.services.biome_generator import generate_and_persist_biome
from app.services.lifeform_generator import generate_and_persist_lifeform

app = create_app()
app.app_context().push()

# Example: generate 50 biomes and 200 lifeforms
print("Generating biomes...")
for i in range(50):
    generate_and_persist_biome(seed=None, commit=True)
print("Generating lifeforms (linked to random biome types)...")
for i in range(200):
    generate_and_persist_lifeform(biome_type="generic", seed=None, commit=True)
print("Done.")
