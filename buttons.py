import pygame
from robot import robot
import constants
from robot.turn_type import TurnType

def draw_button(surface, image_path, x, y, width, height, original_color, hover_color):
    mouse = pygame.mouse.get_pos()

    button_image = pygame.image.load(image_path)
    button_image = pygame.transform.scale(button_image, (width, height))

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(surface, hover_color, (x, y, width, height))
        surface.blit(button_image, (x, y))
        return True  
    else:
        pygame.draw.rect(surface, original_color, (x, y, width, height))
        surface.blit(button_image, (x, y))
        return False  

def handle_button_click(pos, robot, button_list):
    x, y = pos
    for i, button in enumerate(button_list):
        if button['x'] <= x <= button['x'] + button['width'] and button['y'] <= y <= button['y'] + button['height']:
            if button['path'] == './images/moveForward.png':
                robot.straight(10)
                print(robot.get_current_pos())
            elif button['path'] == './images/moveBackward.png':
                robot.straight(-10)
                print(robot.get_current_pos())
            elif button['path'] == './images/slantForwardLeft.png':
                robot.turn(TurnType.SMALL, True, False,
                        False)
                print(robot.get_current_pos())
            elif button['path'] == './images/slantForwardRight.png':
                robot.turn(TurnType.SMALL, False, True,
                        False)
                print(robot.get_current_pos())
            elif button['path'] == './images/turnForwardLeft.png':
                robot.turn(TurnType.MEDIUM, True, False,
                        False)
                print(robot.get_current_pos())
            elif button['path'] == './images/turnForwardRight.png':
                robot.turn(TurnType.MEDIUM, False, True,
                        False)
                print(robot.get_current_pos())
            elif button['path'] == './images/turnReverseLeft.png':
                robot.turn(TurnType.MEDIUM, True, False,
                        True)
                print(robot.get_current_pos())
            elif button['path'] == './images/turnReverseRight.png':
                robot.turn(TurnType.MEDIUM, False, True,
                        True)
                print(robot.get_current_pos())
            elif button['path'] == './images/slantBackwardsLeft.png':
                robot.turn(TurnType.SMALL, True, False,
                        True)
                print(robot.get_current_pos())
            elif button['path'] == './images/slantBackwardsRight.png':
                robot.turn(TurnType.SMALL, False, True,
                        True)
                print(robot.get_current_pos())
            break  



