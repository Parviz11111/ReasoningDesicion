import random


class Blackjack:
    def __init__(self, decks=1):
        self.decks = decks
        self.cards = self.initialize_deck(decks)
        self.player_hand = []
        self.dealer_hand = []

    def initialize_deck(self, decks):
        ranks = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]  # 2-10, J, Q, K are worth 10
        suits = 4  # Number of suits in a deck
        deck = ranks * suits
        deck += [11]  # Ace is initially worth 11
        full_deck = deck * decks
        random.shuffle(full_deck)
        return full_deck

    def reset(self):
        if len(self.cards) < 15:  # Reinitialize if fewer than 15 cards left
            self.cards = self.initialize_deck(self.decks)
        self.player_hand = self.draw_hand()
        self.dealer_hand = self.draw_hand()
        return self.get_state()

    def draw_card(self):
        return self.cards.pop()

    def draw_hand(self):
        return [self.draw_card(), self.draw_card()]

    def get_state(self):
        return self.calculate_hand_value(self.player_hand), self.dealer_hand[0], self.has_usable_ace(self.player_hand)

    def has_usable_ace(self, hand):
        return 11 in hand and self.calculate_hand_value(hand) <= 21

    def calculate_hand_value(self, hand):
        value = sum(hand)
        if value > 21 and self.has_usable_ace(hand):
            value -= 10
        return value

    def step(self, action):
        if action == 0:  # Stick
            return self.play_dealer()

        if action == 1:  # Hit
            self.player_hand.append(self.draw_card())
            if self.calculate_hand_value(self.player_hand) > 21:
                return self.get_state(), -1, True  # Player bust
            else:
                return self.get_state(), 0, False

    def play_dealer(self):
        while self.calculate_hand_value(self.dealer_hand) < 17:
            self.dealer_hand.append(self.draw_card())

        player_score = self.calculate_hand_value(self.player_hand)
        dealer_score = self.calculate_hand_value(self.dealer_hand)

        if dealer_score > 21 or player_score > dealer_score:
            return self.get_state(), 1, True
        elif player_score == dealer_score:
            return self.get_state(), 0, True
        else:
            return self.get_state(), -1, True


def play(env):
    state = env.reset()
    done = False

    while not done:
        print(f'Player state: {state}')
        action = int(input('Enter action (0: Stick, 1: Hit): '))
        state, reward, done = env.step(action)

    print(f'Result: {reward}')


if __name__ == '__main__':
    blackjack_env = Blackjack()
    play(blackjack_env)
