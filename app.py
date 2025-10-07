import streamlit as st
from typing import List, Tuple, Dict, Set

# --------------------------
# Trie Implementation
# --------------------------
class TrieNode:
    def __init__(self):
        self.children: Dict[str, "TrieNode"] = {}
        self.is_word: bool = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word: str):
        node = self.root
        for ch in word:
            node = node.children.setdefault(ch, TrieNode())
        node.is_word = True

# --------------------------
# Word Search in Grid
# --------------------------
def find_words_in_grid(grid: Dict[Tuple[int, int], str], words: List[str]) -> Set[str]:
    if not grid or not words:
        return set()

    trie = Trie()
    for word in words:
        trie.insert(word)

    max_i = max(i for i, _ in grid)
    max_j = max(j for _, j in grid)

    found = set()
    directions = [
        (-1, 0), (1, 0), (0, -1), (0, 1),
        (-1, -1), (-1, 1), (1, -1), (1, 1)
    ]

    def dfs(i: int, j: int, node: TrieNode, prefix: str, visited: Set[Tuple[int, int]]):
        if (i, j) not in grid or (i, j) in visited:
            return
        letter = grid[(i, j)]
        if letter not in node.children:
            return

        next_node = node.children[letter]
        new_prefix = prefix + letter
        visited.add((i, j))

        if next_node.is_word:
            found.add(new_prefix)

        for di, dj in directions:
            ni, nj = i + di, j + dj
            if 0 <= ni <= max_i and 0 <= nj <= max_j:
                dfs(ni, nj, next_node, new_prefix, visited)

        visited.remove((i, j))

    for (i, j) in grid:
        dfs(i, j, trie.root, "", set())

    return found

# --------------------------
# Board helper
# --------------------------
class Board:
    def __init__(self, board_string: str):
        self.board_string = board_string.lower()
        self.mapping = self.create_grid()

    def create_grid(self) -> Dict[Tuple[int, int], str]:
        n = int(len(self.board_string) ** 0.5)
        grid = {}
        for idx, letter in enumerate(self.board_string):
            i = idx // n
            j = idx % n
            grid[(i, j)] = letter
        return grid

# --------------------------
# Load word list
# --------------------------
words_file = "words.txt"
words = []
try:
    with open(words_file, "r", encoding="utf-8") as f:
        words = [line.strip().lower() for line in f if line.strip()]
        words = [w for w in words if w.isalpha()]
except FileNotFoundError:
    st.error(f"{words_file} not found in repo!")

# --------------------------
# Streamlit UI
# --------------------------
st.title("Multi-Tool Word App")

# Tabs
tab1, tab2 = st.tabs(["Word Search", "Other Tool"])

# --------------------------
# Tab 1: Word Search
# --------------------------
with tab1:
    st.header("Word Search Grid Solver")
    board_string = st.text_input("Enter board letters as a single string (row-wise):", "meowpurryowlhiss")
    
    if st.button("Find words", key="find_words"):
        if not words:
            st.warning("Word list is empty or missing.")
        else:
            B = Board(board_string)
            grid = B.mapping

            # Filter words
            letters_excluded = [c for c in 'abcdefghijklmnopqrstuvwxyz' if c not in board_string]
            words_included = [w for w in words if not set(w) & set(letters_excluded)]

            # Find words
            found_words = find_words_in_grid(grid, words_included)
            found_words = [w for w in found_words if len(w) > 3]

            if found_words:
                st.success(f"Found {len(found_words)} words!")

                # Group words by length
                length_to_words = {}
                for word in found_words:
                    length_to_words.setdefault(len(word), []).append(word)

                for length in sorted(length_to_words.keys()):
                    words_of_len = sorted(length_to_words[length])
                    st.subheader(f"{length} LETTER WORDS ({len(words_of_len)})")

                    # Display words in grid
                    cols_count = 6
                    rows = [words_of_len[i:i + cols_count] for i in range(0, len(words_of_len), cols_count)]

                    for row in rows:
                        cols = st.columns(cols_count)
                        for col, word in zip(cols, row):
                            col.markdown(f"**{word}**")
            else:
                st.info("No words found.")

# --------------------------
# Tab 2: Other Tool (Placeholder)
# --------------------------
with tab2:
    st.header("Other Tool")
    st.write("This is a placeholder for another program. You can add any functionality here.")
