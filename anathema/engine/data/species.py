
from .species_data import SpeciesData


class Species:
    HUMAN = SpeciesData(
        name = "Human",
        speed = 1,
        base_might = 10,
        base_finesse = 10,
        base_vitality = 10,
        base_piety = 10,
        base_cunning = 10,
        base_knowledge = 10,
    )
    WANDERER = SpeciesData(
        name = "Wanderer",
        speed = 1,
        base_might = 10,
        base_finesse = 10,
        base_vitality = 10,
        base_piety = 10,
        base_cunning = 10,
        base_knowledge = 10,
    )


def get_species_data(name: str):
    return getattr(Species, name.upper())
