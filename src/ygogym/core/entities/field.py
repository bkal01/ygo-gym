from typing import List, Dict, Optional, Any
from src.ygogym.core.entities.card import Card
from src.ygogym.core.constants import FIELD_SIZE, CardType, MonsterPosition, SpellTrapPosition, CardLocation

class Field:
    def __init__(self, owner=None):
        self.owner = owner
        self.monster_zones: List[Optional[Card]] = [None] * FIELD_SIZE
        self.spell_trap_zones: List[Optional[Card]] = [None] * FIELD_SIZE
        self.field_spell: Optional[Card] = None
        
    def place_monster(self, card: Card, position: MonsterPosition, zone_index: Optional[int] = None) -> int:
        if zone_index is not None:
            if zone_index >= FIELD_SIZE or self.monster_zones[zone_index] is not None:
                return -1
            self.monster_zones[zone_index] = card
            card.set_position(position)
            card.location = CardLocation.FIELD
            return zone_index
            
        for i in range(FIELD_SIZE):
            if self.monster_zones[i] is None:
                self.monster_zones[i] = card
                card.set_position(position)
                card.location = CardLocation.FIELD
                return i
                
        return -1
    
    def place_spell_trap(self, card: Card, position: SpellTrapPosition, zone_index: Optional[int] = None) -> int:
        if zone_index is not None:
            if zone_index >= FIELD_SIZE or self.spell_trap_zones[zone_index] is not None:
                return -1
            self.spell_trap_zones[zone_index] = card
            card.set_position(position)
            card.location = CardLocation.FIELD
            return zone_index
            
        for i in range(FIELD_SIZE):
            if self.spell_trap_zones[i] is None:
                self.spell_trap_zones[i] = card
                card.set_position(position)
                card.location = CardLocation.FIELD
                return i
                
        return -1
    
    def place_field_spell(self, card: Card, position: SpellTrapPosition) -> bool:
        if not card.is_spell() or card.spell_type.name != "FIELD":
            return False
            
        self.field_spell = card
        card.set_position(position)
        card.location = CardLocation.FIELD
        return True
    
    def remove_card(self, card: Card) -> bool:
        if card in self.monster_zones:
            index = self.monster_zones.index(card)
            self.monster_zones[index] = None
            return True
            
        if card in self.spell_trap_zones:
            index = self.spell_trap_zones.index(card)
            self.spell_trap_zones[index] = None
            return True
            
        if self.field_spell == card:
            self.field_spell = None
            return True
            
        return False
    
    def get_card_from_monster_zone(self, zone_index: int) -> Optional[Card]:
        if zone_index < 0 or zone_index >= FIELD_SIZE:
            return None
        return self.monster_zones[zone_index]
    
    def get_card_from_spell_trap_zone(self, zone_index: int) -> Optional[Card]:
        if zone_index < 0 or zone_index >= FIELD_SIZE:
            return None
        return self.spell_trap_zones[zone_index]
    
    def reset_turn_state(self) -> None:
        for zone in range(FIELD_SIZE):
            if self.monster_zones[zone]:
                self.monster_zones[zone].reset_turn_flags()
            if self.spell_trap_zones[zone]:
                self.spell_trap_zones[zone].reset_turn_flags()
        if self.field_spell:
            self.field_spell.reset_turn_flags()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "monster_zones": [card.to_dict() if card else None for card in self.monster_zones],
            "spell_trap_zones": [card.to_dict() if card else None for card in self.spell_trap_zones],
            "field_spell": self.field_spell.to_dict() if self.field_spell else None,
        } 