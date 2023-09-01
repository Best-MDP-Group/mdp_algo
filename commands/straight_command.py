from commands.command import Command
from robot.direction import Direction
from robot.positioning import Position

class StraightCommand(Command):
    ROBOT_SPEED_PER_SECOND = 100  # Adjust the value as needed

    def __init__(self, dist):
        time = abs(dist / StraightCommand.ROBOT_SPEED_PER_SECOND)
        super().__init__(time)
        self.dist = dist

    def __str__(self):
        return f"StraightCommand(dist={self.dist}, {self.total_ticks} ticks)"

    def process_one_tick(self, robot):
        if self.total_ticks == 0:
            return

        self.tick()
        distance = self.dist / self.total_ticks
        robot.straight(distance)

    def apply_on_pos(self, curr_pos: Position):
        if curr_pos.direction == Direction.RIGHT:
            curr_pos.x += self.dist
        elif curr_pos.direction == Direction.TOP:
            curr_pos.y += self.dist
        elif curr_pos.direction == Direction.BOTTOM:
            curr_pos.y -= self.dist
        else:
            curr_pos.x -= self.dist

        return self

    def convert_to_message(self):
        if int(self.dist) < 0:
            if int(self.dist) > -100:
                return f"SB0{-self.dist}"
            else:
                return f"SB{-self.dist}"
        else:
            if int(self.dist) >= 100:
                return f"SF{self.dist}"
            else:
                return f"SF0{self.dist}"