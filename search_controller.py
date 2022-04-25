import math
from snake import Coordinate, Direction, Shape
import heapq


class SearchController:
    def __init__(self, sg, algorithm):
        self.sg = sg
        self.moves = []
        self.algorithm = algorithm

    def __calculate_next_moves(self):
        head = self.sg.snake.head.__copy__()
        apple = self.sg.apple.__copy__()
        cells = self.algorithm(head.__copy__(), apple.__copy__(), self.sg.map)
        if cells is None:
            cells = [survive((head.x, head.y), self.sg.map)]
            if cells[0] is None:
                self.moves = None
                return

        self.moves = []
        for cell in cells:
            if cell.x > head.x:
                head.x += 1
                self.moves.append(Direction.RIGHT)
            elif cell.x < head.x:
                head.x -= 1
                self.moves.append(Direction.LEFT)
            elif cell.y > head.y:
                head.y += 1
                self.moves.append(Direction.DOWN)
            elif cell.y < head.y:
                head.y -= 1
                self.moves.append(Direction.UP)

    def get_next_move(self):
        if self.moves is None:
            return None
        if len(self.moves) == 0:
            self.__calculate_next_moves()
            return self.get_next_move()
        return self.moves.pop(0)


def straight_line_move(node, goal, game_map):
    cells = []
    # move to x position
    while node != goal:
        if node.x < goal.x:
            node.x += 1
            cells.append(node.__copy__())
        elif node.x > goal.x:
            node.x -= 1
            cells.append(node.__copy__())
        elif node.y < goal.y:
            node.y += 1
            cells.append(node.__copy__())
        elif node.y > goal.y:
            node.y -= 1
            cells.append(node.__copy__())

    return cells


def __h(node, goal):
    # return math.dist(node, goal)
    return math.fabs(node[0] - goal[0]) + math.fabs(node[1] - goal[1])


def __reconstruct_path(came_from, current):
    cells = [Coordinate(current[0], current[1], Shape.EMPTY)]
    while current in came_from.keys():
        current = came_from[current]
        cells.insert(0, Coordinate(current[0], current[1], Shape.EMPTY))
    return cells


def __get_neighbors(node, game_map):
    x = node[0]
    y = node[1]
    shape = game_map.shape

    potential_neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    neighbors = []

    for n in potential_neighbors:
        if n[0] >= shape[0] or n[0] < 0 or n[1] >= shape[1] or n[1] < 0 \
                or int(game_map[n[0], n[1]]) in (1, 2):
            continue
        neighbors.append(n)
    return neighbors


def a_star(start, goal, game_map):
    s = (start.x, start.y)
    g = (goal.x, goal.y)

    came_from = {}
    g_score_map = {}
    f_score_map = {}
    open_set = []

    def g_score(node):
        if node in g_score_map.keys():
            return g_score_map[node]
        return math.inf

    def f_score(node):
        if node in f_score_map.keys():
            return f_score_map[node]
        return math.inf

    g_score_map[s] = 0
    f_score_map[s] = __h(s, g)
    heapq.heappush(open_set, (f_score(s), s))

    while len(open_set) > 0:
        popped = heapq.heappop(open_set)
        current = popped[1]
        if current == g:
            return __reconstruct_path(came_from, current)

        for neighbor in __get_neighbors(current, game_map):
            tentative_g_score = g_score(current) + 1
            if tentative_g_score < g_score(neighbor):
                # get neighbor direction

                # this path to the neighbor is better
                came_from[neighbor] = current
                g_score_map[neighbor] = tentative_g_score
                f_score_map[neighbor] = tentative_g_score + __h(neighbor, g)
                if neighbor not in open_set:
                    heapq.heappush(open_set, (f_score(neighbor), neighbor))
    return None  # failure


def depth_first_search(start, goal, game_map):
    s = (start.x, start.y)
    g = (goal.x, goal.y)

    visited = set()
    stack = [s]
    came_from = {}

    while stack:
        v = stack.pop()
        if v == g:
            return __reconstruct_path(came_from, v)
        if v not in visited:
            visited.add(v)
            for n in __get_neighbors(v, game_map):
                if n not in visited:
                    stack.append(n)
                    came_from[n] = v
    return None


def breadth_first_search(start, goal, game_map):
    s = (start.x, start.y)
    g = (goal.x, goal.y)
    visited = set()
    came_from = {}
    queue = [s]

    while queue:
        v = queue.pop(0)
        if v == g:
            return __reconstruct_path(came_from, v)
        if v not in visited:
            visited.add(v)
            for n in __get_neighbors(v, game_map):
                if n not in visited:
                    queue.append(n)
                    came_from[n] = v
    return None


def survive(node, game_map):
    neighbors = __get_neighbors(node, game_map)
    if len(neighbors) == 0:
        return None
    n = neighbors[0]
    return Coordinate(n[0], n[1], Shape.EMPTY)
