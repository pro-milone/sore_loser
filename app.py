import streamlit as st
import word_search
from utils import Board
import os

# Sidebar menu
st.sidebar.title("Navigation")
tool = st.sidebar.radio("Choose a tool:", ["Word Search", "Other Tool"])

# --------------------------
# Word Search Page
# --------------------------
def word_search_page():
    st.header("Word Search Grid Solver")

    # Load words.txt
    words_file = "words.txt"
    words = []
    if os.path.exists(words_file):
        with open(words_file, "r", encoding="utf-8") as f:
            words = [line.strip().lower() for line in f if line.strip()]
            words = [w for w in words if w.isalpha()]
        st.success(f"Loaded {len(words)} words from {words_file}.")
    else:
        st.error(f"{words_file} not found in repo!")

    board_string = st.text_input("Enter board letters as a single string (row-wise):", "meowpurryowlhiss")

    if st.button("Find words"):
        if not words:
            st.warning("Word list is empty or missing.")
        else:
            B = Board(board_string)
            grid = B.mapping

            letters_excluded = [c for c in 'abcdefghijklmnopqrstuvwxyz' if c not in board_string]
            words_included = [w for w in words if not set(w) & set(letters_excluded)]

            found_words = word_search.find_words_in_grid(grid, words_included)
            found_words = sorted([w for w in found_words if len(w) > 3])

            if found_words:
                st.success(f"Found {len(found_words)} words!")
                max_len = max(len(w) for w in found_words)
                min_len = min(len(w) for w in found_words)
                for i in range(min_len, max_len + 1):
                    words_of_len = [w for w in found_words if len(w) == i]
                    if words_of_len:
                        st.write(f"**{i} LETTER WORDS ({len(words_of_len)})**")
                        st.write(words_of_len)
            else:
                st.info("No words found.")

# --------------------------
# Other Tool Page (Placeholder)
# --------------------------
def other_tool_page():
    st.header("Other Tool")
    st.write("This is a placeholder for another program.")

# --------------------------
# Main App Navigation
# --------------------------
if tool == "Word Search":
    word_search_page()
elif tool == "Other Tool":
    other_tool_page()
