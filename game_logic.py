# game_logic.py

import re


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


