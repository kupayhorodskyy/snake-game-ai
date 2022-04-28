from play_game import play_game, play_game_without_drawing
from search_controller import a_star, depth_first_search, breadth_first_search, greedy_best_first_search, \
    a_star_with_forward_checking, a_start_forward_checking_tail_tracking

MAP_SHAPE = 15
DIMENSIONS_MULTIPLIER = 30
FPS = 60
NUM_OF_TESTS = 15

if __name__ == "__main__":
    print(play_game(a_start_forward_checking_tail_tracking, MAP_SHAPE, FPS, DIMENSIONS_MULTIPLIER))

    # a_star_scores = []
    # print('TESTING A*')
    # for i in range(NUM_OF_TESTS):
    #     score = play_game_without_drawing(a_star, MAP_SHAPE)
    #     print(f'    Score: {score}')
    #     a_star_scores.append(score)
    # print(f'Average A* score: {sum(a_star_scores) / len(a_star_scores)}')
    #
    # a_star_with_forward_checking_scores = []
    # print('TESTING A* WITH FORWARD CHECKING')
    # for i in range(NUM_OF_TESTS):
    #     score = play_game_without_drawing(a_star_with_forward_checking, MAP_SHAPE)
    #     print(f'    Score: {score}')
    #     a_star_with_forward_checking_scores.append(score)
    # print(
    #     f'Average A* WITH FORWARD CHECKING score: {sum(a_star_with_forward_checking_scores) / len(a_star_with_forward_checking_scores)}')
    #
    # bfs_scores = []
    # print('TESTING BFS')
    # for i in range(NUM_OF_TESTS):
    #     score = play_game_without_drawing(breadth_first_search, MAP_SHAPE)
    #     print(f'    Score: {score}')
    #     bfs_scores.append(score)
    # print(f'Average BFS score: {sum(bfs_scores) / len(bfs_scores)}')
    #
    # dfs_scores = []
    # print('TESTING DFS')
    # for i in range(NUM_OF_TESTS):
    #     score = play_game_without_drawing(depth_first_search, MAP_SHAPE)
    #     print(f'    Score: {score}')
    #     dfs_scores.append(score)
    # print(f'Average DFS score: {sum(dfs_scores) / len(dfs_scores)}')
    #
    # super_algorithm_scores = []
    # print('TESTING SUPER ALGORITHM')
    # for i in range(NUM_OF_TESTS):
    #     score = play_game_without_drawing(a_start_forward_checking_tail_tracking, MAP_SHAPE)
    #     print(f'    Score: {score}')
    #     super_algorithm_scores.append(score)
    # print(f'Average SUPER ALGORITHM score: {sum(super_algorithm_scores) / len(super_algorithm_scores)}')
    #
    # # greedy_bfs_scores = []
    # # print('TESTING GREEDY BFS')
    # # for i in range(NUM_OF_TESTS):
    # #     score = play_game_without_drawing(greedy_best_first_search, MAP_SHAPE)
    # #     print(f'    Score: {score}')
    # #     greedy_bfs_scores.append(score)
    # # print(f'Average GREEDY BFS score: {sum(greedy_bfs_scores) / len(greedy_bfs_scores)}')
    #
    # print("==== TESTING COMPLETE ====")
    # print(f'Average A* score: {sum(a_star_scores) / len(a_star_scores)}')
    # print(
    #     f'Average A* WFC score: {sum(a_star_with_forward_checking_scores) / len(a_star_with_forward_checking_scores)}')
    # print(f'Average SUPER ALGORITHM score: {sum(super_algorithm_scores) / len(super_algorithm_scores)}')
    # print(f'Average BFS score: {sum(bfs_scores) / len(bfs_scores)}')
    # print(f'Average DFS score: {sum(dfs_scores) / len(dfs_scores)}')
    # print("==== END TESTING RESULTS ====")
