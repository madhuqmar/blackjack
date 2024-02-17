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

    ## INITIALIZE GAME ###
    st.session_state.bet_amount = selected_bet_amount
    game_deck, dealer, player, game_play = start_game(st.session_state.bet_amount)

    if st.button('Play with my bets'):

        st.success("Button clicked!")

        if selected_bet_amount:
            st.session_state.bet_amount = selected_bet_amount
            game_deck, dealer, player, game_play = start_game(st.session_state.bet_amount)
            game_play.deal_in()
            st.session_state.current_amount -= st.session_state.bet_amount




    col1, col2, col3 = st.columns(3)

    metrics = st.empty()
    update_metrics(metrics, current_amount=st.session_state.current_amount, 
                                    bet_amount=st.session_state.bet_amount, 
                                    last_bet_amount=st.session_state.last_bet_amount, 
                                    last_outcome=st.session_state.last_outcome, 
                                    last_outcome_score=st.session_state.last_outcome_score)


    # col1.metric(label="Pockets", value=f"${st.session_state.current_amount:,.2f}", delta=0)
    # col2.metric(label="Current Bet", value=f"${st.session_state.bet_amount:,.2f}", delta=st.session_state.bet_amount - st.session_state.last_bet_amount)
    # col3.metric(label="Last Outcome", value=st.session_state.last_outcome, delta=st.session_state.last_outcome_score)

with maincol2:

    st.write("**Player Spread**")
    player_stats = st.empty()
    player_images = st.empty()

    player_hit_option = st.empty()
    player_double_down_option = st.empty()
    player_split_option = st.empty()
    player_stand_option = st.empty()

    
    dealer_stats = st.empty()
    dealer_images = st.empty()
    dealer_stats.write("**Dealer Spread**")
    


    #WRITE GAME PLAY RESULTS
    # player_stats.write(player)
    player_images.image([Image.open(card.image_location)
                        for card in player.cards], width=100)

    # dealer_stats.write(dealer)
    dealer_images.image([Image.open(card.image_location)
                        for card in dealer.cards], width=100)


    player_hit_option, player_double_down_option, player_split_option, player_stand_option = st.columns([1, 1.1, 1.2, 1.3])

    if 'Hit' in player.possible_actions:
        if player_hit_option.button('Hit'):
                player.player_hit(game_deck, game_play)
                if 'Hit' not in player.possible_actions:
                    player_hit_option.empty()

    if 'Double Down' in player.possible_actions:
        if player_double_down_option.button('Double Down'):
                player.double_down(game_deck, game_play)
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

    if 'Split' in player.possible_actions:
        if player_split_option.button('Split'):
            # player_images = st.empty()
            
            # Split the player's hand
            new_hand = player.split(game_deck, game_play)
            
            # Display the cards of the original hand
            player_images.image([Image.open(card.image_location) for card in player.cards], width=100)

            # Display the cards of the new hand
            st.write("**New Hand After Split**")
            new_hand_images = st.empty()
            new_hand_images.image([Image.open(card.image_location) for card in new_hand.cards], width=100)


            # Empty the split button
            player_split_option.empty()


            dealer_images.empty()
            dealer_stats.empty()

            dealer_stats_new = st.empty()
            dealer_stats_new.write("**Dealer Spread**")
            dealer_images_new = st.empty()
            dealer_images_new.image([Image.open(card.image_location)
                                for card in dealer.cards], width=100)

            new_hand_hit_option, new_hand_double_down_option, new_hand_stand_option = st.columns([1, 1.1, 1.2])
            if 'Hit' in new_hand.possible_actions:
                if new_hand_hit_option.button('Hit'):
                        new_hand.player_hit(game_deck, game_play)
                        if 'Hit' not in new_hand.possible_actions:
                            new_handr_hit_option.empty()

            if 'Double Down' in new_hand.possible_actions:
                if new_hand_double_down_option.button('Double Down'):
                        new_hand.double_down(game_deck, game_play)
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

            if 'Stand' in new_hand.possible_actions:
                if new_hand_stand_option.button('Stand'):
                        new_hand.stand(game_play)
                        new_hand_hit_option.empty()
                        new_hand_double_down_option.empty()
                        new_hand_stand_option.empty()

            
    if 'Stand' in player.possible_actions:
        if player_stand_option.button('Stand'):
                player.stand(game_play)
                player_hit_option.empty()
                player_double_down_option.empty()
                player_stand_option.empty()



    game_play.check_game_over()
    game_play.update()




with maincol3:
    result = st.empty()
    result.write(game_play)

#for last outcome
st.session_state.last_outcome = game_play.player_win

#for bet amount delta
st.session_state.last_bet_amount = game_play.player_win_amount

#for last outcome delta
if st.session_state.last_outcome == "Win":
    st.session_state.last_outcome_score = 1
if st.session_state.last_outcome == "Blackjack":
    st.session_state.last_outcome_score = 1
elif st.session_state.last_outcome == "Loss":
    st.session_state.last_outcome_score = -1
elif st.session_state.last_outcome == "Push":
    st.session_state.last_outcome_score = 0

#UPDATE PLAYER METRICS
#for pocketing
if st.session_state.last_outcome == "Win" or st.session_state.last_outcome  == "Blackjack":
    st.session_state.current_amount += st.session_state.bet_amount * blackjack_multiplier
elif st.session_state.last_outcome  == "Push":
    st.session_state.current_amount += st.session_state.bet_amount

update_metrics(metrics, current_amount = st.session_state.current_amount, 
                        bet_amount = st.session_state.bet_amount, 
                        last_bet_amount = st.session_state.last_bet_amount, 
                        last_outcome = st.session_state.last_outcome, 
                        last_outcome_score=st.session_state.last_outcome_score)


# if __name__ == "__main__":
#     main()
