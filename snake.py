from enum import Enum
from random import randrange
import numpy as np


class Shape(Enum):
    EMPTY = 0
    HEAD = 1
    BODY = 2
    APPLE = 3


class Direction(Enum):
    LEFT = 1
    RIGHT = 3
    UP = 2
    DOWN = 4


class Coordinate:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape

    def __copy__(self):
        return Coordinate(self.x, self.y, self.shape)

    def __eq__(self, other):
        return isinstance(other, Coordinate) and self.x == other.x and self.y == other.y


def copy_coordinates(coord1, coord2):
    coord1.x = coord2.x
    coord1.y = coord2.y


class Snake:
    def __init__(self):
        head = Coordinate(2, 0, Shape.HEAD)
        tail1 = Coordinate(1, 0, Shape.BODY)
        tail2 = Coordinate(0, 0, Shape.BODY)
        self.coordinates = np.array([head, tail1, tail2])
        self.head = self.coordinates[0]
        self.direction = Direction.DOWN

    def turn(self, direction):
        if direction in self.get_allowed_turns():
            self.direction = direction

    def move(self):
        """Move the snake one cell ahead"""
        # copy the previous coordinates from tail to head
        i = len(self.coordinates) - 1
        while i > 0:
            copy_coordinates(self.coordinates[i], self.coordinates[i - 1])
            i -= 1
        # determine the new head position
        # head = self.coordinates[0]
        match self.direction:
            case Direction.RIGHT:
                self.head.x += 1
            case Direction.LEFT:
                self.head.x -= 1
            case Direction.UP:
                self.head.y -= 1
            case Direction.DOWN:
                self.head.y += 1

    def grow(self):
        self.coordinates = np.append(self.coordinates, self.coordinates[-1].__copy__())

    def get_allowed_turns(self):
        """
        If the snake is moving up, it can go left or right.
        If the snake is moving right, it can go up or down.
        """
        # if self.direction.value % 2 == 0:
        #     return Direction.RIGHT, Direction.LEFT
        # else:
        #     return Direction.UP, Direction.DOWN
        if self.direction in [Direction.UP, Direction.DOWN]:
            return Direction.RIGHT, Direction.LEFT
        else:
            return Direction.UP, Direction.DOWN


class SnakeGame:
    def __init__(self, map_shape=(100, 100)):
        self.map = np.zeros(shape=map_shape)
        self.snake = Snake()
        self.apple = self.generate_apple_coordinate()
        self.game_over = False

    def move_snake(self):
        self.snake.move()
        if self.check_collision():
            self.game_over = True
        if self.snake.head == self.apple:
            self.eat_apple()

    def check_collision(self):
        x_max = self.map.shape[0]
        y_max = self.map.shape[1]
        if self.snake.head.x >= x_max or self.snake.head.x < 0:
            return True
        if self.snake.head.y >= y_max or self.snake.head.y < 0:
            return True
        for coordinate in self.snake.coordinates[1:]:
            if self.snake.head == coordinate:
                return True
        return False

    def turn_snake(self, direction):
        self.snake.turn(direction)

    def generate_apple_coordinate(self):
        max_range = self.map.shape[0] - 1
        x = randrange(max_range)
        y = randrange(max_range)
        if self.map[x, y] == 0:
            return Coordinate(x, y, Shape.APPLE)
        return self.generate_apple_coordinate()

    def eat_apple(self):
        self.snake.grow()
        self.apple = self.generate_apple_coordinate()

    def update_map(self):
        self.map = np.zeros(shape=self.map.shape)
        for coordinate in self.snake.coordinates:
            self.map[coordinate.x, coordinate.y] = coordinate.shape.value
        self.map[self.apple.x, self.apple.y] = self.apple.shape.value
