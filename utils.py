import json
import pygame
import obstacle
import constants
from robot.position import Position, RobotPosition
from robot.direction import Direction
from robot.commands import TurnCommand

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
def convert_json(screen, json):
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
            obstacle.Obstacle(screen,Position(new_x,new_y, new_d),dict['id']))
    
    return new_obstacles


def chain_commands(commands):
    chained = []
    i = 0

    while i < len(commands):
        command = commands[i]

        if command.startswith('SF') or command.startswith('SB'):
            direction = 1 if command[1] == 'F' else -1
            total_value = direction * int(command[2:])
            i += 1

            while i < len(commands) and (commands[i].startswith('SF') or commands[i].startswith('SB')):
                next_direction = 1 if commands[i][1] == 'F' else -1
                total_value += next_direction * int(commands[i][2:])
                i += 1

            prefix = 'SF' if total_value > 0 else 'SB'

            # If total value is 2 digits, we add a 0 in front of it, if total value is 1 digit, we add two 0s in front of it

            if abs(total_value) < 10:
                chained_command = f"{prefix}00{abs(total_value)}"
            elif abs(total_value) < 100:
                chained_command = f"{prefix}0{abs(total_value)}"
            else:
                chained_command = f"{prefix}{abs(total_value)}"
            
            # If the total_value is 0, we skip adding it
            if total_value == 0:
                continue
            
            chained.append(chained_command)
        else:
            chained.append(command)
            i += 1

    return ','.join(chained)

def get_commands(commands):
  output = []
  
  for command in commands:
    output.append(command.rpi_message())

  return ','.join(output)

def get_atomic_commands(commands):
  output = []
  
  for command in commands:
    # if the command is of type TurnCommand, and the type_of_turn is SMALL, then we need to split it into 4 commands
    if isinstance(command, TurnCommand):
        if (command.rpi_message() == "RF090"):
            output.append("RF090")
            output.append("SB005")
        if (command.rpi_message() == "RB090"):
            output.append("RB090")
            output.append("SB005")
        if (command.rpi_message() == "LF090"):
            output.append("LF090")
            output.append("SB005")
        if (command.rpi_message() == "LB090"):
            output.append("LB090")
            output.append("SB005")     
        if (command.rpi_message() == "JF000"):
            output.append("RF034")
            output.append("LF034")
            output.append("SF010")
        if (command.rpi_message() == "KF000"):
            output.append("LF034")
            output.append("RF034")
            output.append("SF010")
        if (command.rpi_message() == "JB000"):
            output.append("RB034")
            output.append("LB034")
            output.append("SB015")
        if (command.rpi_message() == "KB000"):
            output.append("LB034")
            output.append("RB034")
            output.append("SB015")
    
    else:
      output.append(command.rpi_message())

    
  return ','.join(output)