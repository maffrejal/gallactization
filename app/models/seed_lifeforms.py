from app import create_app
from app.extensions import db
from app.models import Biome, Lifeform
from lifeform_generator import SyntheticLifeGenerator

app = create_app()
gen = SyntheticLifeGenerator()

with app.app_context():
    for b in Biome.query.all():
        count = int(2 + b.biodiversity * 8)
        for _ in range(count):
            lf = gen.generate_synthetic_life_form(b.base_type)
            db.session.add(Lifeform(
                id=lf.life_id,
                biome_id=b.id,
                name=lf.name,
                domain=lf.domain.value,
                trophic_level=lf.trophic_level.value,
                reproduction_type=lf.reproduction_type.value,
                lifespan_years=lf.lifespan_years,
                adult_size_kg=lf.adult_size_kg,
                complexity=lf.complexity,
                anatomy=lf.anatomy.__dict__,
                physiology=lf.physiology.__dict__,
                genetics=lf.genetics.__dict__,
                ecology=lf.ecology.__dict__,
                special_abilities=lf.special_abilities
            ))
    db.session.commit()
    print("Seeded lifeforms for all biomes")
