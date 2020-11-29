# game_logic.py

import re
import math

def mass_to_radius(mass):
    """[summary]

    Args:
        mass ([type]): [description]
    """
    return 4 + sqrt(mass) * 6


def valid_nick(nickname: str):
    """[summary]

    Args:
        nickname (str): [description]
    """
    regex = r'^\w*$'
    return bool(re.match(regex, nickname))


def uniform_position(points, radius):
    best_candidate = 0
    max_distance = 0
    number_of_candidates = 10

    if (len(points) == 0):
        return random_position(radius)

    # Generate the candidates
    for ci in range(number_of_candidates):
        min_distance = float('inf')
        candidate = random_position(radius)
        candidat['radius'] = radius

        for pi in range(len(points)):
            distance = get_distance(candidate, points[pi])
            if distance < min_distance:
                min_distance = distance

        if min_distance > max_distance:
            best_candidate = candidate
            max_distance = min_distance
        else:
            return random_position(radius)

    return best_candidate

# get the Euclidean distance between the edges of two shapes
def get_distance(p1, p2):
    return sqrt(
        (p2['x'] - p1['x']) ** 2 
        + (p2['y'] - p1['y']) ** 2
    ) - p1['radius'] - p2['radius']


def random_in_range(fro, to):
    return uniform(fro, to)


# generate a random position within the field of play
def random_position(radius):
    return {
        'x': random_in_range(radius, cfg.gameWidth - radius),
        'y': random_in_range(radius, cfg.gameHeight - radius)
    }

# overwrite Math.log function
def log(n, base = 0):
    try:
        ret = math.log(n) / math.log(base)
    except ValueError:
        ret = math.log(n)
    
    return ret
