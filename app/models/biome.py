from app.extensions import db
from sqlalchemy.dialects.postgresql import JSONB

class Biome(db.Model):
    __tablename__ = 'biomes'
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(200), nullable=False, index=True)
    base_type = db.Column(db.String(100), nullable=False, index=True)
    rarity = db.Column(db.Float, nullable=False, default=0.0)
    biodiversity = db.Column(db.Float, nullable=False, default=0.0)
    productivity = db.Column(db.Float, nullable=False, default=0.0)

    climate = db.Column(JSONB, nullable=False, default=dict)
    soil = db.Column(JSONB, nullable=False, default=dict)
    vegetation = db.Column(JSONB, nullable=False, default=dict)
    fauna = db.Column(JSONB, nullable=False, default=dict)
    special_features = db.Column(JSONB, nullable=False, default=list)

    # relationship: one biome -> many lifeforms
    #lifeforms = db.relationship('Lifeform', backref='biome', cascade='all, delete-orphan', lazy='dynamic')
    planet_links = db.relationship("PlanetBiome", back_populates="biome", lazy=True)
    lifeforms = db.relationship("Lifeform", back_populates="biome", lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'base_type': self.base_type,
            'rarity': self.rarity,
            'biodiversity': self.biodiversity,
            'productivity': self.productivity,
            'climate': self.climate,
            'soil': self.soil,
            'vegetation': self.vegetation,
            'fauna': self.fauna,
            'special_features': self.special_features
        }
