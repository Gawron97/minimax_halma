
class Player:
    def __init__(self, player_number, actual_strategy = "rand", second_strategy = None, third_strategy = None) -> None:
        self.player_number = player_number
        self.actual_strategy = actual_strategy
        self.playing_time = 0.0
        self.strategies = []
        self.set_strategies(second_strategy, third_strategy)
        self.index = 0

    def set_strategies(self, second_strategy, third_strategy):
        self.strategies.append(self.actual_strategy)
        if(second_strategy):
            self.strategies.append(second_strategy)
        if(third_strategy):
            self.strategies.append(third_strategy)


    def update_actual_strategy(self):
        self.index += 1
        if(self.index >= len(self.strategies)):
            self.index = 0
        self.actual_strategy = self.strategies[self.index]