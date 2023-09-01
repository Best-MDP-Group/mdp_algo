from abc import ABC, abstractmethod


class Command(ABC):
    def __init__(self, time):
        self.time = time
        self.ticks = int(time * constants.FRAMES)
        self.total_ticks = self.ticks

    def tick(self):
        self.ticks -= 1

    @abstractmethod
    def process_one_tick(self, robot):
        self.tick()

    @abstractmethod
    def convert_to_message(self):
        pass