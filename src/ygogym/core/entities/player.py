from ygogym.core import constants

class Player:
    def __init__(self):
        self.life_points = constants.STARTING_LP

        self.has_normal_summoned = False


if __name__ == "__main__":
    player = Player()
    print(player.life_points)