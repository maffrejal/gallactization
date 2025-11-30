import random
from datetime import datetime
from app.extensions import db

# Correct imports (FIXED)
from app.models.galaxy import Galaxy
from app.models.system import StarSystem
from app.models.planet import Planet
from app.models.job_queue import JobQueue   # if separate


# -------------------------------------------------------
# Universe Constants (configurable later via settings file)
# -------------------------------------------------------
DEFAULT_GALAXY_COUNT = 5
SYSTEMS_PER_GALAXY = (5, 10)       # min, max
PLANETS_PER_SYSTEM = (3, 8)        # min, max


def generate_universe(user_id, job: JobQueue = None):
    """
    Generate a small universe instance. Called by the worker.
    Writes galaxies → star systems → planets.
    Updates job.progress as it goes.
    """

    # --- Safety check --------------------------------------------------------
    if not Galaxy or not StarSystem or not Planet:
        raise RuntimeError(
            "Required models (Galaxy, StarSystem, Planet) not importable. "
            "Check app.models.* files and __init__.py."
        )

    print(f"🌌 Starting universe generation for user {user_id}")

    # ---------------------------------------------------------
    # Step 1 — Create galaxies
    # ---------------------------------------------------------
    num_galaxies = DEFAULT_GALAXY_COUNT
    galaxies = []

    for g in range(num_galaxies):
        gal = Galaxy(
            name=f"Galaxy {g + 1}",
            seed=random.randint(1, 999999999),
            num_stars=random.randint(50_000_000_000, 500_000_000_000),
            type=random.choice(["spiral", "elliptical", "irregular"]),
            meta={"created_for_user": user_id}
        )
        db.session.add(gal)
        galaxies.append(gal)

    db.session.commit()

    if job:
        job.progress = 0.3
        job.meta = {"message": f"Created {num_galaxies} galaxies"}
        db.session.commit()

    # ---------------------------------------------------------
    # Step 2 — Create star systems for each galaxy
    # ---------------------------------------------------------
    systems = []
    for gal in galaxies:
        system_count = random.randint(*SYSTEMS_PER_GALAXY)
        for s in range(system_count):
            sys = StarSystem(
                galaxy_id=gal.id,
                name=f"{gal.name} / System {s+1}",
                star_type=random.choice(["G-type", "K-type", "M-type", "Binary", "Giant"]),
                meta={"temperature": random.randint(2500, 7000)}
            )
            db.session.add(sys)
            systems.append(sys)

    db.session.commit()

    if job:
        job.progress = 0.55
        job.meta = {"message": f"Created {len(systems)} star systems"}
        db.session.commit()

    # ---------------------------------------------------------
    # Step 3 — Create planets for each star system
    # ---------------------------------------------------------
    planets = []
    for sys in systems:
        planet_count = random.randint(*PLANETS_PER_SYSTEM)
        for p in range(planet_count):
            planet = Planet(
                system_id=sys.id,
                name=f"{sys.name} - Planet {p+1}",
                size=random.randint(1, 10),
                position=p + 1,
                meta={"habitable": random.choice([True, False, False])},
            )
            db.session.add(planet)
            planets.append(planet)

    db.session.commit()

    if job:
        job.progress = 0.9
        job.meta = {"message": f"Created {len(planets)} planets"}
        db.session.commit()

    # ---------------------------------------------------------
    # Step 4 — Finalize
    # ---------------------------------------------------------
    if job:
        job.progress = 1.0
        job.status = "completed"
        job.meta = {"message": "Universe generation completed"}
        db.session.commit()

    print("✨ Universe generation complete!")
    return True
