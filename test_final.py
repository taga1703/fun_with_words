import streamlit as st
import random
import json
import time


# Initialize session state variables if they don't exist
if 'word_dict' not in st.session_state:
    with open("C:\python\english_words_dictionary.txt", encoding='utf-8') as f:
        data = f.read()
        st.session_state.word_dict = json.loads(data)

if 'game_initialized' not in st.session_state:
    st.session_state.game_initialized = False

if 'max_attempts' not in st.session_state:
    st.session_state.max_attempts = 3

if 'correct_words' not in st.session_state:
    st.session_state.correct_words = set()

if 'current_word' not in st.session_state:
    st.session_state.current_word = None

if 'attempts' not in st.session_state:
    st.session_state.attempts = 0

if 'show_clue' not in st.session_state:
    st.session_state.show_clue = False

if 'first_attempt_success' not in st.session_state:
    st.session_state.first_attempt_success = set()

if 'failed_word' not in st.session_state:
    st.session_state.failed_word = False

if 'player_name' not in st.session_state:
    st.session_state.player_name = ""

if 'player_gender' not in st.session_state:
    st.session_state.player_gender = ""


def initialize_game():
    st.session_state.game_initialized = True
    st.session_state.current_word = get_random_word()
    st.session_state.attempts = 0
    st.session_state.show_clue = False
    st.session_state.failed_word = False


# def get_random_word():
#     available_words = list(
#         set(st.session_state.word_dict.keys())
#         - st.session_state.first_attempt_success
#         - {st.session_state.current_word}
#     )
#     if not available_words:
#         return None
#     return random.choice(available_words)

def get_random_word():
    available_words = list(
        set(st.session_state.word_dict.keys())
        - st.session_state.first_attempt_success
        - {st.session_state.current_word}
    )
    if not available_words:
        return None
    return random.choice(available_words)


def check_synonym(word, user_answer):
    return user_answer.lower().strip() == st.session_state.word_dict[word]


def get_clue(word, attempt):
    # Show more letters with each attempt
    visible_letters = attempt
    result = ''
    for i, char in enumerate(word):
        if i < visible_letters:
            # Show actual character if it's within visible range
            result += char + ' '
        else:
            # Show '-' for spaces, '_' for other characters
            if char == ' ':
                result += '- '
            else:
                result += '_ '
    return result.strip()


# Main app
# Initial setup if game not initialized
if not st.session_state.game_initialized:
    st.write("ברוך הבא! בואו נתחיל לשחק")

    # Name input
    name = st.text_input("מה השם שלך?")

    # Gender selection
    gender = st.radio("אתה/את:", options=["בן", "בת"])

    st.write("כמה נסיונות תרצה לקבל לכל מילה?")

    col1, col2 = st.columns([2, 1])
    with col1:
        attempts = st.slider("מספר נסיונות:", min_value=2, max_value=4, value=3)
    with col2:
        if st.button("התחל משחק!"):
            # Validate inputs
            if not name:
                st.error("אנא הזן את שמך")
            else:
                # Store name and gender in session state
                st.session_state.player_name = name
                st.session_state.player_gender = gender
                st.session_state.max_attempts = attempts
                initialize_game()
                st.rerun()

elif st.session_state.current_word is not None:
    # Modify the title to use name and gender-specific greeting
    name = st.session_state.player_name
    greeting = f"{name}, {'בואי' if st.session_state.player_gender == 'בת' else 'בוא'} ונלמד אנגלית"
    st.title(f"🎉{greeting}🎉")

    lets_go = f"{'נסי' if st.session_state.player_gender == 'בת' else 'נסה'} לכתוב את המילה באנגלית"
    st.write(f"{lets_go}")
    st.write(f"## המילה היא: {st.session_state.current_word}")
    # st.write("נסה לכתוב את המילה המתאימה באנגלית")
    # st.write(f"## המילה היא: {st.session_state.current_word}")

    # Show clue based on number of attempts
    if st.session_state.show_clue and st.session_state.attempts > 0:
        correct_synonym = st.session_state.word_dict[st.session_state.current_word]
        clue = get_clue(correct_synonym, st.session_state.attempts)
        st.write("הנה רמז:")
        st.write(f"**{clue}**")

    # Only show input and check button if we haven't failed all attempts
    if not st.session_state.failed_word:
        user_answer = st.text_input("כתבו את המילה באנגלית:", key="synonym_input")
        if st.button("לחצו כדי לבדוק את התשובה"):
            if user_answer:
                if check_synonym(st.session_state.current_word, user_answer):
                    st.success("🎉 מעולהההההה")
                    st.balloons()

                    if st.session_state.attempts == 0:
                        st.session_state.first_attempt_success.add(st.session_state.current_word)

                    # Add a small delay before moving to the next word
                    time.sleep(1)

                    new_word = get_random_word()
                    if new_word:
                        st.session_state.current_word = new_word
                        st.session_state.attempts = 0
                        st.session_state.show_clue = False
                        st.session_state.failed_word = False
                        st.rerun()
                    else:
                        st.session_state.current_word = None
                        st.rerun()
                else:
                    st.session_state.attempts += 1
                    if st.session_state.attempts >= st.session_state.max_attempts:
                        st.error(
                            f"מצטערת, התשובה הנכונה היא: {st.session_state.word_dict[st.session_state.current_word]}")
                        st.session_state.failed_word = True
                    else:
                        st.session_state.show_clue = True
                        st.error(
                            f"מצטערת, התשובה לא נכונה. נסיון {st.session_state.attempts} מתוך {st.session_state.max_attempts}")
                    st.rerun()
    else:
        st.write(f"התשובה הנכונה היא: {st.session_state.word_dict[st.session_state.current_word]}")

    # if st.button("אני רוצה לנסות מילה אחרת"):
    #     new_word = get_random_word()
    #     if new_word:
    #         st.session_state.current_word = new_word
    #         st.session_state.attempts = 0
    #         st.session_state.show_clue = False
    #         st.session_state.failed_word = False
    #         st.rerun()

    if st.button("אני רוצה לנסות מילה אחרת"):
        new_word = get_random_word()
        if new_word:
            st.session_state.current_word = new_word
            st.session_state.attempts = 0
            st.session_state.show_clue = False
            st.session_state.failed_word = False
            st.rerun()
        else:
            # This means no more available words
            st.warning("זו המילה האחרונה! אנא נסה לענות על המילה הנוכחית.")

    # Show progress
    total_words = len(st.session_state.word_dict)
    correct_first_attempt = len(st.session_state.first_attempt_success)
    st.write(f"התקדמות: {correct_first_attempt}/{total_words} נכונות בנסיון ראשון")

# else:
#     if len(st.session_state.first_attempt_success) == len(st.session_state.word_dict):
#         st.success(f"כל הכבוד!!! סיימת את כל המילים שברשימה 🎉")
#         if st.button("Start Over"):
#             st.session_state.game_initialized = False
#             st.session_state.first_attempt_success = set()
#             st.rerun()
else:
    if len(st.session_state.first_attempt_success) == len(st.session_state.word_dict):
        # Use larger heading and include user's name
        st.markdown(f"# 🎉!!! כל הכבוד, {st.session_state.player_name} 🎉")
        st.markdown(f"## סיימת את כל המילים שברשימה")

        # Add a very big smiley
        st.markdown("<h1 style='text-align: center; font-size: 200px;'>😄</h1>", unsafe_allow_html=True)

        if st.button("Start Over"):
            st.session_state.game_initialized = False
            st.session_state.first_attempt_success = set()
            st.rerun()