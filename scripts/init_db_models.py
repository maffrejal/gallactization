"""Init DB tables for Gallactization models ZIP 1
Usage:
    Set your DATABASE_URL or ensure create_app() in your project uses Postgres URI.
    Then run:
        python scripts/init_db_models.py
"""
import os
from app import create_app
from app.extensions import db
from app.models import Biome, Lifeform, PlanetBiome

def main():
    app = create_app()
    with app.app_context():
        print('Creating tables...')
        db.create_all()
        print('Tables created: biomes, lifeforms, planet_biomes')
if __name__ == '__main__':
    main()
