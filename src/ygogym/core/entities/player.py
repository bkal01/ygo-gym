from typing import List, Dict, Optional, Set
from src.ygogym.core.entities.card import Card
from src.ygogym.core.entities.deck import Deck
from src.ygogym.core.entities.field import Field
from src.ygogym.core.constants import STARTING_LP, FIELD_SIZE, CardType, MonsterPosition, SpellTrapPosition, CardLocation

class Player:
    def __init__(self, deck: Deck, name: str = "Player"):
        self.name = name
        self.deck = deck
        self.life_points = STARTING_LP
        
        self.hand: List[Card] = []
        self.field = Field(owner=self)
        self.graveyard: List[Card] = []
        self.banished: List[Card] = []
        self.extra_deck: List[Card] = []
        
        self.normal_summon_used = False
        self.can_conduct_battle_phase = True
        self.available_actions = set()

        self.has_lost = False
        
        for card in self.deck.main_deck + self.deck.extra_deck:
            card.owner = self
            if card.card_type == CardType.MONSTER and card.monster_type and card.monster_type.name in ["FUSION", "SYNCHRO", "XYZ", "LINK"]:
                self.extra_deck.append(card)
    
    def draw(self, count: int = 1) -> List[Card]:
        if count > self.deck.remaining_cards():
            self.has_lost = True
            return []
        drawn_cards = self.deck.draw(count=count)
        self.hand.extend(drawn_cards)
        return drawn_cards
    
    def summon_monster(self, card_index: int, position: MonsterPosition, tributes: List[int] = None) -> bool:
        if card_index >= len(self.hand):
            return False
            
        card = self.hand[card_index]
        if not card.is_monster() or not card.can_be_summoned():
            return False
            
        if tributes:
            for zone_index in sorted(tributes, reverse=True):
                monster_card = self.field.get_card_from_monster_zone(zone_index)
                if not monster_card:
                    return False
                self.send_to_graveyard(monster_card)
        
        self.hand.pop(card_index)
        placed_zone = self.field.place_monster(card, position)
        if placed_zone == -1:
            self.hand.insert(card_index, card)
            return False
            
        card.summoned_this_turn = True
        return True
    
    def set_spell_trap(self, card_index: int) -> bool:
        if card_index >= len(self.hand):
            return False
            
        card = self.hand[card_index]
        if not (card.is_spell() or card.is_trap()):
            return False
            
        if card.is_spell() and card.spell_type.name == "FIELD":
            self.hand.pop(card_index)
            if not self.field.place_field_spell(card, SpellTrapPosition.FACE_DOWN):
                self.hand.insert(card_index, card)
                return False
            return True
            
        self.hand.pop(card_index)
        placed_zone = self.field.place_spell_trap(card, SpellTrapPosition.FACE_DOWN)
        if placed_zone == -1:
            self.hand.insert(card_index, card)
            return False
            
        return True
    
    def activate_spell_trap(self, zone_index: int) -> bool:
        card = self.field.get_card_from_spell_trap_zone(zone_index)
        if not card:
            return False
            
        if not card.can_be_activated():
            return False
            
        card.set_position(SpellTrapPosition.FACE_UP)
        card.effect_activated_this_turn = True
        
        return True
    
    def send_to_graveyard(self, card: Card) -> None:
        if card.location == CardLocation.HAND:
            self.hand.remove(card)
        elif card.location == CardLocation.FIELD:
            self.field.remove_card(card)
            
        self.graveyard.append(card)
        card.location = CardLocation.GRAVEYARD
    
    def banish_card(self, card: Card) -> None:
        if card.location == CardLocation.HAND:
            self.hand.remove(card)
        elif card.location == CardLocation.FIELD:
            self.field.remove_card(card)
        elif card.location == CardLocation.GRAVEYARD:
            self.graveyard.remove(card)
            
        self.banished.append(card)
        card.location = CardLocation.BANISHED
    
    def reset_turn_state(self) -> None:
        self.normal_summon_used = False
        self.can_conduct_battle_phase = True
        self.field.reset_turn_state()
    
    def get_available_actions(self) -> Set[str]:
        self.available_actions.clear()
        return self.available_actions
    
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "life_points": self.life_points,
            "deck_count": len(self.deck.main_deck),
            "hand": [card.to_dict() for card in self.hand],
            "field": self.field.to_dict(),
            "graveyard": [card.to_dict() for card in self.graveyard],
            "banished": [card.to_dict() for card in self.banished],
            "extra_deck_count": len(self.extra_deck),
            "normal_summon_used": self.normal_summon_used,
        }

if __name__ == "__main__":
    player = Player()
    print(player.life_points)