from PIL import Image
import streamlit as st
from game import GamePlay, Player, Dealer, Deck

number_of_decks = 8
blackjack_multiplier = 1.5

st.title('Welcome to this Virtual Lucky 8 Blackjack Table!')
st.subheader("You get to start with $1000")

st.divider()

# Initialize session state variables
if 'current_amount' not in st.session_state:
    st.session_state.current_amount = 1000

if 'bet_amount' not in st.session_state:
    st.session_state.bet_amount = 0


if 'last_bet_amount' not in st.session_state:
    st.session_state.last_bet_amount = 0

if 'last_outcome' not in st.session_state:
    st.session_state.last_outcome = 'awaiting game'

if 'last_outcome_score' not in st.session_state:
    st.session_state.last_outcome_score = 0

bet_amounts = [0, 50, 100, 200]
selected_bet_amount = st.selectbox("Select your bet amount", bet_amounts)

if st.session_state.last_outcome == "Win":
    st.session_state.last_outcome_score = 1
if st.session_state.last_outcome == "Loss":
    st.session_state.last_outcome_score = -1
if st.session_state.last_outcome == "Push":
    st.session_state.last_outcome_score = 0


@st.cache_resource()
def start_game():
    game_deck = Deck(number_of_decks)
    dealer = Dealer()
    player = Player()
    game_play = GamePlay(player, dealer, game_deck, blackjack_multiplier, selected_bet_amount)
    return game_deck, dealer, player, game_play


def main():

    game_deck, dealer, player, game_play = start_game()

    if st.button('Play with my bets'):
        game_play.deal_in()
        st.session_state.bet_amount = selected_bet_amount
        st.session_state.current_amount -= selected_bet_amount



    col1, col2, col3 = st.columns(3)
    col1.metric(label="Pockets", value=st.session_state.current_amount, delta=0)
    col2.metric(label="Current Bet", value=st.session_state.bet_amount, delta=st.session_state.bet_amount - st.session_state.last_bet_amount)
    col3.metric(label="Last Outcome", value=st.session_state.last_outcome, delta = st.session_state.last_outcome_score)

    player_stats = st.empty()
    player_images = st.empty()
    player_hit_option = st.empty()
    player_double_down_option = st.empty()
    player_stand_option = st.empty()

    dealer_stats = st.empty()
    dealer_images = st.empty()
    result = st.empty()


    if 'Hit' in player.possible_actions:
        if player_hit_option.button('Hit'):
            player.player_hit(game_deck, game_play)
            if 'Hit' not in player.possible_actions:
                player_hit_option.empty()

    if 'Double Down' in player.possible_actions:
        if player_double_down_option.button('Double Down'):
            player.double_down(game_deck, game_play)
            player_double_down_option.empty()
            player_hit_option.empty()
            player_stand_option.empty()
            
    if 'Stand' in player.possible_actions:
        if player_stand_option.button('Stand'):
            player.stand(game_play)
            player_hit_option.empty()
            player_double_down_option.empty()
            player_stand_option.empty()

    
    game_play.update()
    st.session_state.last_outcome = game_play.player_win

    player_stats.write(player)
    player_images.image([Image.open(card.image_location)
                        for card in player.cards], width=100)

    dealer_stats.write(dealer)
    dealer_images.image([Image.open(card.image_location)
                        for card in dealer.cards], width=100)

    
    result.write(game_play)


if __name__ == "__main__":
    main()