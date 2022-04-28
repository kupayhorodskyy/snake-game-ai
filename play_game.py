from snake import SnakeGame
from search_controller import SearchController
import pygame


def play_game(controller_algorithm, map_shape, fps, dimensions_multiplier):
    pygame.init()
    sg = SnakeGame(map_shape=(map_shape, map_shape))
    # fix?
    sg.update_game(sg.snake.direction)
    controller = SearchController(sg, controller_algorithm)

    x = sg.map.shape[0]
    y = sg.map.shape[1]

    screen_width = x * dimensions_multiplier
    screen_height = y * dimensions_multiplier

    screen = pygame.display.set_mode([screen_width, screen_height])
    clock_object = pygame.time.Clock()

    while not sg.game_over:
        sg.update_game(controller.get_next_move())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sg.game_over = True
            # elif event.type == pygame.KEYDOWN:
            #     match event.key:
            #         case pygame.K_LEFT:
            #             sg.turn_snake(Direction.LEFT)
            #         case pygame.K_RIGHT:
            #             sg.turn_snake(Direction.RIGHT)
            #         case pygame.K_DOWN:
            #             sg.turn_snake(Direction.DOWN)
            #         case pygame.K_UP:
            #             sg.turn_snake(Direction.UP)

        screen.fill((0, 0, 0))
        for i in range(x):
            for j in range(y):
                if sg.map[i, j] != 0:
                    # color = (0, 0, 0)
                    match sg.map[i, j]:
                        case 3:
                            color = (255, 0, 0)
                        case 1:
                            color = (0, 0, 255)
                        case _:
                            color = (0, 255, 0)
                    rect = pygame.Rect(i * dimensions_multiplier, j * dimensions_multiplier, dimensions_multiplier,
                                       dimensions_multiplier)
                    pygame.draw.rect(screen, color, rect)
        pygame.display.flip()
        clock_object.tick(fps)
    return sg.score


def play_game_without_drawing(controller_algorithm, map_shape):
    print("NEW GAME")
    sg = SnakeGame(map_shape=(map_shape, map_shape))
    controller = SearchController(sg, controller_algorithm)
    counter = 0
    while not sg.game_over:
        sg.update_game(controller.get_next_move())
        counter += 1
        if counter % 200 == 0:
            print(".", end='')
    return sg.score
