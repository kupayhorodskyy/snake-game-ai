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

    def __to_string__(self):
        return f'x: {self.x}, y: {self.y}'


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
        if self.direction in [Direction.UP, Direction.DOWN]:
            return Direction.RIGHT, Direction.LEFT
        else:
            return Direction.UP, Direction.DOWN

    def __copy__(self):
        s = Snake()
        s.head = self.head.__copy__()
        s.coordinates = self.coordinates.__copy__()
        s.direction = self.direction
        return s


class SnakeGame:
    def __init__(self, map_shape=(100, 100)):
        self.map = np.zeros(shape=map_shape)
        self.snake = Snake()
        self.apple = self.__generate_apple_coordinate()
        self.game_over = False
        self.score = 0

    def update_game(self, direction):
        self.__turn_snake(direction)
        self.__move_snake()
        if not self.game_over:
            self.__update_map()

    def get_snake_percentage(self):
        """How much of the map is the snake occupying?"""
        shape = self.map.shape[0]
        area = shape * shape
        return len(self.snake.coordinates) / area

    def __move_snake(self):
        self.snake.move()
        if self.__check_collision():
            self.game_over = True
        if self.snake.head == self.apple:
            self.__eat_apple()

    def __check_collision(self):
        x_max = self.map.shape[0]
        y_max = self.map.shape[1]
        if self.snake.head.x >= x_max or self.snake.head.x < 0:
            print('snake went off screen')
            return True
        if self.snake.head.y >= y_max or self.snake.head.y < 0:
            print('snake went off screen')
            return True
        for coordinate in self.snake.coordinates[1:]:  # check whether the snake collided with its body
            if self.snake.head == coordinate:
                print(f'snake head collided with {coordinate.x, coordinate.y}')
                return True
        return False

    def __turn_snake(self, direction):
        if direction is not None:
            self.snake.turn(direction)

    def __generate_apple_coordinate(self):
        max_range = self.map.shape[0] - 1
        x = randrange(max_range)
        y = randrange(max_range)
        if self.map[x, y] == 0:
            return Coordinate(x, y, Shape.APPLE)
        return self.__generate_apple_coordinate()

    def __eat_apple(self):
        self.snake.grow()
        self.apple = self.__generate_apple_coordinate()
        self.score += 1

    def __update_map(self):
        self.map = np.zeros(shape=self.map.shape)
        for coordinate in self.snake.coordinates:
            self.map[coordinate.x, coordinate.y] = coordinate.shape.value
        self.map[self.apple.x, self.apple.y] = self.apple.shape.value
