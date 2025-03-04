from typing import List, Optional, Tuple, Dict, Any

from ygogym.core.constants import Phase, Action, CardLocation, MonsterPosition, SpellTrapPosition
from ygogym.core.entities.player import Player
from ygogym.core.entities.deck import Deck

class Game:
    def __init__(self, player1_deck: Deck, player2_deck: Deck, starting_player: int = 0):
        self.player1 = Player(player1_deck, name="Player 1")
        self.player2 = Player(player2_deck, name="Player 2")
        self.players = [self.player1, self.player2]
        
        self.current_player_idx = starting_player
        self.opponent_idx = 1 - starting_player
        self.turn_count = 0
        self.current_phase = None
        self.game_over = False
        self.winner = None
        
    @property
    def current_player(self) -> Player:
        return self.players[self.current_player_idx]
        
    @property
    def opponent(self) -> Player:
        return self.players[self.opponent_idx]
    
    def start_game(self):
        # Draw 6 cards for the current player and 5 for the opponent.
        for i in range(len(self.players)):
            if i == self.current_player_idx:
                self.current_player.draw(6)
            else:
                self.opponent.draw(5)
        
        self.current_phase = Phase.DRAW_PHASE
        self.turn_count = 1
        
    def next_phase(self) -> Phase:
        phase_order = [
            Phase.DRAW_PHASE,
            Phase.STANDBY_PHASE,
            Phase.MAIN_PHASE_1,
            Phase.BATTLE_PHASE,
            Phase.MAIN_PHASE_2,
            Phase.END_PHASE
        ]
        
        current_idx = phase_order.index(self.current_phase)
        next_idx = (current_idx + 1) % len(phase_order)
        
        if next_idx == 0:
            self.end_turn()
            
        self.current_phase = phase_order[next_idx]
        
        if self.current_phase == Phase.DRAW_PHASE:
            self.current_player.draw()
        
        return self.current_phase
    
    def end_turn(self):
        self.current_player.reset_turn_state()
        self.current_player_idx = self.opponent_idx
        self.opponent_idx = 1 - self.current_player_idx
        self.turn_count += 1
        
    def execute_action(self, action_type: Action, params: Dict[str, Any] = None) -> bool:
        pass
    
    def check_game_over(self) -> bool:
        if self.player1.has_lost:
            self.game_over = True
            self.winner = self.player2
            return True
            
        if self.player2.has_lost:
            self.game_over = True
            self.winner = self.player1
            return True
            
        return False
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "players": {
                "player1": self.player1.to_dict(),
                "player2": self.player2.to_dict()
            },
            "current_player": self.current_player_idx,
            "turn_count": self.turn_count,
            "current_phase": self.current_phase.value if self.current_phase else None,
            "game_over": self.game_over,
            "winner": self.winner.name if self.winner else None
        } 