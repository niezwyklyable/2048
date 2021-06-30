
class DB_Object():
    
    def __init__(self, games, game):
        self.games = games
        self.update_games(game)

    def update_games(self, game):
        self.games[game.size] = {
            'board': game.board,
            'score': game.score,
            'best_score': game.best_score,
            'previous_score': game.previous_score,
            'previous_board': game.previous_board,
            'previous_step': game.previous_step,
            'restart_screen': game.restart_screen,
            'gameover': game.gameover,
            '_2048': game._2048,
            'controls_blocked': game.controls_blocked,
            'after_2048': game.after_2048
            }

    def get_last_game(self, size):
        game = self.games[size]
        return (game['board'], game['score'], game['best_score'], game['previous_score'], \
            game['previous_board'], game['previous_step'], game['restart_screen'], game['gameover'], \
            game['_2048'], game['controls_blocked'], game['after_2048'])
