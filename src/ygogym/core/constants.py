from enum import Enum

# Game constants
MAX_PLAYERS = 2
STARTING_LP = 8000
MAX_HAND_SIZE = 5
FIELD_SIZE = 5
MIN_DECK_SIZE = 40
MAX_DECK_SIZE = 60
MAX_EXTRA_DECK_SIZE = 15

# Game Enums
class Phase(Enum):
    DRAW_PHASE = "draw_phase"
    STANDBY_PHASE = "standby_phase"
    MAIN_PHASE_1 = "main_phase_1"
    BATTLE_PHASE = "battle_phase"
    MAIN_PHASE_2 = "main_phase_2"
    END_PHASE = "end_phase"

# Card Enums
class CardType(Enum):
    MONSTER = "monster"
    SPELL = "spell"
    TRAP = "trap"

class MonsterType(Enum):
    NORMAL = "normal"
    EFFECT = "effect"
    FUSION = "fusion"

class MonsterAbility(Enum):
    NONE = "none"
    FLIP = "flip"

class MonsterAttribute(Enum):
    LIGHT = "light"
    DARK = "dark"
    FIRE = "fire"
    WATER = "water"
    WIND = "wind"
    EARTH = "earth"
    DIVINE = "divine"

class MonsterRace(Enum):
    # sorry, race is an old name for type!
    AQUA = "aqua"
    BEAST = "beast"
    BEAST_WARRIOR = "beast_warrior"
    CYBERSE = "cyberse"
    DINOSAUR = "dinosaur"
    DIVINE_BEAST = "divine_beast"
    DRAGON = "dragon"
    FAIRY = "fairy"
    FIEND = "fiend"
    FISH = "fish"
    ILLUSION = "illusion"
    INSECT = "insect"
    MACHINE = "machine"
    PLANT = "plant"
    PSYCHIC = "psychic"
    PYRO = "pyro"
    REPTILE = "reptile"
    ROCK = "rock"
    SEA_SERPENT = "sea_serpent"
    SPELLCASTER = "spellcaster"
    THUNDER = "thunder"
    WARRIOR = "warrior"
    WINGED_BEAST = "winged_beast"
    WYRM = "wyrm"
    
class SpellType(Enum):
    NORMAL = "normal"
    CONTINUOUS = "continuous"
    FIELD = "field"
    EQUIP = "equip"

class TrapType(Enum):
    NORMAL = "normal"
    CONTINUOUS = "continuous"
    COUNTER = "counter"
    
class MonsterPosition(Enum):
    FACE_UP_ATTACK = "face_up_attack"
    FACE_UP_DEFENSE = "face_up_defense"
    FACE_DOWN_DEFENSE = "face_down_defense"

class SpellTrapPosition(Enum):
    FACE_UP = "face_up"
    FACE_DOWN = "face_down"

class CardLocation(Enum):
    DECK = "deck"
    HAND = "hand"
    FIELD = "field"
    GRAVEYARD = "graveyard"
    BANISHED = "banished"
    EXTRA_DECK = "extra_deck"

# Actions
class Action(Enum):
    DRAW = "draw"
    NORMAL_SUMMON = "normal_summon"
    TRIBUTE_SUMMON = "tribute_summon"
    FLIP_SUMMON = "flip_summon"
    SPECIAL_SUMMON = "special_summon"

    ACTIVATE_SPELL = "activate_spell"
    ACTIVATE_SPELL_EFFECT = "activate_spell_effect"
    SET_SPELL = "set_spell"
    ACTIVATE_TRAP = "activate_trap"
    ACTIVATE_TRAP_EFFECT = "activate_trap_effect"
    SET_TRAP = "set_trap"

    ACTIVATE_MONSTER_EFFECT = "activate_monster_effect"

    CHANGE_MONSTER_POSITION = "change_monster_position"
    DISCARD = "discard"

    END_TURN = "end_turn"
