# Biome / Lifeform models package initializer
from app.extensions import db

from .user import User
from .universe import Universe
from .galaxy import Galaxy
from .system import StarSystem
from .planet import Planet
from .planet_biome import PlanetBiome
from .biome import Biome
from .lifeform import Lifeform
from .save_game import SaveGame
from .job_queue import JobQueue

__all__ = [
    "User",
    "Universe",
    "Galaxy",
    "StarSystem",   # <-- correct
    "Planet",
    "Biome",
    "Lifeform",
    "PlanetBiome",
    "SaveGame",
    "JobQueue"
]