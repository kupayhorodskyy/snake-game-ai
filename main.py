from snake import SnakeGame, Direction
import pygame

DIMENSIONS_MULTIPLIER = 10

if __name__ == "__main__":
    pygame.init()
    sg = SnakeGame(map_shape=(50, 50))

    x = sg.map.shape[0]
    y = sg.map.shape[1]

    screen_width = x * DIMENSIONS_MULTIPLIER
    screen_height = y * DIMENSIONS_MULTIPLIER

    screen = pygame.display.set_mode([screen_width, screen_height])
    clock_object = pygame.time.Clock()

    while not sg.game_over:
        sg.update_map()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sg.game_over = True
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_LEFT:
                        sg.turn_snake(Direction.LEFT)
                    case pygame.K_RIGHT:
                        sg.turn_snake(Direction.RIGHT)
                    case pygame.K_DOWN:
                        sg.turn_snake(Direction.DOWN)
                    case pygame.K_UP:
                        sg.turn_snake(Direction.UP)

        screen.fill((0, 0, 0))
        for i in range(x):
            for j in range(y):
                if sg.map[i, j] != 0:
                    # color = (0, 0, 0)
                    match sg.map[i, j]:
                        case 3:
                            color = (255, 0, 0)
                        case _:
                            color = (0, 255, 0)
                    rect = pygame.Rect(i * DIMENSIONS_MULTIPLIER, j * DIMENSIONS_MULTIPLIER, DIMENSIONS_MULTIPLIER,
                                       DIMENSIONS_MULTIPLIER)
                    pygame.draw.rect(screen, color, rect)
        pygame.display.flip()
        sg.move_snake()
        clock_object.tick(30)

    pygame.quit()
