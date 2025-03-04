import random
from typing import List, Optional, Dict, Any

from src.ygogym.core.entities.card import Card
from src.ygogym.core.constants import MAX_DECK_SIZE, MIN_DECK_SIZE, MAX_EXTRA_DECK_SIZE

class Deck:
    def __init__(self, main_deck_ids: List[str], extra_deck_ids: Optional[List[str]] = None):
        if len(main_deck_ids) < MIN_DECK_SIZE or len(main_deck_ids) > MAX_DECK_SIZE:
            raise ValueError(f"Main deck must contain between {MIN_DECK_SIZE} and {MAX_DECK_SIZE} cards")
        
        extra_deck_ids = extra_deck_ids or []
        if len(extra_deck_ids) > MAX_EXTRA_DECK_SIZE:
            raise ValueError(f"Extra deck cannot contain more than {MAX_EXTRA_DECK_SIZE} cards")
        
        self.main_deck = [Card.from_id(card_id) for card_id in main_deck_ids]
        self.extra_deck = [Card.from_id(card_id) for card_id in extra_deck_ids]
        
        self.graveyard = []
        self.banished = []
    
    def shuffle(self) -> None:
        random.shuffle(self.main_deck)
    
    def draw(self) -> Optional[Card]:
        if not self.main_deck:
            return None
        return self.main_deck.pop(0)
    
    def draw_multiple(self, count: int) -> List[Card]:
        cards = []
        for _ in range(count):
            card = self.draw()
            if card:
                cards.append(card)
            else:
                break
        return cards
    
    def add_to_graveyard(self, card: Card) -> None:
        self.graveyard.append(card)
        card.location = "graveyard"
    
    def add_to_banished(self, card: Card) -> None:
        self.banished.append(card)
        card.location = "banished"
    
    def return_to_deck(self, card: Card, position: int = -1) -> None:
        if position == 0:
            self.main_deck.insert(0, card)
        elif position == -1:
            self.main_deck.append(card)
        else:
            self.main_deck.insert(position, card)
        card.location = "deck"
    
    def return_from_graveyard(self, card_index: int, position: int = -1) -> Optional[Card]:
        if 0 <= card_index < len(self.graveyard):
            card = self.graveyard.pop(card_index)
            self.return_to_deck(card, position)
            return card
        return None
    
    def return_from_banished(self, card_index: int, position: int = -1) -> Optional[Card]:
        if 0 <= card_index < len(self.banished):
            card = self.banished.pop(card_index)
            self.return_to_deck(card, position)
            return card
        return None
    
    def get_card_from_extra_deck(self, card_id: str) -> Optional[Card]:
        for i, card in enumerate(self.extra_deck):
            if card.id == card_id:
                return self.extra_deck.pop(i)
        return None
    
    def remaining_cards(self) -> int:
        return len(self.main_deck)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "main_deck": [card.to_dict() for card in self.main_deck],
            "extra_deck": [card.to_dict() for card in self.extra_deck],
            "graveyard": [card.to_dict() for card in self.graveyard],
            "banished": [card.to_dict() for card in self.banished],
            "main_deck_count": len(self.main_deck),
            "extra_deck_count": len(self.extra_deck),
            "graveyard_count": len(self.graveyard),
            "banished_count": len(self.banished)
        }
    
    @classmethod
    def from_deck_list(cls, deck_list_path: str) -> "Deck":
        """
        Create a deck from a deck list file.
        
        The file should have one card ID per line, with a section for main deck
        and extra deck separated by a line containing "!extra".
        """
        main_deck_ids = []
        extra_deck_ids = []
        
        with open(deck_list_path, 'r') as f:
            in_extra = False
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                if line.lower() == "!extra":
                    in_extra = True
                    continue
                
                if in_extra:
                    extra_deck_ids.append(line)
                else:
                    main_deck_ids.append(line)
        
        return cls(main_deck_ids, extra_deck_ids)


if __name__ == "__main__":
    deck = Deck.from_deck_list("data/test_deck.txt")
    print(deck.to_dict())
