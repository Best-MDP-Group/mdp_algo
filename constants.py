import pygame
# GRID
GRID_SIZE = 20
CELL_LENGTH = 10
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
RIGHT_MARGIN = int(SCREEN_WIDTH * 0.2)
TOP_BOTTOM_MARGIN = int(SCREEN_HEIGHT * 0.1)
GRID_PIXEL_SIZE = min(SCREEN_WIDTH - RIGHT_MARGIN, SCREEN_HEIGHT - 2 * TOP_BOTTOM_MARGIN)
CELL_SIZE = GRID_PIXEL_SIZE // GRID_SIZE
# INIT_VISITED = [(10,10),(20,10),(30,10),(10,20),(20,20),(30,20),(10,30),(20,30),(30,30)]
INIT_VISITED = [(10,0),(20,0),(0,0),(10,10),(20,10),(0,10),(10,20),(20,20),(0,20)]

# OBSTACLE
PINK = (255, 105, 180)
BLUE = (0, 128, 255)
OBSTACLE_LENGTH = 10
OBSTACLE_SAFETY_MARGIN = 10

# ROBOT ATTRIBUTES
ROBOT_SAFETY_DISTANCE = 10
ROBOT_SCAN_DURATION = 0.25
ROBOT_SPEED = 100

YELLOW = (255,255,0)
RED = (255,69,0)

# BUTTONS

BUTTON_LIST = [
    {'path': './images/moveForward.png', 'x': SCREEN_WIDTH - 150, 'y': 100, 'width': 30, 'height': 30},
    {'path': './images/moveBackward.png', 'x': SCREEN_WIDTH - 150, 'y': 190, 'width': 30, 'height': 30},
    {'path': './images/slantForwardLeft.png', 'x': SCREEN_WIDTH - 180, 'y': 100, 'width': 30, 'height': 30},
    {'path': './images/slantForwardRight.png', 'x': SCREEN_WIDTH - 120, 'y': 100, 'width': 30, 'height': 30},
    {'path': './images/turnForwardLeft.png', 'x': SCREEN_WIDTH - 180, 'y': 130, 'width': 30, 'height': 30},
    {'path': './images/turnForwardRight.png', 'x': SCREEN_WIDTH - 120, 'y': 130, 'width': 30, 'height': 30},
    {'path': './images/turnReverseLeft.png', 'x': SCREEN_WIDTH - 180, 'y': 160, 'width': 30, 'height': 30},
    {'path': './images/turnReverseRight.png', 'x': SCREEN_WIDTH - 120, 'y': 160, 'width': 30, 'height': 30},
    {'path': './images/slantBackwardsLeft.png', 'x': SCREEN_WIDTH - 180, 'y': 190, 'width': 30, 'height': 30},
    {'path': './images/slantBackwardsRight.png', 'x': SCREEN_WIDTH - 120, 'y': 190, 'width': 30, 'height': 30},

]

START_BUTTON =     {
    'text': 'START',  # Text or image path
    'x': SCREEN_WIDTH - 200,  # 100 pixels from the right
    'y': SCREEN_HEIGHT - 150,  # 50 pixels from the bottom
    'width': 150,  # button width
    'height': 80,  # button height
}

FRAMES = 50