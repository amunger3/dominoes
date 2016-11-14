import dominoes

class Series:
    '''
    Python class for objects that represent a series of dominoes games.

    A series of dominoes games is played with 4 players, split into two teams.
    They will then play a sequence of games and keep a running tally of how
    many points each team has scored. When a team's cumulative score surpasses
    some predetermined threshold (usually 100 or 200), that team wins.

    Prior to starting the series, the teams agree to a starting domino (usually
    [6|6]). The player that draws this domino during the first game will play
    first. The starting player for subsequent games is determined as follows:
        * If a player wins by playing their last domino, that player will start
          the following game.
        * If a player makes the game stuck, and his/her team wins, that player
          will start the following game.
        * If a player makes the game stuck, and there is a tie, the player who
          started that game will start the following game.
        * If a player makes the game stuck, and his/her team loses, then the
          following player (from the other team) will start the following game.

    :param int target_score: score up to which the series will be played;
                             defaults to 200
    :param Domino starting_domino: domino that will determine which player
                                   starts the first game; defaults to [6|6]
    :var games: ordered list of games played in the series
    :var scores: list containing the two teams' scores; team 0 has players 0
                 and 2, and team 1 has players 1 and 3
    :var target_score: score up to which the series will be played
    '''
    def __init__(self, target_score=200, starting_domino=None):
        if starting_domino is None:
            starting_domino = dominoes.Domino(6, 6)

        self.games = [dominoes.Game(starting_domino=starting_domino)]
        self.scores = [0, 0]
        self.target_score = target_score

    def is_over(self):
        '''
        :return: boolean indicating whether either team has
                 reached the target score, thus ending the series
        '''
        return max(self.scores) >= self.target_score

    def next_game(self):
        '''
        Advances the series to the next game, if possible. Also updates
        each team's score with points from the most recently completed game.

        :return: the next game, if the previous game did not end the series;
                 None otherwise
        :raises SeriesOverException: if the series has already ended
        :raises GameInProgressException: if the last game has not yet finished
        '''
        if self.is_over():
            raise dominoes.SeriesOverException(
                'Cannot start a new game - series ended with a score of {} to {}'.format(*self.scores)
            )

        result = self.games[-1].result
        if result is None:
            raise dominoes.GameInProgressException(
                'Cannot start a new game - the latest one has not finished!'
            )

        # update each team's score with the points from the previous game
        if result.points >= 0:
            self.scores[result.player % 2] += result.points
        else:
            self.scores[(result.player + 1) % 2] -= result.points

        # return None if the series is now over
        if self.is_over():
            return

        # determine the starting player for the next game
        if result.won or result.points > 0:
            starting_player = result.player
        elif not result.points:
            starting_player = self.games[-1].starting_player
        else: # result.points < 0
            starting_player = (result.player + 1) % 4

        # start the next game
        self.games.append(dominoes.Game(starting_player=starting_player))

        return self.games[-1]

    def __str__(self):
        string_list = ['Series to {} points:'.format(self.target_score)]

        for i, score in enumerate(self.scores):
            string_list.append('Team {} has {} points.'.format(i, score))

        return '\n'.join(string_list)

    def __repr__(self):
        return str(self)