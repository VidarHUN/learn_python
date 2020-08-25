# Write your code here
import random


class RockPaperScissors:
    FILE_NAME = 'rating.txt'
    DRAW_POINTS = 50
    WIN_POINTS = 100

    def __init__(self):
        self.player_name = None
        self.ratings = {}
        self.load_ratings()
        self.rules = []

    def load_ratings(self):
        with open(RockPaperScissors.FILE_NAME) as file_rating:
            for line in file_rating:
                player_name, score = line.split(sep=" ", maxsplit=1)
                self.ratings[player_name] = int(score)

    def ask_for_name(self):
        self.player_name = input('Enter your name:')
        if self.player_name not in self.ratings:
            self.ratings[self.player_name] = 0

    def greetings(self):
        print("Hello, %s" % self.player_name)

    def print_rating(self):
        score = self.ratings[self.player_name]
        print("Your rating: %s" % score)

    def add_score(self, points):
        self.ratings[self.player_name] += points

    def play_round(self, option):
        if option not in self.rules:
            print('Invalid input')
            return

        computer_selection = random.choice(self.rules)

        if option == computer_selection:
            print('There is a draw (%s)' % option)
            self.add_score(RockPaperScissors.DRAW_POINTS)
        elif self.is_option_winner(option, computer_selection):
            print('Well done. Computer chose %s and failed' % computer_selection)
            self.add_score(RockPaperScissors.WIN_POINTS)
        else:
            print('Sorry, but computer chose %s' % computer_selection)

    def save_ratings(self):
        with open(RockPaperScissors.FILE_NAME, 'w') as file_rating:
            for key, value in self.ratings.items():
                print(key, value, file=file_rating)

    def ask_for_rules(self):
        rules = input()
        if not rules:
            rules = 'rock,paper,scissors'
        self.rules = rules.split(sep=',')

        print("Okay, let's start")

    def is_option_winner(self, option, computer_selection):
        index_to = self.rules.index(option)
        index_from = index_to + 1
        elements_after = self.rules[index_from:]
        elements_before = self.rules[:index_to]
        elements = elements_after + elements_before

        half = len(elements) // 2
        beating_to_option = elements[:half]
        return computer_selection not in beating_to_option

    def play(self):
        self.ask_for_name()
        self.greetings()
        self.ask_for_rules()

        while True:
            option = input()

            if option == '!exit':
                break

            if option == '!rating':
                self.print_rating()
            else:
                self.play_round(option)

        print('Bye!')
        self.save_ratings()


game = RockPaperScissors()
game.play()
