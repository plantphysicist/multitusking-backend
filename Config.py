class Comm:
    """Constants related to communication.
    """
    HOST = '127.0.0.1'
    PORT = '2392'
    
class Game:
    """Game-related constants.
    """
    DEFAULT_PLAYER_MASS = 10
    FOOD_MASS = 1
    FOOD_UNIFORM_DISPOSITION = True
    VIRUS_UNIFORM_DISPOSITION = True
    SLOW_BASE = 4.5
    MERGE_TIMER = 15

class Virus:
    """[summary]
    """
    DEFAULT_MASS_FROM = 100
    DEFAULT_MASS_TO = 150
    FILL = '#33ff33'
    STROKE = '#19D119'
    STROKE_WIDTH = 20
    SPLIT_MASS = 180