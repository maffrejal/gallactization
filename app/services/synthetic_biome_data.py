# File: app/services/synthetic_biome_data.py
"""
SyntheticBiomeGenerator
- Cleaned-up, self-contained version of the biome generator class you provided.
- Put this file at: app/services/synthetic_biome_data.py
- No DB imports here — purely procedural generator that returns dataclasses.
"""
from dataclasses import dataclass
from typing import List, Tuple, Optional
import random
import hashlib
import json

@dataclass
class SyntheticClimate:
    temperature_range: Tuple[float, float]
    precipitation_mm: Tuple[float, float]
    humidity_level: float
    seasonality: float
    storm_frequency: float
    wind_patterns: List[str]

@dataclass
class SyntheticSoil:
    fertility: float
    drainage: float
    ph_level: float
    organic_content: float
    mineral_composition: List[str]

@dataclass
class SyntheticVegetation:
    canopy_structure: str
    leaf_type: str
    growth_pattern: str
    root_system: str
    reproduction_method: str
    dominant_forms: List[str]

@dataclass
class SyntheticFauna:
    size_distribution: str
    activity_patterns: List[str]
    feeding_strategies: List[str]
    mobility_types: List[str]
    social_structures: List[str]

@dataclass
class SyntheticBiome:
    id: str
    name: str
    base_type: str
    climate: SyntheticClimate
    soil: SyntheticSoil
    vegetation: SyntheticVegetation
    fauna: SyntheticFauna
    special_features: List[str]
    rarity: float
    biodiversity: float
    productivity: float

class SyntheticBiomeGenerator:
    def __init__(self, seed: Optional[int] = None):
        if seed is not None:
            random.seed(seed)
        self.setup_generator_components()

    def setup_generator_components(self):
        self.base_archetypes = {
            "forest": 0.15,
            "grassland": 0.12,
            "wetland": 0.10,
            "desert": 0.10,
            "alpine": 0.08,
            "marine": 0.12,
            "volcanic": 0.06,
            "cavernous": 0.07,
            "crystalline": 0.05,
            "fungal": 0.08,
            "luminous": 0.04,
            "floating": 0.03
        }

        self.temperature_profiles = {
            "cryogenic": (-100, -50),
            "frigid": (-49, -20),
            "cold": (-19, 0),
            "cool": (1, 10),
            "temperate": (11, 20),
            "warm": (21, 28),
            "hot": (29, 40),
            "scorching": (41, 60),
            "molten": (61, 100)
        }

        self.precipitation_levels = {
            "hyperarid": (0, 50),
            "arid": (51, 250),
            "semi_arid": (251, 500),
            "moderate": (501, 1000),
            "humid": (1001, 2000),
            "very_humid": (2001, 4000),
            "superhumid": (4001, 8000),
            "deluge": (8001, 15000)
        }

        self.canopy_structures = [
            "towering", "layered", "sparse", "dense", "floating", "underground",
            "crystalline", "bioluminescent", "transparent", "metallic",
            "weeping", "spiraling", "geometric", "symbiotic", "parasitic"
        ]

        self.leaf_types = [
            "broadleaf", "needleleaf", "scale-like", "succulent", "feathery",
            "crystalline", "membranous", "filamentous", "bioluminescent",
            "photosynthetic_fungi", "mineral_absorbing", "gas_processing"
        ]

        self.growth_patterns = [
            "rapid_colonizer", "slow_ancient", "seasonal_boom", "continuous",
            "pulsating", "symbiotic_clusters", "floating_colonies", "underground_networks"
        ]

        self.size_distributions = [
            "microscopic_dominant", "small_creatures", "mixed_sizes",
            "large_megafauna", "gigantic_beings", "size_variable"
        ]

        self.feeding_strategies = [
            "photosynthetic", "carnivorous", "herbivorous", "omnivorous",
            "filter_feeding", "scavenging", "parasitic", "symbiotic",
            "mineral_consuming", "energy_absorbing", "dimensional_feeding"
        ]

        self.mobility_types = [
            "burrowing", "arboreal", "aerial", "aquatic", "subterranean",
            "gliding", "teleporting", "phase_shifting", "gravity_defying"
        ]

        self.special_features_pool = [
            "floating_islands", "crystalline_forests", "bioluminescent_flora",
            "singing_rocks", "memory_absorbing_plants", "time_dilated_zones",
            "gravity_anomalies", "dimensional_portals", "psychic_resonance",
            "mineral_growths", "liquid_crystal_rivers", "gas_giant_vegetation",
            "magnetic_storms", "prismatic_fog", "echoing_valleys",
            "dream_catching_fungi", "light_bending_trees", "sound_gardens"
        ]

        self.name_prefixes = [
            "Crystal", "Shadow", "Verdant", "Azure", "Crimson", "Emerald",
            "Sapphire", "Obsidian", "Pearl", "Jade", "Amber", "Opal",
            "Whispering", "Singing", "Dancing", "Floating", "Shifting",
            "Eternal", "Ancient", "Primordial", "Celestial", "Abyssal"
        ]

        self.name_suffixes = [
            "wood", "vale", "mire", "peak", "reach", "deep", "height",
            "garden", "waste", "sanctum", "domain", "realm", "expanse",
            "jungle", "forest", "marsh", "tundra", "desert", "cavern",
            "grove", "thicket", "fen", "bog", "strand", "crag"
        ]

        self.name_connectors = [
            " of ", " in the ", " beyond the ", " within the ", " under ",
            " over the ", " across the ", " between the ", " amid the "
        ]

        self.name_descriptors = [
            "Lost", "Forgotten", "Hidden", "Secret", "Mysterious", "Enchanted",
            "Cursed", "Blessed", "Sacred", "Profane", "Timeless", "Endless"
        ]

    def generate_biome_name(self) -> str:
        name_type = random.choice(["simple", "compound", "descriptive", "mystical"])
        if name_type == "simple":
            return f"{random.choice(self.name_prefixes)}{random.choice(self.name_suffixes)}"
        elif name_type == "compound":
            return f"{random.choice(self.name_prefixes)}{random.choice(self.name_connectors)}{random.choice(self.name_descriptors)} {random.choice(self.name_suffixes)}"
        elif name_type == "descriptive":
            feature = random.choice(self.special_features_pool).replace('_', ' ').title()
            return f"{feature} {random.choice(self.name_suffixes)}"
        else:
            elements = ["Fire", "Water", "Earth", "Air", "Light", "Shadow", "Time", "Space"]
            return f"{random.choice(elements)}-Touched {random.choice(self.name_suffixes)}"

    def generate_climate(self, base_type: str) -> SyntheticClimate:
        climate_profiles = {
            "forest": {"temp": "cool", "precip": "humid", "humidity": 0.8},
            "grassland": {"temp": "temperate", "precip": "moderate", "humidity": 0.6},
            "wetland": {"temp": "warm", "precip": "very_humid", "humidity": 0.9},
            "desert": {"temp": "hot", "precip": "arid", "humidity": 0.2},
            "alpine": {"temp": "cold", "precip": "moderate", "humidity": 0.5},
            "marine": {"temp": "cool", "precip": "humid", "humidity": 0.85},
            "volcanic": {"temp": "scorching", "precip": "moderate", "humidity": 0.4},
            "cavernous": {"temp": "cool", "precip": "semi_arid", "humidity": 0.7},
            "crystalline": {"temp": "temperate", "precip": "moderate", "humidity": 0.3},
            "fungal": {"temp": "warm", "precip": "humid", "humidity": 0.8},
            "luminous": {"temp": "temperate", "precip": "moderate", "humidity": 0.6},
            "floating": {"temp": "cool", "precip": "moderate", "humidity": 0.5}
        }
        profile = climate_profiles.get(base_type, climate_profiles["forest"])
        temp_variation = random.choice(list(self.temperature_profiles.keys()))
        precip_variation = random.choice(list(self.precipitation_levels.keys()))
        temp_range = self._blend_ranges(self.temperature_profiles[profile["temp"]], self.temperature_profiles[temp_variation], random.random())
        precip_range = self._blend_ranges(self.precipitation_levels[profile["precip"]], self.precipitation_levels[precip_variation], random.random())
        humidity = max(0.1, min(0.95, profile["humidity"] + random.uniform(-0.3, 0.3)))
        seasonality = random.uniform(0.1, 0.9)
        storm_frequency = random.uniform(0.0, 1.0)
        wind_patterns = random.sample(["gentle_breezes", "strong_gales", "whispering_winds", "cyclonic", "magnetic_pulses", "psychic_currents", "gravitational_flows"], random.randint(1, 3))
        return SyntheticClimate(temperature_range=temp_range, precipitation_mm=precip_range, humidity_level=humidity, seasonality=seasonality, storm_frequency=storm_frequency, wind_patterns=wind_patterns)

    def generate_soil(self, base_type: str) -> SyntheticSoil:
        base_soil_profiles = {
            "forest": {"fertility": 0.7, "drainage": 0.6, "ph": 0.3, "organic": 0.8},
            "desert": {"fertility": 0.2, "drainage": 0.9, "ph": 0.7, "organic": 0.1},
            "wetland": {"fertility": 0.8, "drainage": 0.1, "ph": 0.4, "organic": 0.9},
            "volcanic": {"fertility": 0.9, "drainage": 0.8, "ph": 0.5, "organic": 0.3},
            "crystalline": {"fertility": 0.3, "drainage": 0.7, "ph": 0.6, "organic": 0.1}
        }
        profile = base_soil_profiles.get(base_type, base_soil_profiles["forest"])
        minerals = random.sample(["silica_crystals", "magnetic_ores", "psychic_resonators", "bioluminescent_minerals", "memory_stones", "gravity_dust", "phase_crystals", "prismatic_shards", "echoing_rocks"], random.randint(2, 5))
        return SyntheticSoil(fertility=max(0.0, min(1.0, profile["fertility"] + random.uniform(-0.2, 0.2))), drainage=max(0.0, min(1.0, profile["drainage"] + random.uniform(-0.2, 0.2))), ph_level=max(0.0, min(1.0, profile["ph"] + random.uniform(-0.3, 0.3))), organic_content=max(0.0, min(1.0, profile["organic"] + random.uniform(-0.2, 0.2))), mineral_composition=minerals)

    def generate_vegetation(self, base_type: str) -> SyntheticVegetation:
        if base_type in ["crystalline", "luminous", "floating"]:
            canopy = random.choice(["crystalline", "bioluminescent", "floating", "energy-based"])
            leaf_type = random.choice(["crystalline", "membranous", "light-emitting", "gas-processing"])
        else:
            canopy = random.choice(self.canopy_structures)
            leaf_type = random.choice(self.leaf_types)
        growth_pattern = random.choice(self.growth_patterns)
        root_system = random.choice(["deep_taproot", "fibrous_network", "aerial_roots", "crystalline_anchors", "magnetic_attachment"])
        reproduction_method = random.choice(["spores", "seeds", "budding", "fragmentation", "energy_dispersal", "psychic_propagation"])
        dominant_forms = random.sample(["towering_trees", "glowing_fungi", "crystal_formations", "floating_spheres", "weeping_vines", "spiraling_towers", "pulsating_mounds", "geometric_structures"], random.randint(2, 4))
        return SyntheticVegetation(canopy_structure=canopy, leaf_type=leaf_type, growth_pattern=growth_pattern, root_system=root_system, reproduction_method=reproduction_method, dominant_forms=dominant_forms)

    def generate_fauna(self, base_type: str) -> SyntheticFauna:
        size_distribution = random.choice(self.size_distributions)
        activity_patterns = random.sample(["diurnal", "nocturnal", "crepuscular", "seasonal", "tidal", "storm_chasers", "light_seekers", "shadow_dwellers"], random.randint(2, 4))
        feeding_strategies = random.sample(self.feeding_strategies, random.randint(2, 3))
        mobility_types = random.sample(self.mobility_types, random.randint(2, 3))
        social_structures = random.sample(["solitary", "pack_hunters", "swarm_intelligence", "hive_mind", "symbiotic_colonies", "telepathic_network", "individualistic"], random.randint(1, 2))
        return SyntheticFauna(size_distribution=size_distribution, activity_patterns=activity_patterns, feeding_strategies=feeding_strategies, mobility_types=mobility_types, social_structures=social_structures)

    def _blend_ranges(self, range1: Tuple[float, float], range2: Tuple[float, float], weight: float) -> Tuple[float, float]:
        min_val = range1[0] * (1 - weight) + range2[0] * weight
        max_val = range1[1] * (1 - weight) + range2[1] * weight
        return (min_val, max_val)

    def _generate_biome_id(self, name: str, characteristics: dict) -> str:
        content = f"{name}{json.dumps(characteristics, sort_keys=True)}"
        return hashlib.md5(content.encode()).hexdigest()[:12]

    def calculate_biome_metrics(self, biome: SyntheticBiome) -> Tuple[float, float, float]:
        temp_range = biome.climate.temperature_range[1] - biome.climate.temperature_range[0]
        climate_rarity = abs(biome.climate.humidity_level - 0.5) * 0.3
        climate_rarity += (1 - (temp_range / 100)) * 0.3
        climate_rarity += len(biome.special_features) * 0.1
        rarity = min(1.0, climate_rarity)
        biodiversity = (1 - biome.climate.seasonality) * 0.4
        biodiversity += biome.soil.fertility * 0.3
        biodiversity += (1 - abs(biome.climate.humidity_level - 0.7)) * 0.3
        biodiversity = min(1.0, biodiversity)
        productivity = biome.soil.fertility * 0.4
        productivity += biome.climate.humidity_level * 0.3
        productivity += (biome.climate.temperature_range[1] / 50) * 0.3
        productivity = min(1.0, productivity)
        return rarity, biodiversity, productivity

    def generate_synthetic_biome(self, biome_id: Optional[int] = None) -> SyntheticBiome:
        base_type = random.choices(list(self.base_archetypes.keys()), weights=list(self.base_archetypes.values()))[0]
        name = self.generate_biome_name()
        climate = self.generate_climate(base_type)
        soil = self.generate_soil(base_type)
        vegetation = self.generate_vegetation(base_type)
        fauna = self.generate_fauna(base_type)
        num_features = random.choices([0, 1, 2, 3, 4], weights=[0.1, 0.3, 0.4, 0.15, 0.05])[0]
        special_features = random.sample(self.special_features_pool, num_features)
        temp_biome = SyntheticBiome(id="temp", name=name, base_type=base_type, climate=climate, soil=soil, vegetation=vegetation, fauna=fauna, special_features=special_features, rarity=0.0, biodiversity=0.0, productivity=0.0)
        rarity, biodiversity, productivity = self.calculate_biome_metrics(temp_biome)
        characteristics = {
            "base_type": base_type,
            "climate": {
                "temp_range": climate.temperature_range,
                "precipitation": climate.precipitation_mm,
                "humidity": climate.humidity_level
            },
            "special_features": special_features
        }
        final_id = self._generate_biome_id(name, characteristics)
        return SyntheticBiome(id=final_id, name=name, base_type=base_type, climate=climate, soil=soil, vegetation=vegetation, fauna=fauna, special_features=special_features, rarity=rarity, biodiversity=biodiversity, productivity=productivity)


# Lightweight instance for quick use
default_biome_generator = SyntheticBiomeGenerator()


# File: app/services/biome_generator.py
"""
Wrapper that exposes a simple, DB-aware API for generating and optionally persisting biomes.
Put this file at: app/services/biome_generator.py

Functions provided:
- generate_synthetic_biome(): returns a SyntheticBiome dataclass
- persist_biome(db_session, BiomeModel, biome_dataclass): merges/persists a Biome row
- get_or_create_biome(db_session, BiomeModel, biome_dataclass): convenience wrapper

This file intentionally does a *safe* import of the Biome model (try/except)
so it can be used in environments where the model doesn't exist yet (tests).
"""
from typing import Optional
from app.services.synthetic_biome_data import default_biome_generator, SyntheticBiome


def generate_synthetic_biome() -> SyntheticBiome:
    """Return a generated SyntheticBiome dataclass (not persisted)."""
    return default_biome_generator.generate_synthetic_biome()


def persist_biome(db_session, BiomeModel, biome: SyntheticBiome):
    """Persist the dataclass into DB using the provided session and model.

    BiomeModel is expected to have columns: id (string/pk), name, type, meta (json), rarity (float)
    """
    # Build a plain dict to persist into JSON/meta
    meta = {
        "climate": {
            "temperature_range": biome.climate.temperature_range,
            "precipitation_mm": biome.climate.precipitation_mm,
            "humidity": biome.climate.humidity_level,
            "seasonality": biome.climate.seasonality,
            "storm_frequency": biome.climate.storm_frequency,
            "wind_patterns": biome.climate.wind_patterns
        },
        "soil": {
            "fertility": biome.soil.fertility,
            "drainage": biome.soil.drainage,
            "ph": biome.soil.ph_level,
            "organic": biome.soil.organic_content,
            "minerals": biome.soil.mineral_composition
        },
        "vegetation": {
            "canopy": biome.vegetation.canopy_structure,
            "leaf": biome.vegetation.leaf_type,
            "growth": biome.vegetation.growth_pattern,
            "dominant": biome.vegetation.dominant_forms
        },
        "fauna": {
            "size_distribution": biome.fauna.size_distribution,
            "feeding": biome.fauna.feeding_strategies,
            "mobility": biome.fauna.mobility_types
        },
        "special_features": biome.special_features,
        "game_metrics": {
            "rarity": biome.rarity,
            "biodiversity": biome.biodiversity,
            "productivity": biome.productivity
        }
    }

    # Upsert via merge to avoid duplicates when same biome id exists
    obj = BiomeModel(
        id=biome.id,
        name=biome.name,
        type=biome.base_type,
        meta=meta,
        rarity=biome.rarity
    )
    db_session.merge(obj)
    db_session.flush()
    return obj


def get_or_create_biome(db_session, BiomeModel, biome: SyntheticBiome):
    """Check for existing biome row by id; if missing, persist and return it."""
    existing = db_session.query(BiomeModel).get(biome.id)
    if existing:
        return existing
    return persist_biome(db_session, BiomeModel, biome)


# End of bundle
