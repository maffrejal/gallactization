from app.extensions import db
from sqlalchemy.dialects.postgresql import JSONB

class Lifeform(db.Model):
    __tablename__ = 'lifeforms'
    id = db.Column(db.String(64), primary_key=True)
    biome_id = db.Column(db.String(64), db.ForeignKey('biomes.id', ondelete='CASCADE'), nullable=False, index=True)
    name = db.Column(db.String(200), nullable=False, index=True)
    domain = db.Column(db.String(50))
    trophic_level = db.Column(db.String(50))
    reproduction_type = db.Column(db.String(50))
    lifespan_years = db.Column(db.Float)
    adult_size_kg = db.Column(db.Float)
    complexity = db.Column(db.String(50))

    anatomy = db.Column(JSONB, nullable=False, default=dict)
    physiology = db.Column(JSONB, nullable=False, default=dict)
    genetics = db.Column(JSONB, nullable=False, default=dict)
    ecology = db.Column(JSONB, nullable=False, default=dict)
    special_abilities = db.Column(JSONB, nullable=False, default=list)
    
    biome = db.relationship("Biome", back_populates="lifeforms")

    def to_dict(self):
        return {
            'id': self.id,
            'biome_id': self.biome_id,
            'name': self.name,
            'domain': self.domain,
            'trophic_level': self.trophic_level,
            'reproduction_type': self.reproduction_type,
            'lifespan_years': self.lifespan_years,
            'adult_size_kg': self.adult_size_kg,
            'complexity': self.complexity,
            'anatomy': self.anatomy,
            'physiology': self.physiology,
            'genetics': self.genetics,
            'ecology': self.ecology,
            'special_abilities': self.special_abilities
        }
