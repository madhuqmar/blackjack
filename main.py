import streamlit as st
from game import GamePlay, Player, Dealer, Deck
from PIL import Image


st.set_page_config(layout="wide")

number_of_decks = 8
blackjack_multiplier = 1.5

st.title('Welcome to this Virtual Lucky 8 Blackjack Table!')
st.subheader("You get to start with $1000")

st.divider()

def update_metrics(metrics, current_amount, bet_amount, last_bet_amount, last_outcome, last_outcome_score):
    metrics.empty()
    with metrics:
        col1, col2, col3 = st.columns(3)
        col1.metric(label="Pockets", value=f"${current_amount:,.2f}", delta=0)
        col2.metric(label="Current Bet", value=f"${bet_amount:,.2f}", delta=bet_amount - last_bet_amount)
        col3.metric(label="Last Outcome", value=last_outcome, delta=last_outcome_score)

@st.cache_resource()
def start_game(bet_amount):
    game_deck = Deck(number_of_decks)
    dealer = Dealer()
    player = Player()
    game_play = GamePlay(player, dealer, game_deck, blackjack_multiplier, bet_amount)
    return game_deck, dealer, player, game_play

@st.cache_resource()
def start_split_game(_new_hand, _game_play, _bet_amount):
    dealer = _game_play.dealer
    game_deck = _game_play.game_deck
    blackjack_multiplier = _game_play.blackjack_multiplier
    split_game = GamePlay(_new_hand, dealer, game_deck, blackjack_multiplier, _bet_amount)
    return split_game
    
split_game_player = None

maincol1, maincol2, maincol3 = st.columns(3)

with maincol1:

    ### TRACKING PLAYER POCKETS ###
    if 'current_amount' not in st.session_state:  # if game not started
        st.session_state.current_amount = 1000

    ### TRACKING BET AMOUNTS ###
    bet_amounts = [0, 25, 50, 100, 200]
    selected_bet_amount = st.selectbox("Select your bet amount", bet_amounts)

    if 'last_bet_amount' not in st.session_state:
        st.session_state.last_bet_amount = 0

    ### TRACKING PLAYER GAME OUTCOMES ###
    if 'last_outcome' not in st.session_state:
        st.session_state.last_outcome = 'Start'

    if 'last_outcome_score' not in st.session_state:
        st.session_state.last_outcome_score = 0

    ### TRACK GAME STATUS ###
    if 'game_finished' not in st.session_state:
        st.session_state.game_finished = False

    if 'game_started' not in st.session_state:
        st.session_state.game_started = False

    ## INITIALIZE GAME ###
    st.session_state.bet_amount = selected_bet_amount
    game_deck, dealer, player, game_play = start_game(st.session_state.bet_amount)

    if st.button('Play with my bets'):
        st.success("Bets placed!")
        st.session_state.game_finished = False
        st.session_state.game_started = True

        if selected_bet_amount:
            st.session_state.bet_amount = selected_bet_amount
            game_deck, dealer, player, game_play = start_game(st.session_state.bet_amount)
            game_play.deal_in()
            st.session_state.current_amount -= st.session_state.bet_amount
            if 'split' in st.session_state:
                st.session_state.split = False

    ## CHECK FOR SPLIT GAME ###
    if 'split' not in st.session_state:
        st.session_state.split = False

    if 'split_game_player' not in st.session_state:
        st.session_state.split_game_player = False

    col1, col2, col3 = st.columns(3)

    metrics = st.empty()
    update_metrics(metrics, current_amount=st.session_state.current_amount, 
                                    bet_amount=st.session_state.bet_amount, 
                                    last_bet_amount=st.session_state.last_bet_amount, 
                                    last_outcome=st.session_state.last_outcome, 
                                    last_outcome_score=st.session_state.last_outcome_score)


with maincol2:

    if 'player_cards' not in st.session_state:
        st.session_state.player_cards = []  # Initialize player cards in session state
    if 'dealer_cards' not in st.session_state:
        st.session_state.dealer_cards = []  # Initialize dealer cards in session state

    player_stats = st.empty()
    st.write("**Player Spread**")
    if st.session_state.game_started:
        player_images = st.container()
        player_images.image([Image.open(card.image_location) for card in game_play.player.cards], width=100)

    dealer_stats = st.empty()
    dealer_images = st.empty()

    with dealer_stats.container():
        st.write("**Dealer Spread**")
        if st.session_state.game_started:
            dealer_images.image([Image.open(card.image_location) for card in game_play.dealer.cards], width=100)

    if not st.session_state.game_finished:
        st.write("**Player Options**")
    player_hit_option = st.empty()
    player_double_down_option = st.empty()
    player_split_option = st.empty()
    player_stand_option = st.empty()


    if 'Hit' in player.possible_actions:
        if player_hit_option.button('Hit'):
            player.player_hit(game_deck, game_play)
            player_images.image([Image.open(game_play.player.cards[-1].image_location)], width=100)


            if 'Hit' not in game_play.player.possible_actions:
                player_hit_option.empty()

    if 'Double Down' in player.possible_actions:
        if player_double_down_option.button('Double Down'):
            player.double_down(game_deck, game_play)
            player_images.image([Image.open(card.image_location) for card in game_play.player.cards], width=100)
            st.session_state.current_amount -= st.session_state.bet_amount
            st.session_state.bet_amount = st.session_state.bet_amount * 2

            update_metrics(metrics, current_amount = st.session_state.current_amount, 
                                    bet_amount = st.session_state.bet_amount, 
                                    last_bet_amount = st.session_state.last_bet_amount, 
                                    last_outcome = st.session_state.last_outcome, 
                                    last_outcome_score=st.session_state.last_outcome_score)

        
            player_double_down_option.empty()
            player_hit_option.empty()
            player_stand_option.empty()

    
    if 'Stand' in player.possible_actions:
        if player_stand_option.button('Stand'):
            player.stand(game_play)
            # dealer_images.image([Image.open(card.image_location) for card in game_play.dealer.cards], width=100)
            
            player_hit_option.empty()
            player_double_down_option.empty()
            player_stand_option.empty()


    if 'Split' in player.possible_actions:
        if player_split_option.button('Split'):
            player.split(game_play)
            split_card = player.cards.pop()

            if split_card not in st.session_state:
                st.session_state.split_card = split_card

            st.session_state.split = True
            
            #New hand player init
            new_hand = Player()
            new_hand.cards.append(split_card)
      
            if new_hand not in st.session_state:
                st.session_state.new_hand = new_hand
            
            #Empty split option button
            player_split_option.empty()

            if len(player.cards) < 2:
                player.player_hit(game_deck, game_play)
                player.hand_scores = [0, 0]
                player.hand_scores = [a + b for a, b in zip(player.cards[0].card_scores, player.cards[1].card_scores)]

            player_images.image([Image.open(card.image_location) for card in player.cards], width=100)

            if len(player.cards) <= 1:
                player.best_outcome = 'Awaiting Deal'

            elif 21 in player.hand_scores and len(player.cards) == 2:
                player.best_outcome = 'Blackjack'

            elif player.hand_scores[0] > 21 and player.hand_scores[1] > 21:
                player.best_outcome = 'Bust'

            else:
                player.best_outcome = max([i for i in player.hand_scores if i <= 21])
                
        
            player.get_possibilities(game_play)
           
            if split_game_player is None:
                split_game_player = Player()
                st.session_state.split_game_player == True
                split_game_player.cards = st.session_state.new_hand.cards[:]
                split_game = start_split_game(split_game_player, game_play, st.session_state.bet_amount)
                split_game.player = split_game_player
            
                split_game_player.player_hit(game_deck, split_game)
                split_game_player.hand_scores = [0, 0]
                split_game_player.hand_scores = [a + b for a, b in zip(split_game.player.cards[0].card_scores, split_game.player.cards[1].card_scores)]

            st.session_state.split_game_player = split_game_player
            st.session_state.split_game = split_game

            st.session_state.current_amount -= st.session_state.bet_amount
            st.session_state.bet_amount = st.session_state.bet_amount * 2
            update_metrics(metrics, current_amount = st.session_state.current_amount, 
                                    bet_amount = st.session_state.bet_amount, 
                                    last_bet_amount = st.session_state.last_bet_amount, 
                                    last_outcome = st.session_state.last_outcome, 
                                    last_outcome_score=st.session_state.last_outcome_score)



    ### SPLIT GAME ###

    if st.session_state.split == True:

        st.write("**New Hand After Split**")

        split_game_player = st.session_state.split_game_player
        split_game = st.session_state.split_game

        if len(split_game_player.cards) <= 1:
            split_game_player.best_outcome = 'Awaiting Deal'

        elif 21 in split_game_player.hand_scores and len(split_game_player.cards) == 2:
            split_game_player.best_outcome = 'Blackjack'

        elif split_game_player.hand_scores[0] > 21 and split_game_player.hand_scores[1] > 21:
            split_game_player.best_outcome = 'Bust'

        else:
            split_game_player.best_outcome = max([i for i in split_game_player.hand_scores if i <= 21])

        new_hand_images = st.empty()
        new_hand_images.image([Image.open(card.image_location) for card in split_game_player.cards], width=100)

        new_hand_hit_option = st.empty()
        new_hand_stand_option = st.empty()
        new_hand_double_down_option = st.empty()

        st.write("**New Hand Player Options**")

        split_game_player.get_possibilities(split_game)


        if 'Hit' in split_game_player.possible_actions:
            if new_hand_hit_option.button('Hit 2'):
                split_game_player.player_hit(game_deck, split_game)
                new_hand_images.image([Image.open(card.image_location) for card in split_game_player.cards], width=100)
                if 'Hit' not in split_game.player.possible_actions:
                    new_hand_hit_option.empty()

        if 'Double Down' in split_game_player.possible_actions:
            if new_hand_double_down_option.button('Double Down 2'):
                split_game_player.double_down(game_deck, split_game)

                st.session_state.current_amount -= st.session_state.bet_amount
                st.session_state.bet_amount = st.session_state.bet_amount * 2
                update_metrics(metrics, current_amount = st.session_state.current_amount, 
                                        bet_amount = st.session_state.bet_amount, 
                                        last_bet_amount = st.session_state.last_bet_amount, 
                                        last_outcome = st.session_state.last_outcome, 
                                        last_outcome_score=st.session_state.last_outcome_score)

            
                new_hand_double_down_option.empty()
                new_hand_hit_option.empty()
                new_hand_stand_option.empty()

        if 'Stand' in split_game_player.possible_actions:
            if new_hand_stand_option.button('Stand 2'):
                split_game_player.stand(split_game)

                new_hand_hit_option.empty()
                new_hand_double_down_option.empty()
                new_hand_stand_option.empty()

        dealer_images.empty()
        dealer_stats.empty()

        dealer_stats_new = st.empty()
        with dealer_stats_new.container():
            st.write("**Dealer Spread**")
        dealer_images_new = st.empty()
        dealer_images_new.image([Image.open(card.image_location)
                            for card in dealer.cards], width=100)


        st.session_state.split_game_player = split_game_player
        st.session_state.split_game = split_game

    ### SPLIT GAME END ###

    if st.session_state.split == True:
        if len(player.possible_actions) == 0 and len(split_game_player.possible_actions) == 0:
            game_play.check_game_over()
            game_play.update()
            if game_play.check_game_over():
                st.session_state.game_finished = True

            split_game.check_game_over()
            split_game.update()
            if split_game.check_game_over():
                st.session_state.game_finished = True

            dealer_images_new.image([Image.open(card.image_location) for card in dealer.cards], width=100)
    else:
        game_play.check_game_over()
        if game_play.check_game_over():
            st.session_state.game_finished = True

        game_play.update()
        dealer_images.image([Image.open(card.image_location) for card in dealer.cards], width=100)

with maincol3:
    if st.session_state.split == False:
        result = st.empty()
        result.write(game_play)
    else:
        game1, game2 = st.columns(2)
        with game1:
            result = st.empty()
            result.write(game_play)
        with game2:
            result2 = st.empty()
            result2.write(split_game)


#UPDATE LAST OUTCOME
# if game_play.player_win == "Win" and game_play.player_win == "Yes":
#     st.session_state.last_outcome = "Double Win"
# elif game_play.player_win == "Loss" and game_play.player_win == "No":
#     st.session_state.last_outcome = "Double Loss"
#
# if st.session_state.split == True:
#     if game_play.player_win == "Win" and split_game.player_win == "Win":
#         st.session_state.last_outcome = "Double Win"
#     elif game_play.player_win == "Loss" and split_game.player_win == "Loss":
#         st.session_state.last_outcome = "Double Loss"
#     elif game_play.player_win == "Loss" and split_game.player_win == "Win":
#         st.session_state.last_outcome = "Partial Win"
#     elif game_play.player_win == "Win" and split_game.player_win == "Loss":
#         st.session_state.last_outcome = "Partial Win"
#     elif game_play.player_win == "Loss" and split_game.player_win == "Push":
#         st.session_state.last_outcome = "Partial Loss"
#     elif game_play.player_win == "Push" and split_game.player_win == "Loss":
#         st.session_state.last_outcome = "Partial Loss"
#     else:
#         pass
# else:
#     st.session_state.last_outcome = game_play.player_win

if st.session_state.game_finished:
    if st.session_state.split == True:
        if game_play.player_win == "Win" and split_game.player_win == "Win":
            st.session_state.last_outcome = "Double Win"
        elif game_play.player_win == "Loss" and split_game.player_win == "Loss":
            st.session_state.last_outcome = "Double Loss"
        elif game_play.player_win == "Loss" and split_game.player_win == "Win":
            st.session_state.last_outcome = "Partial Win"
        elif game_play.player_win == "Win" and split_game.player_win == "Loss":
            st.session_state.last_outcome = "Partial Win"
        # Add remaining conditions
    else:
        st.session_state.last_outcome = game_play.player_win


#for bet amount delta
st.session_state.last_bet_amount = game_play.player_win_amount

#for last outcome delta
if st.session_state.last_outcome == "Win":
    st.session_state.last_outcome_score = 1
elif st.session_state.last_outcome == "Double Win":
    st.session_state.last_outcome_score = 2
elif st.session_state.last_outcome == "Double Loss":
    st.session_state.last_outcome == -2
elif st.session_state.last_outcome == "Partial Win":
    st.session_state.last_outcome == 0.5
elif st.session_state.last_outcome == "Partial Loss":
    st.session_state.last_outcome == -0.5
elif st.session_state.last_outcome == "Blackjack":
    st.session_state.last_outcome_score = 1
elif st.session_state.last_outcome == "Loss":
    st.session_state.last_outcome_score = -1
elif st.session_state.last_outcome == "Push":
    st.session_state.last_outcome_score = 0

#UPDATE PLAYER METRICS
if st.session_state.last_outcome == "Win" or st.session_state.last_outcome  == "Blackjack":
    st.session_state.current_amount += st.session_state.bet_amount * blackjack_multiplier
elif st.session_state.last_outcome  == "Push":
    st.session_state.current_amount += st.session_state.bet_amount

update_metrics(metrics, current_amount = st.session_state.current_amount, 
                        bet_amount = st.session_state.bet_amount, 
                        last_bet_amount = st.session_state.last_bet_amount, 
                        last_outcome = st.session_state.last_outcome, 
                        last_outcome_score=st.session_state.last_outcome_score)