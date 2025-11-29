import random
from app.models.system import StarSystem
from app.extensions import db

STAR_TYPES = [
    "Red Dwarf", "Yellow Dwarf", "Blue Giant", "White Dwarf",
    "Red Giant", "Neutron Star", "Binary Stars", "Black Hole"
]

def generate_star_systems_for_galaxy(galaxy, n=10):
    """Generate N systems inside a galaxy (if not already generated)."""

    if galaxy.systems and len(galaxy.systems) > 0:
        return galaxy.systems  # Already exists

    systems = []
    for i in range(n):
        s = StarSystem(
            galaxy_id=galaxy.id,
            name=f"System {galaxy.id}-{i+1}",
            star_type=random.choice(STAR_TYPES),
            position_x=random.randint(-2000, 2000),
            position_y=random.randint(-2000, 2000)
        )
        db.session.add(s)
        systems.append(s)

    db.session.commit()
    return systems
