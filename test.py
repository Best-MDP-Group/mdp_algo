import grid 
import constants
import jsonParse
import obstacle
import math
from path_finding import hamiltonian
from robot import robot
from robot.position import Position, RobotPosition
from robot.direction import Direction
import json

obstacles = jsonParse.convert_json(jsonParse.parse_json(constants.CASE_1))
grid = grid.Grid(obstacles)
robot = robot.Robot(grid, 0, 0)
robot.setCurrentPos(constants.ROBOT_SAFETY_DISTANCE, constants.ROBOT_SAFETY_DISTANCE, Direction.TOP)
hamiltonian = hamiltonian.Hamiltonian(robot,grid)
hamiltonian.get_path()
commands = [command.rpi_message() for command in hamiltonian.commands]
message_to_rpi = {
  "target": "STM", 
  "cat": "path",
  "value": {
    "commands": commands
  },
}
print(json.dumps(message_to_rpi))
