# server.py

from Config import Comm, Game
import game_logic as util

# TODO: Solve this quadtree nonesense
tree = None # quadtree(0, 0, c.gameWidth, c.gameHeight);

# TODO: How do collision ;-;
SAT = None # require('sat');

users = [];
massFood = [];
food = [];
virus = [];
sockets = {};

# TODO i cri
V = None #SAT.Vector;
C = None #SAT.Circle;

# TODO JS does SQL & HTML stuff here

def add_food(to_add):
    """[summary]

    Args:
        to_add ([type]): [description]
    """
    radius = util.mass_to_radius(Game.FOOD_MASS)

    for i in range(to_add):
        position = 