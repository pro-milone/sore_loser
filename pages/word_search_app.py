import streamlit as st
from word_search import find_words_in_grid
from utils import Board
import os

def app():
    st.header("Word Search Grid Solver")

    # Load words.txt from repo
    words_file = "words.txt"
    words = []
    if os.path.exists(words_file):
        with open(words_file, "r", encoding="utf-8") as f:
            words = [line.strip().lower() for line in f if line.strip()]
            words = [w for w in words if w.isalpha()]
        st.success(f"Loaded {len(words)} words from {words_file}.")
    else:
        st.error(f"{words_file} not found in repo!")

    # Enter board string
    board_string = st.text_input("Enter board letters as a single string (row-wise):", "meowpurryowlhiss")

    if st.button("Find words"):
        if not words:
            st.warning("Word list is empty or missing.")
        else:
            # Build grid
            B = Board(board_string)
            grid = B.mapping

            # Filter words by letters in grid
            letters_excluded = [c for c in 'abcdefghijklmnopqrstuvwxyz' if c not in board_string]
            words_included = [w for w in words if not set(w) & set(letters_excluded)]

            # Find words
            found_words = find_words_in_grid(grid, words_included)
            found_words = sorted([w for w in found_words if len(w) > 3])

            if found_words:
                st.success(f"Found {len(found_words)} words!")
                # Display words by length
                max_len = max(len(w) for w in found_words)
                min_len = min(len(w) for w in found_words)
                for i in range(min_len, max_len + 1):
                    words_of_len = [w for w in found_words if len(w) == i]
                    if words_of_len:
                        st.write(f"**{i} LETTER WORDS ({len(words_of_len)})**")
                        st.write(words_of_len)
            else:
                st.info("No words found.")
