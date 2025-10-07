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
    """
    grid: dict mapping (i, j) -> string (usually one letter)
    words: list of valid words (~100k entries)
    returns: set of all words found in grid
    """
    if not grid or not words:
        return set()

    # Build Trie from words
    trie = Trie()
    for word in words:
        trie.insert(word)

    # Extract grid bounds
    max_i = max(i for i, _ in grid)
    max_j = max(j for _, j in grid)

    found = set()
    directions = [
        (-1, 0), (1, 0), (0, -1), (0, 1),
        (-1, -1), (-1, 1), (1, -1), (1, 1)
    ]

    def dfs(i: int, j: int, node: TrieNode, prefix: str, visited: Set[Tuple[int, int]]):
        """Depth-first search with Trie pruning."""
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

        visited.remove((i, j))  # backtrack

    for (i, j) in grid:
        dfs(i, j, trie.root, "", set())

    return found
