import json
import os

from typing import Optional, List, Dict, Any, Callable
from src.ygogym.core.constants import (
    CardType, MonsterType, MonsterAbility, MonsterAttribute, 
    MonsterRace, SpellType, TrapType, MonsterPosition, SpellTrapPosition
)

class Card:
    def __init__(
        self,
        id: str,
        name: str,
        card_type: CardType,
        description: str,
        # Monster-specific attributes
        level: Optional[int] = None,
        attack: Optional[int] = None,
        defense: Optional[int] = None,
        monster_type: Optional[MonsterType] = None,
        monster_ability: Optional[MonsterAbility] = None,
        attribute: Optional[MonsterAttribute] = None,
        race: Optional[MonsterRace] = None,
        # Spell-specific attributes
        spell_type: Optional[SpellType] = None,
        # Trap-specific attributes
        trap_type: Optional[TrapType] = None,
        # Effects and conditions
        effects: Optional[Dict[str, Callable]] = None,
        conditions: Optional[Dict[str, Callable]] = None,
    ):
        self.id = id
        self.name = name
        self.card_type = card_type
        self.description = description
        
        self.position = None
        self.owner = None
        self.location = None
        self.counters = {}
        
        # Monster attributes
        self.level = level
        self.attack = attack
        self.defense = defense
        self.monster_type = monster_type
        self.monster_ability = monster_ability
        self.attribute = attribute
        self.race = race
        
        # Spell attributes
        self.spell_type = spell_type
        
        # Trap attributes
        self.trap_type = trap_type
        
        # Effects and conditions
        self.effects = effects or {}
        self.conditions = conditions or {}
        
        self.attack_modifier = 0
        self.defense_modifier = 0
        self.level_modifier = 0
        
        self.can_attack = True
        self.can_change_position = True
        self.can_activate_effect = True
        self.summoned_this_turn = False
        self.position_changed_this_turn = False
        self.effect_activated_this_turn = False
    
    @property
    def current_attack(self) -> Optional[int]:
        if self.attack is None:
            return None
        return self.attack + self.attack_modifier
    
    @property
    def current_defense(self) -> Optional[int]:
        if self.defense is None:
            return None
        return self.defense + self.defense_modifier
    
    @property
    def current_level(self) -> Optional[int]:
        if self.level is None:
            return None
        return self.level + self.level_modifier
    
    def is_monster(self) -> bool:
        return self.card_type == CardType.MONSTER
    
    def is_spell(self) -> bool:
        return self.card_type == CardType.SPELL
    
    def is_trap(self) -> bool:
        return self.card_type == CardType.TRAP
    
    def set_position(self, position):
        if self.is_monster():
            if not isinstance(position, MonsterPosition):
                raise ValueError(f"Invalid position {position} for monster card")
        else:
            if not isinstance(position, SpellTrapPosition):
                raise ValueError(f"Invalid position {position} for spell/trap card")
        
        self.position = position
        self.position_changed_this_turn = True
    
    def can_be_summoned(self) -> bool:
        if not self.is_monster():
            return False
        return True
    
    def can_be_activated(self) -> bool:
        if self.is_monster():
            return self.can_activate_effect
        elif self.is_spell():
            return True
        elif self.is_trap():
            return True
        return False
    
    def reset_turn_flags(self):
        self.can_attack = True
        self.can_change_position = True
        self.can_activate_effect = True
        self.summoned_this_turn = False
        self.position_changed_this_turn = False
        self.effect_activated_this_turn = False
    
    def apply_effect(self, effect_name, *args, **kwargs):
        if effect_name in self.effects:
            return self.effects[effect_name](*args, **kwargs)
        return False
    
    def check_condition(self, condition_name, *args, **kwargs) -> bool:
        if condition_name in self.conditions:
            return self.conditions[condition_name](*args, **kwargs)
        return False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert card to dictionary for serialization"""
        result = {
            "id": self.id,
            "name": self.name,
            "card_type": self.card_type,
            "description": self.description,
            "location": self.location,
        }
        
        if self.position:
            result["position"] = self.position
        
        if self.is_monster():
            result.update({
                "level": self.level,
                "attack": self.attack,
                "defense": self.defense,
                "monster_type": self.monster_type,
                "monster_ability": self.monster_ability,
                "attribute": self.attribute,
                "race": self.race,
                "current_attack": self.current_attack,
                "current_defense": self.current_defense,
            })
        elif self.is_spell():
            result["spell_type"] = self.spell_type
        elif self.is_trap():
            result["trap_type"] = self.trap_type
        
        return result
    
    @staticmethod
    def from_id(id: str) -> "Card":
        with open("data/english_cards.json", 'r') as f:
            card_data = json.load(f)
        card_info = card_data.get(id)
        if not card_info:
            raise ValueError(f"Card with ID {id} not found in database")
        
        card_args = {
            "id": card_info.get("id"),
            "name": card_info.get("name"),
            "description": card_info.get("effectText", ""),
            "card_type": card_info.get("cardType", "")
        }
        
        if card_info.get("cardType") == "monster":
            card_args.update({
                "monster_type": card_info.get("type"),
                "level": card_info.get("level"),
                "attack": card_info.get("atk"),
                "defense": card_info.get("def"),
                "attribute": card_info.get("attribute")
            })
            
            if "properties" in card_info:
                pass
        
        elif card_info.get("cardType") == "spell":
            if "property" in card_info:
                card_args["spell_type"] = card_info.get("property")
        elif card_info.get("cardType") == "trap":
            if "property" in card_info:
                card_args["trap_type"] = card_info.get("property")
                
        return Card(**card_args)

if __name__ == "__main__":
    card = Card.from_id("4439")
    print(card.to_dict())
