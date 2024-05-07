

class Player:
    def __init__(self, player_number, actual_strategy = ("rand", 50, 20), second_strategy = None, third_strategy = None) -> None:
        self.player_number = player_number
        self.actual_strategy = actual_strategy[0]
        self.playing_time = 0.0
        self.strategies = []
        self.set_strategies(actual_strategy, second_strategy, third_strategy)
        self.index = 0
        self.isWin = False
        self.strategy_ratio = actual_strategy[1]
        self.counter = actual_strategy[2]

    def set_strategies(self, first_strategy, second_strategy, third_strategy):
        self.strategies.append(first_strategy)
        if(second_strategy):
            self.strategies.append(second_strategy)
        if(third_strategy):
            self.strategies.append(third_strategy)

    def update_strategy(self):
        self.counter -= 1
        if(self.counter == 0):
            self.index += 1
            if(self.index >= len(self.strategies)):
                self.index = 0
            self.actual_strategy = self.strategies[self.index][0]
            self.strategy_ratio = self.strategies[self.index][1]
            self.counter = self.strategies[self.index][2]

    def update_actual_strategy(self):
        self.index += 1
        if(self.index >= len(self.strategies)):
            self.index = 0
        self.actual_strategy = self.strategies[self.index][0]
        self.strategy_ratio = self.strategies[self.index][1]