import random 

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

        if self.rank == 1:
            self.card_scores = [1, 11]
        elif self.rank >= 11 and self.rank <= 14:
            self.card_scores = [10, 10]
        else:
            self.card_scores = [self.rank, self.rank]


        if self.rank == 1:
            self.short_rank = 'ace'
        elif self.rank == 11:
            self.short_rank = 'jack'
        elif self.rank == 12:
            self.short_rank = 'queen'
        elif self.rank == 13:
            self.short_rank = 'king'
        else:
            self.short_rank = str(self.rank)


        if self.suit == 'Spades':
            self.short_suit = 'spades'
        elif self.suit == 'Hearts':
            self.short_suit = 'hearts'
        elif self.suit == 'Clubs':
            self.short_suit = 'clubs'
        else:
            self.short_suit = 'diamonds'
        
        #9_of_spades.png
        self.image_location = 'card_images/{}_of_{}.png'.format(self.short_rank, self.short_suit)

        
    def __repr__(self):
        if self.rank == 1:
            true_rank = 'Ace'
        elif self.rank == 11:
            true_rank = 'Jack'
        elif self.rank == 12:
            true_rank = 'Queen'
        elif self.rank == 13:
            true_rank = 'King'
        else:
            true_rank = str(self.rank)
        return '{} of {}'.format(true_rank, self.suit)
    
    def get_number(self, rank):
        if self.rank == 1:
            number = 1
        elif self.rank == 11:
            number = 10
        elif self.rank == 12:
            number = 10
        elif self.rank == 13:
            number = 10
        else:
            number = self.rank
        return number



suits = ('Spades', 'Hearts', 'Clubs', 'Diamonds')

class Deck:
    def __init__(self, number_of_decks):
        self.number_of_decks = number_of_decks
        self.cards = []
        self.create(self.number_of_decks)
    
    def __repr__(self):
        return 'Game deck has {} cards remaining'.format(len(self.cards))

    def create(self, number_of_decks):
        decks = [Card(rank, suit) for suit in suits for rank in range(1, 14) for deck in 
                    range(number_of_decks)]
        decks = random.sample(decks, len(decks))
        self.cards.extend(decks)

    def draw(self):
        drawn_card = self.cards[0]
        self.cards.remove(self.cards[0])
        return drawn_card
    
    def reset(self):
        self.cards = []
        self.create(self.number_of_decks)


class Dealer:
    def __init__(self):
        self.cards = []
        self.hand_scores = [0, 0]
        self.best_outcome = 'Awaiting deal'
        self.card_scores = [0, 0]
    
    def __repr__(self):
        return 'Dealer Hand: {}, Scores: {}, Best Outcome: {}'.format(self.cards, list(set(self.hand_scores)), self.best_outcome)

    def hit(self, game_deck):
        draw_card = game_deck.draw()
        self.cards.append(draw_card)
        card_scores = draw_card.card_scores
        self.card_scores = card_scores
        self.hand_scores = [a + b for a, b in zip(self.hand_scores, card_scores)]

        if len(self.cards) <= 1:
            self.best_outcome = 'Awaiting Deal'

        elif 21 in self.hand_scores and len(self.cards) == 2:
            self.best_outcome = 'Blackjack'

        elif self.hand_scores[0] > 21 and self.hand_scores[1] > 21:
            self.best_outcome = 'Bust'
        
        else:
            self.best_outcome = max([i for i in self.hand_scores if i <= 21])

    def reset(self):
        self.cards.clear()
        self.hand_scores = [0, 0]
        self.best_outcome = 'Awaiting Deal'


class Player:
    def __init__(self):
        self.cards = []
        self.hand_scores = [0, 0]
        self.best_outcome = 'Awaiting deal'
        self.possible_actions = ['No deal yet']
        self.doubled_down = 'No'
        self.card_scores = [0, 0]
    
    def __repr__(self):
        return 'Player Hand: {}, Scores: {}, Best Outcome: {}'.format(self.cards, list(set(self.hand_scores)),
                    self.best_outcome)

    def hit(self, game_deck):
        draw_card = game_deck.draw()
        self.cards.append(draw_card)
        card_scores = draw_card.card_scores
        self.card_scores = card_scores
        self.hand_scores = [a + b for a, b in zip(self.hand_scores, card_scores)]

        if len(self.cards) <= 1:
            self.best_outcome = 'Awaiting Deal'

        elif 21 in self.hand_scores and len(self.cards) == 2:
            self.best_outcome = 'Blackjack'

        elif self.hand_scores[0] > 21 and self.hand_scores[1] > 21:
            self.best_outcome = 'Bust'

        else:
            self.best_outcome = max([i for i in self.hand_scores if i <= 21])

    
    def stand(self, game_play):
        self.possible_actions = []
        game_play.commentary = 'Player is standing'

    
    def double_down(self, game_deck, game_play):
        self.hit(game_deck)
        game_play.commentary = 'Player is doubling down'
        self.doubled_down = 'Yes'
        self.possible_actions = []

    def split(self, game_deck, game_play):
        game_play.commentary = 'Player is splitting'
        split_card = self.cards.pop(1)
        new_hand = Player()
        new_hand.cards.append(split_card)

        self.get_possibilities(game_play)
        return new_hand
    
    def player_hit(self, game_deck, game_play):
        self.hit(game_deck)
        game_play.commentary = 'Player has hit'
        self.get_possibilities(game_play)
    
    def get_possibilities(self, game_play):
        if self.best_outcome in ['Blackjack', 'Bust', 21]:
            self.possible_actions = []
            game_play.commentary = 'Player has no more options'
        
        elif len(self.cards) == 2 and self.cards[0].get_number(self.cards[0].rank) == self.cards[1].get_number(self.cards[1].rank):
            self.possible_actions = ['Hit', 'Stand', 'Double Down', 'Split']
            game_play.commentary = 'Player can still hit, split, double down, or stand'
        
        elif len(self.cards) == 2:
            self.possible_actions = ['Hit', 'Stand', 'Double Down']
            game_play.commentary = 'Player can still hit, double down, or stand'

        else:
            self.possible_actions = ['Hit', 'Stand']
            game_play.commentary = 'Player can still hit or stand'

    def reset(self):
        self.cards = []
        self.hand_scores = [0, 0]
        self.best_outcome = 'Awaiting deal'
        self.possible_actions = []


class GamePlay:
    def __init__(self, player, dealer, game_deck, blackjack_multiplier, bet_amount: int):
        self.player = player
        self.dealer = dealer
        self.game_deck = game_deck 
        self.blackjack_multiplier = blackjack_multiplier 
        self.initial_bet_amount = bet_amount
        self.commentary = ""
        self.player_win = "Game"
        self.player_win_amount = 0
        self.is_game_over = False

    
    def dealer_turn(self):
        
        if self.dealer.hand_scores[0] >= 17 and self.dealer.hand_scores[1] >= 17:
            self.commentary = 'Dealer hand has reached 17. Dealer cannot hit anymore'
            return
    
        elif self.player.best_outcome == 'Awaiting Deal':
            self.commentary = 'Player has not been dealt yet. Dealer does not take any action.'
            return

        elif self.player.best_outcome == 'Bust':
            self.commentary = 'Player is Bust. Dealer does not take any action.'
            return
        
        while True:
            self.dealer.hit(self.game_deck)

            if self.dealer.best_outcome == 'Blackjack':
                self.commentary = 'Dealer hit Blackjack'
                break  # Exit the loop if the dealer gets Blackjack

            elif self.dealer.best_outcome == 'Bust':
                self.commentary = 'Dealer went Bust'
                break  # Exit the loop if the dealer goes Bust

            elif int(self.dealer.best_outcome) < 17:
                self.commentary = 'Dealer has {}, Dealer has to hit'.format(self.dealer.best_outcome)

            elif int(self.dealer.best_outcome) == 17 and 1 in [card.rank for card in self.dealer.cards]:
                self.commentary = 'Dealer has a soft 17, Dealer has to hit'
            
            elif int(self.dealer.best_outcome) >= 17:
                self.commentary = 'Dealer reached the limit. Dealer can no longer hit.'
                break

            else:
                self.commentary = 'Dealer is proceeding with {}'.format(self.dealer.best_outcome)

    def check_game_over(self):
        if len(self.player.possible_actions) == 0:
           self.is_game_over = True
        else:
           self.is_game_over = False
        return self.is_game_over

    def update(self):

        if len(self.player.possible_actions) == 0:
            if self.player.best_outcome == 'Bust' and self.player.doubled_down == 'Yes':
                    self.commentary = "Player busted. Player loses ${}".format(str(self.initial_bet_amount * 2))
                    self.player_win = "Loss"

            elif self.player.best_outcome == 'Bust':
                    self.commentary = "Player busted. Player loses ${}".format(str(self.initial_bet_amount))
                    self.player_win = "Loss"

            elif self.player.best_outcome == 'Blackjack' and self.dealer.cards[0].rank not in [1, 10]:
                self.commentary = "Player has Blackjack. Dealer has no chance to hit Blackjack. Player wins ${} dollars!".format(
                    str(self.blackjack_multiplier * self.initial_bet_amount))
                self.player_win = "Blackjack"
                self.player_win_amount = self.blackjack_multiplier * self.initial_bet_amount

            else:
                self.commentary = "Dealer turn can proceed as normal"
                self.dealer_turn()

                if self.dealer.best_outcome == 'Bust':
                    self.commentary = "Dealer busted. Player wins ${}".format(str(self.initial_bet_amount))
                    self.player_win = "Win"
                    self.player_win_amount = self.initial_bet_amount
                
                elif self.dealer.best_outcome == 'Bust' and self.player.doubled_down == 'Yes':
                    self.commentary = "Dealer busted. Player wins ${}".format(str(self.initial_bet_amount * 2))
                    self.player_win = "Win"
                    self.player_win_amount = self.initial_bet_amount

                elif self.dealer.best_outcome == 'Blackjack' and self.player.best_outcome == 'Blackjack':
                    self.commentary = "Dealer and Player both have Blackjack. Player takes back ${}".format(str(self.initial_bet_amount))
                    self.player_win = "Push"

                elif self.dealer.best_outcome == 'Blackjack' and self.player.best_outcome != 'Blackjack':
                    self.commentary = "Dealer has Blackjack. Player loses ${}".format(str(self.initial_bet_amount))
                    self.player_win = "Loss"

                elif self.dealer.best_outcome == 'Blackjack' and self.player.best_outcome != 'Blackjack' and self.player_doubled_down == 'Yes':
                    self.commentary = "Dealer has Blackjack. Player loses ${}".format(str(self.initial_bet_amount * 2))
                    self.player_win = "Loss"

                elif self.dealer.best_outcome != 'Blackjack' and self.player.best_outcome == 'Blackjack':
                    self.commentary = "Player has Blackjack. Player wins {} times their initial bet".format(
                        str(self.blackjack_multiplier * self.initial_bet_amount))
                    self.player_win = "Blackjack"
                    self.player_win_amount = self.blackjack_multiplier * self.initial_bet_amount

                elif int(self.dealer.best_outcome) == int(self.player.best_outcome):
                    self.commentary = "Dealer and Player have same score. Player takes back ${}".format(str(self.initial_bet_amount))
                    self.player_win = "Push"

                elif int(self.dealer.best_outcome) > int(self.player.best_outcome):
                    self.commentary = "Dealer has {} whereas Player has {}. Player loses ${}".format(
                        str(self.dealer.best_outcome), str(self.player.best_outcome), str(self.initial_bet_amount))
                    self.player_win = "Loss"

                
                elif int(self.dealer.best_outcome) > int(self.player.best_outcome) and self.player_doubled_down == 'Yes':
                    self.commentary = "Dealer has {} whereas Player has {}. Player loses ${}".format(
                        str(self.dealer.best_outcome), str(self.player.best_outcome), str(self.initial_bet_amount * 2))
                    self.player_win = "Loss"

                elif int(self.dealer.best_outcome) < int(self.player.best_outcome):
                    self.commentary = "Dealer has {} whereas Player has {}. Player wins ${}".format(
                        str(self.dealer.best_outcome), str(self.player.best_outcome), str(self.initial_bet_amount))
                    self.player_win = "Win"
                    self.player_win_amount = self.initial_bet_amount
                
                elif int(self.dealer.best_outcome) < int(self.player.best_outcome) and self.player_doubled_down == 'Yes':
                    self.commentary = "Dealer has {} whereas Player has {}. Player wins ${}".format(
                        str(self.dealer.best_outcome), str(self.player.best_outcome), str(self.initial_bet_amount * 2))
                    self.player_win = "Win"
                    self.player_win_amount = self.initial_bet_amount
                
        else:
            pass

    def reset(self):
        self.commentary = " "
        self.player_win_amount = 0
        self.is_game_over = False
        self.player_win = "Game"
        

    def deal_in(self):
        self.dealer.reset()
        self.player.reset()
        self.game_deck.reset()

        self.reset()

        self.player.player_hit(self.game_deck, self)
        self.dealer.hit(self.game_deck)
        
        self.player.player_hit(self.game_deck, self)
        self.player.get_possibilities(self)
        
