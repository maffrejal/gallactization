from app.extensions import db
from app.models.universe import Universe
from app.models.galaxy import Galaxy
from datetime import datetime
import random

def generate_universe(user_id, job=None):
    # 1) Create Universe first
    universe = Universe(
        user_id=user_id,
        name=f"Universe {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}",
        seed=random.randint(1, 999999999)
    )
    db.session.add(universe)
    db.session.commit()  # <— we MUST commit so universe.id exists

    # (optional) update job status
    if job:
        job.message = "Universe created. Generating galaxies..."
        job.progress = 5
        db.session.commit()

    # 2) Generate galaxies
    galaxy_count = 5  # later configurable

    for i in range(1, galaxy_count + 1):
        g = Galaxy(
            universe_id=universe.id,    # <— THE MISSING PIECE
            name=f"Galaxy {i}",
            seed=random.randint(1, 999999999),
            num_stars=random.randint(10_000, 200_000),  # safe number range
            type=random.choice(["spiral", "elliptical", "irregular"]),
            meta={"origin": "auto"}
        )
        db.session.add(g)

        # optional job progress
        if job:
            job.progress = int(5 + (i / galaxy_count) * 90)
            job.message = f"Generating galaxy {i} of {galaxy_count}..."
            db.session.commit()

    db.session.commit()

    # final update
    if job:
        job.progress = 100
        job.status = "done"
        job.message = "Universe generation complete"
        db.session.commit()

    return universe.id
