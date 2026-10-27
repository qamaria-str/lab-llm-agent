class LiquidHandler:
    """Simulateur très simple d'un robot de pipetage."""
## part1: robot state
    MAX_VOLUME_UL = 200
    MIN_VOLUME_UL = 1

    def __init__(self): #cette fonction s’exécute automatiquement quand on crée un robot. Elle fixe son état de départ.
        self.tip_attached = False #« ce robot n’a pas de pointe pour l’instant ».
        self.held_volume = 0.0 #volume de liquide actuellement dans la pointe
        self.wells = {"plate_1": {"A1": 1000.0}, "plate_2": {}}

## part2 : action on the tip
    def pick_up_tip(self): #prendre une pointe
        if self.tip_attached:
            raise ValueError("Une pointe est déjà fixée.")
        self.tip_attached = True
        return "Pointe fixée."

    def drop_tip(self): #jeter la pointe
        if not self.tip_attached:
            raise ValueError("Aucune pointe à jeter.")
        self.tip_attached = False
        self.held_volume = 0.0
        return "Pointe jetée."

## part3: aspirate & dispense 
    def aspirate(self, plate, well, volume_ul):
        if not (self.MIN_VOLUME_UL <= volume_ul <= self.MAX_VOLUME_UL):
            raise ValueError(f"Volume {volume_ul} µL hors limites (1 à 200 µL).")
        if not self.tip_attached:
            raise ValueError("Impossible d'aspirer sans pointe.")
        available = self.wells[plate].get(well, 0.0)
        if available < volume_ul:
            raise ValueError(f"Le puits {plate}/{well} ne contient que {available} µL.")
        self.wells[plate][well] = available - volume_ul
        self.held_volume += volume_ul
        return f"{volume_ul} µL aspirés depuis {plate}/{well}."

    def dispense(self, plate, well, volume_ul):
        if not self.tip_attached:
            raise ValueError("Impossible de dispenser sans pointe.")
        if volume_ul > self.held_volume:
            raise ValueError(f"La pointe ne contient que {self.held_volume} µL.")
        self.wells[plate][well] = self.wells[plate].get(well, 0.0) + volume_ul
        self.held_volume -= volume_ul
        return f"{volume_ul} µL dispensés dans {plate}/{well}."

