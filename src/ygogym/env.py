import gym
import numpy as np
from typing import Dict, List, Tuple, Any, Optional
from gym import spaces

from ygogym.core.game import Game
from ygogym.core.entities.deck import Deck
from ygogym.core.constants import Action, Phase, MonsterPosition, SpellTrapPosition

class YGOEnv(gym.Env):
    metadata = {'render.modes': ['human']}
    
    def __init__(self, agent_deck_path: str, opponent_deck_path: str):
        super(YGOEnv, self).__init__()
        
        self.agent_deck = Deck.from_deck_list(agent_deck_path)
        self.opponent_deck = Deck.from_deck_list(opponent_deck_path)
        self.game = None
        
        self.action_space = spaces.Discrete(1)
        
        self.observation_space = spaces.Dict({})
        
    def reset(self):
        self.game = Game(self.agent_deck, self.opponent_deck)
        self.game.start_game()
        return self._get_observation()
    
    def step(self, action: int) -> Tuple[Dict, float, bool, Dict]:
        pass
    
    def render(self, mode='human'):
        if mode == 'human':
            game_state = self.game.to_dict()
            print(f"Turn {game_state['turn_count']}, Phase: {game_state['current_phase']}")
            print(f"Current Player: {self.game.current_player.name}")
            
            print(f"\nPlayer 2 (LP: {self.game.player2.life_points}) - Hand: {len(self.game.player2.hand)} - Deck: {self.game.player2.deck.remaining_cards()}")
            
            if self.game.player2.hand:
                print("\nHand:")
                print("┌" + "───────────────┬" * (len(self.game.player2.hand) - 1) + "───────────────┐")
                self._print_card_row(self.game.player2.hand)
                print("└" + "───────────────┴" * (len(self.game.player2.hand) - 1) + "───────────────┘")

            self._print_field_zone("Field Spell", self.game.player2.field.field_spell)
            print("┌───────────────┬───────────────┬───────────────┬───────────────┬───────────────┐")
            self._print_card_row(self.game.player2.field.spell_trap_zones)
            print("├───────────────┼───────────────┼───────────────┼───────────────┼───────────────┤")
            self._print_card_row(self.game.player2.field.monster_zones)
            print("└───────────────┴───────────────┴───────────────┴───────────────┴───────────────┘")
            
            # Center field
            print("\n" + "─" * 90 + "\n")
            
            print("┌───────────────┬───────────────┬───────────────┬───────────────┬───────────────┐")
            self._print_card_row(self.game.player1.field.monster_zones)
            print("├───────────────┼───────────────┼───────────────┼───────────────┼───────────────┤")
            self._print_card_row(self.game.player1.field.spell_trap_zones)
            print("└───────────────┴───────────────┴───────────────┴───────────────┴───────────────┘")
            self._print_field_zone("Field Spell", self.game.player1.field.field_spell)
            
            print(f"\nPlayer 1 (LP: {self.game.player1.life_points}) - Hand: {len(self.game.player1.hand)} - Deck: {self.game.player1.deck.remaining_cards()}")
            
            if self.game.player1.hand:
                print("\nHand:")
                print("┌" + "───────────────┬" * (len(self.game.player1.hand) - 1) + "───────────────┐")
                self._print_card_row(self.game.player1.hand)
                print("└" + "───────────────┴" * (len(self.game.player1.hand) - 1) + "───────────────┘")
    
    def _print_card_row(self, cards):
        top_row = []
        bottom_row = []
        
        for card in cards:
            if card:
                if len(card.name) <= 13:
                    top_row.append(f"│ {'':<13} ")
                    bottom_row.append(f"│ {card.name:^13} ")
                else:
                    # Split longer names across two rows
                    name_parts = card.name.split()
                    top_part = ""
                    bottom_part = ""
                    
                    for part in name_parts:
                        if len(top_part) + len(part) + 1 <= 13 and not bottom_part:
                            if top_part:
                                top_part += " " + part
                            else:
                                top_part = part
                        else:
                            if bottom_part:
                                bottom_part += " " + part
                            else:
                                bottom_part = part
                    
                    # If bottom part is too long, truncate it
                    if len(bottom_part) > 13:
                        bottom_part = bottom_part[:10] + "..."
                    
                    top_row.append(f"│ {top_part:^13} ")
                    bottom_row.append(f"│ {bottom_part:^13} ")
            else:
                top_row.append(f"│ {'':<13} ")
                bottom_row.append(f"│ {'':<13} ")
        
        print("".join(top_row) + "│")
        print("".join(bottom_row) + "│")
    
    def _print_field_zone(self, label, card):
        print("┌───────────────┐")
        if card:
            name = card.name if len(card.name) <= 13 else card.name[:10] + "..."
            print(f"│ {name:^13} │ <- {label}")
        else:
            print(f"│ {'':<13} │ <- {label}")
        print("└───────────────┘")
    
    def _get_observation(self) -> Dict:
        return None
    
    def _encode_card(self, card, is_opponent=False) -> np.ndarray:
        return None
    
    def _map_action(self, action_idx: int) -> Tuple[Optional[Action], Dict[str, Any]]:
        return None, {}
    
if __name__ == "__main__":
    env = YGOEnv(agent_deck_path="data/test_deck.txt", opponent_deck_path="data/test_deck.txt")
    env.reset()
    env.render()
