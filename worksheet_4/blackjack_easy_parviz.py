import random


class Blackjack:
    def __init__(self):
        self.player_hand = []
        self.dealer_hand = []

    def reset(self):
        self.player_hand = self.draw_hand()
        self.dealer_hand = self.draw_hand()
        return self.get_state()

    def draw_card(self):
        return random.choice(range(1, 11))

    def draw_hand(self):
        return [self.draw_card(), self.draw_card()]

    def get_state(self):
        return sum(self.player_hand), self.dealer_hand[0], self.is_usable_ace(self.player_hand)

    def is_usable_ace(self, hand):
        return 1 in hand and sum(hand) + 10 <= 21

    def step(self, action):
        if action == 0:  # Stick
            return self.play_dealer()

        if action == 1:  # Hit
            self.player_hand.append(self.draw_card())
            if sum(self.player_hand) > 21:
                return self.get_state(), -1, True  # Player bust
            else:
                return self.get_state(), 0, False

    def play_dealer(self):
        while sum(self.dealer_hand) < 17:
            self.dealer_hand.append(self.draw_card())

        player_score = sum(self.player_hand)
        dealer_score = sum(self.dealer_hand)

        if dealer_score > 21 or player_score > dealer_score:
            return self.get_state(), 1, True
        elif player_score == dealer_score:
            return self.get_state(), 0, True
        else:
            return self.get_state(), -1, True


def human_play(env):
    state = env.reset()
    done = False

    while not done:
        print(f'State: {state}')
        print(f"Dealer's hand: {env.dealer_hand}")
        action = int(input('Enter action (0: Stick, 1: Hit): '))
        state, reward, done = env.step(action)

    print(f'Result: {reward}')


if __name__ == '__main__':
    env = Blackjack()
    human_play(env)
