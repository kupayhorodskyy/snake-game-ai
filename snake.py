from enum import Enum
import pygame
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


def copy_coordinates(coord1, coord2):
    coord1.x = coord2.x
    coord1.y = coord2.y


class Apple:
    pass


class Snake:
    def __init__(self):
        head = Coordinate(0, 2, Shape.HEAD)
        tail1 = Coordinate(0, 1, Shape.BODY)
        tail2 = Coordinate(0, 0, Shape.BODY)
        self.coordinates = np.array([head, tail1, tail2])
        self.direction = Direction.RIGHT

    def turn(self, direction):
        if direction not in self.get_allowed_turns():
            return
        self.direction = direction
        # self.move()

    def move(self):
        """Move the snake one cell ahead"""
        # copy the previous coordinates from tail to head
        i = len(self.coordinates) - 1
        while i > 0:
            copy_coordinates(self.coordinates[i], self.coordinates[i - 1])
            i -= 1
        # determine the new head position
        head = self.coordinates[0]
        match self.direction:
            case Direction.RIGHT:
                head.x += 1
            case Direction.LEFT:
                head.x -= 1
            case Direction.UP:
                head.y -= 1
            case Direction.DOWN:
                head.y += 1

    def grow(self):
        self.coordinates = np.append(self.coordinates, self.coordinates[-1].__copy__())

    def get_allowed_turns(self):
        """
        If the snake is moving up, it can go left or right.
        If the snake is moving right, it can go up or down.
        """
        if self.direction.value % 2 == 0:
            return Direction.RIGHT, Direction.LEFT
        else:
            return Direction.UP, Direction.DOWN


class SnakeGame:
    def __init__(self, map_shape=(100, 100)):
        self.map = np.zeros(shape=map_shape)
        self.snake = Snake()

    def move_snake(self):
        self.snake.move()

    def eat_apple(self):
        self.snake.grow()

    def draw_snake(self):
        self.map = np.zeros(shape=self.map.shape)
        for coordinate in self.snake.coordinates:
            self.map[coordinate.x, coordinate.y] = coordinate.shape.value
