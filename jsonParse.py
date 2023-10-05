import json
import obstacle
import constants
from robot.position import Position, RobotPosition
from robot.direction import Direction

# parse JSON file
def parse_json(json_str):
    try:
        data = json.loads(json_str)
        if 'cat' in data and 'value' in data:
            cat = data['cat']
            value = data['value']
            if 'obstacles' in value and 'mode' in value:
                obstacles = value['obstacles']
                mode = value['mode']
                return cat, obstacles, mode
    except json.JSONDecodeError:
        pass

    # If the JSON data doesn't match the expected structure, return None
    return None

# convert JSON file to obstacles object using specified format
def convert_json(json):
    new_obstacles = []
    cat, obstacles, mode = json
    for dict in obstacles:

        new_x = dict['x']*10
        new_y = dict['y']*10
        if dict['d'] == 0:
            new_d = Direction.TOP
        elif dict['d'] == 2:
            new_d = Direction.RIGHT
        elif dict['d'] == 4:
            new_d = Direction.BOTTOM
        elif dict['d'] == 6:
            new_d = Direction.LEFT
        
        new_obstacles.append(
            obstacle.Obstacle(Position(new_x,new_y, new_d),dict['id']))
    
    return new_obstacles

