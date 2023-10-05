from flask import Flask, request, jsonify
import grid 
import constants
import jsonParse
import obstacle
import math
from path_finding import hamiltonian
from robot import robot
from robot.position import Position, RobotPosition
from robot.direction import Direction

app = Flask(__name__)

@app.route('/get_path', methods=['POST'])
def get_path():
    data = request.get_data()
    obs = data.decode('utf-8')
    print(data)
    
    obstacles = jsonParse.convert_json(jsonParse.parse_json(obs))

    grid_instance = grid.Grid(obstacles)
    robot_instance = robot.Robot(grid_instance, 0, 0)
    robot_instance.setCurrentPos(constants.ROBOT_SAFETY_DISTANCE, constants.ROBOT_SAFETY_DISTANCE, Direction.TOP)
    hamiltonian_instance = hamiltonian.Hamiltonian(robot_instance, grid_instance)
    hamiltonian_instance.get_path()
    commands = [command.rpi_message() for command in hamiltonian_instance.commands]
    message_to_rpi = {
    "target": "STM", 
    "cat": "path",
    "value": {
        "commands": commands
    },
    }
    return jsonify(message_to_rpi)

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000,debug=False)
