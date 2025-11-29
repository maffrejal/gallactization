from app import create_app
from app.extensions import db
from app.models import Biome
from biome_generator import SyntheticBiomeGenerator

app = create_app()
gen = SyntheticBiomeGenerator()

with app.app_context():
    for _ in range(100):
        b = gen.generate_synthetic_biome()
        db.session.add(Biome(
            id=b.id,
            name=b.name,
            base_type=b.base_type,
            rarity=b.rarity,
            biodiversity=b.biodiversity,
            productivity=b.productivity,
            climate=b.climate.__dict__,
            soil=b.soil.__dict__,
            vegetation=b.vegetation.__dict__,
            fauna=b.fauna.__dict__,
            special_features=b.special_features
        ))
    db.session.commit()
    print("Seeded 100 biomes")
