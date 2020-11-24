# server.py

from Config import Comm, Game
import game_logic as util
import time
import random

# TODO JS does SQL & HTML stuff here

# TODO needs a name
class NeedsName:
    def __init__(self):
        self.users = []
        self.massFood = []
        self.food = []
        self.virus = []
        self.sockets = {}
        # TODO: Solve this quadtree nonesense
        self.tree = None # quadtree(0, 0, c.gameWidth, c.gameHeight);

        # TODO: How do collision ;-;
        self.sat = None # require('sat');

        # TODO i cri
        self.V = None #SAT.Vector;
        self.C = None #SAT.Circle;

    def add_food(self, to_add):
        """[summary]

        Args:
            to_add ([type]): [description]
        """
        radius = util.mass_to_radius(Game.FOOD_MASS)

        for _ in range(to_add):
            if Game.FOOD_UNIFORM_DISPOSITION:
                position = util.uniform_position(self.food, radius)
            else:
                position = util.random_position(radius)

            self.food.append(
                {
                    'id': int('{}{}'.format(time.time_ns(), len(self.food))),
                    'x': position['x'],
                    'y': position['y'],
                    'radius': radius,
                    'mass': random.random() + 2,
                    'hue': round(random.random() * 360)
                }
            )

    def add_virus(to_add):
        for _ in range(to_add):
            mass = util.random_in_range()