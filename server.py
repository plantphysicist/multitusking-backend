# server.py

import Config
import game_logic as util
import time
import random
import math

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

        self.init_mass_log = util.log(Config.Game.DEFAULT_PLAYER_MASS, Config.Game.SLOW_BASE)

    def add_food(self, to_add):
        """[summary]

        Args:
            to_add ([type]): [description]
        """
        radius = util.mass_to_radius(Config.Game.FOOD_MASS)

        for _ in range(to_add):
            if Config.Game.FOOD_UNIFORM_DISPOSITION:
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

    def add_virus(self, to_add):
        for _ in range(to_add):
            mass = util.random_in_range(Config.Virus.DEFAULT_MASS_FROM, Config.Virus.DEFAULT_MASS_TO)
            radius = util.mass_to_radius(mass)
            if Config.Game.VIRUS_UNIFORM_DISPOSITION:
                position = util.uniform_position(self.virus, radius)
            else:
                position = util.random_position(radius)
            
            self.virus.append(
                {
                    'id': int('{}{}'.format(time.time_ns(), len(self.virus))),
                    'x': position['x'],
                    'y': position['y'],
                    'radius': radius,
                    'mass': mass,
                    'fill': Config.Virus.FILL,
                    'stroke': Config.Virus.STROKE,
                    'stroke_width': Config.Virus.STROKE_WIDTH
                }
            )

    def remove_food(self, to_rem):
        for _ in range(to_rem):
            self.food.pop()

    def move_player(self, player):
        x = 0
        y = 0
        for i in range(len(player.cells)):
            target = {
                'x': player.x - player.cells[i].x + player.target.x,
                'y': player.y - player.cells[i].y + player.target.y
            }
            dist = sqrt(target['y'] ** 2 + target.x ** 2)
            deg = math.atan2(target['y'], target['x'])
            slow_down = 1
            if player.cells[i].speed <= 6.25:
                slow_down = util.log(player.cells[i].mass, Config.Game.SLOW_BASE) - self.init_mass_log - 1

            delta_y = player.cells[i].speed * math.sin(deg) / slow_down
            delta_x = player.cells[i].speed * math.cos(deg) / slow_down

            if player.cells[i].speed > 6.25:
                player.cells[i].speed -= 0.5

            if dist < (50 + player.cells[i].radius):
                delta_y *= dist / (50 + player.cells[i].radius)
                delta_x *= dist / (50 + player.cells[i].radius)

            player.cells[i].y += delta_y
            player.cells[i].x += delta_x

            # TODO Find best solution.
            for j in range(len(player.cells)):
                if j != i and player.cells[i]:
                    distance = sqrt((player.cells[j].y - player.cells[i].y) ** 2)
                               + (player.cells[j].x - player.cells[i].x) ** 2
                    radius_total = player.cells[i].radius + player.cells[j].radius
                    if distance < radius_total:
                        if player.last_split >  time.time_ns() - 1000 * Config.Game.MERGE_TIMER:
                            if player.cells[i]['x'] < player.cells[j]['x']:

    def move_mass(self, mass):
        pass

    def balance_mass(self):
        pass

    def tick_player(current_player):
        pass

    def func_food(self, f):
        pass

    def delete_food(self, f):
        pass

    def eat_mass(self, m):
        pass

    def check(self, user):
        pass

    def collision_check(self, collision):
        pass

    def move_loop(self):
        pass

    def game_loop(self):
        pass
    
    def send_updates(self):
        pass
