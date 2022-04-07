from snake import SnakeGame

if __name__ == "__main__":
    sg = SnakeGame()
    sg.draw_snake()
    print(sg.map)
    sg.eat_apple()
    sg.move_snake()
    sg.draw_snake()
    print(sg.map)
    sg.move_snake()
    sg.draw_snake()
    print(sg.map)

