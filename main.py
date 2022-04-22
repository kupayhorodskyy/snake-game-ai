from snake import SnakeGame, Direction
from search_controller import SearchController, straight_line_move, a_star, depth_first_search
import pygame

DIMENSIONS_MULTIPLIER = 10
FPS = 60

if __name__ == "__main__":
    pygame.init()
    sg = SnakeGame(map_shape=(50, 50))
    # controller = SearchController(sg, straight_line_move)
    # controller = SearchController(sg, a_star)
    controller = SearchController(sg, depth_first_search)

    x = sg.map.shape[0]
    y = sg.map.shape[1]

    screen_width = x * DIMENSIONS_MULTIPLIER
    screen_height = y * DIMENSIONS_MULTIPLIER

    screen = pygame.display.set_mode([screen_width, screen_height])
    clock_object = pygame.time.Clock()

    while not sg.game_over:
        sg.update_map()
        sg.move_snake()
        sg.turn_snake(controller.get_next_move())

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

        # sg.turn_snake(controller.get_next_move())

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
                    rect = pygame.Rect(i * DIMENSIONS_MULTIPLIER, j * DIMENSIONS_MULTIPLIER, DIMENSIONS_MULTIPLIER,
                                       DIMENSIONS_MULTIPLIER)
                    pygame.draw.rect(screen, color, rect)
        pygame.display.flip()
        clock_object.tick(FPS)

    print(f'Game over. Score: {sg.score}')
    print(f'The snake position was: {[c.__to_string__() for c in sg.snake.coordinates]}')
    print(f'The move set was: {controller.moves}')

    while True:
        clock_object.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
