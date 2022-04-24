from play_game import play_game
from search_controller import a_star, depth_first_search, breadth_first_search

MAP_SHAPE = 50
DIMENSIONS_MULTIPLIER = 10
FPS = 60

if __name__ == "__main__":
    # get average a_star score
    a_star_scores = []
    print('TESTING A*')
    for i in range(20):
        score = play_game(a_star, MAP_SHAPE, FPS, DIMENSIONS_MULTIPLIER)
        print(f'    Score: {score}')
        a_star_scores.append(score)
    print(f'Average A* score: {sum(a_star_scores) / len(a_star_scores)}')
