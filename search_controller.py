import math
import numpy as np
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
        if self.algorithm is super_algorithm:
            cells = self.algorithm(head.__copy__(), apple.__copy__(), self.sg.map, self.sg.snake)
        else:
            cells = self.algorithm(head.__copy__(), apple.__copy__(), self.sg.map)
        if cells is None:
            cells = [survive((head.x, head.y), self.sg.map)]
            if cells[0] is None:  # dead end, terminate gracefully
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
            return None  # dead end
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

    while open_set:
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


def super_algorithm(start, goal, game_map, snake):
    s = (start.x, start.y)
    g = (goal.x, goal.y)

    apple_coordinate = g
    head_coordinate = [snake.head.x, snake.head.y]
    body_coordinates = [[c.x, c.y] for c in snake.coordinates[1:]]

    initial_state = [head_coordinate, body_coordinates]

    def generate_map(head_c, body_cs):
        m = np.zeros((game_map.shape[0], game_map.shape[1]))
        m[apple_coordinate] = Shape.APPLE.value
        m[head_c] = Shape.HEAD.value
        for c in body_cs:
            m[c[0], c[1]] = Shape.BODY.value
        return m

    came_from = {}
    g_score_map = {}
    f_score_map = {}
    state_map = {}
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

    state_map[s] = initial_state

    while open_set:
        popped = heapq.heappop(open_set)
        current = popped[1]
        current_state = state_map[current]
        current_body = current_state[1]
        current_map = generate_map(current, current_body)

        if current == g:
            if forward_check(current, game_map)[0]:
                return __reconstruct_path(came_from, current)

        for neighbor in __get_neighbors(current, current_map):
            tentative_g_score = g_score(current) + 1
            if tentative_g_score < g_score(neighbor):
                # this path to the neighbor is better
                came_from[neighbor] = current
                g_score_map[neighbor] = tentative_g_score
                f_score_map[neighbor] = tentative_g_score + __h(neighbor, g)
                if neighbor not in open_set:
                    heapq.heappush(open_set, (f_score(neighbor), neighbor))
                # generate neighbor state
                neighbor_body = np.concatenate(([current], current_body[:-1]))
                state_map[neighbor] = [neighbor, neighbor_body]
    return None  # failure


def a_star_with_forward_checking(start, goal, game_map):
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

    while open_set:
        popped = heapq.heappop(open_set)
        current = popped[1]
        if current == g:
            if forward_check(current, game_map)[0]:
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


def forward_check(node, game_map):
    #  do bfs for reachable nodes
    def __num_of_empty_cells(gmap):
        return len(gmap[gmap == Shape.EMPTY.value])

    reachable_neighbors = 0
    visited = set()

    queue = [node]
    while queue:
        current = queue.pop(0)
        for neighbor in __get_neighbors(current, game_map):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                reachable_neighbors += 1
        if reachable_neighbors / __num_of_empty_cells(game_map) >= 0.30:
            return True, reachable_neighbors
    return False, reachable_neighbors


def greedy_best_first_search(start, goal, game_map):
    s = (start.x, start.y)
    g = (goal.x, goal.y)
    visited = set()
    came_from = {}
    open_set = []
    heapq.heappush(open_set, (__h(s, g), s))

    while open_set:
        current = heapq.heappop(open_set)[1]
        if current == g:
            return __reconstruct_path(came_from, current)
        visited.add(current)
        for neighbor in __get_neighbors(current, game_map):
            if neighbor not in visited:
                came_from[neighbor] = current
                heapq.heappush(open_set, (__h(neighbor, g), neighbor))

    return None


def survive(node, game_map):
    max_x = game_map.shape[0] - 1
    max_y = game_map.shape[1] - 1
    neighbors = __get_neighbors(node, game_map)
    if len(neighbors) == 0:
        return None
    evaluated_neighbors = []
    while neighbors:
        n = neighbors.pop()
        check = forward_check(n, game_map)
        edge = n[0] >= max_x or n[0] <= 0 or n[1] >= max_y or n[1] <= 0
        if check[0] and not edge:
            return Coordinate(n[0], n[1], Shape.EMPTY)
        evaluated_neighbors.append([n, check[1]])

    # if there is no node that is not on the edge, return the one with the most reachable nodes
    best = max(evaluated_neighbors, key=lambda neighbor: neighbor[1])
    return Coordinate(best[0][0], best[0][1], Shape.EMPTY)
