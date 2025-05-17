class TrieNode:
    def __init__(self):
        self.children = {}
        self.isEnd = False

class WordDictionary:
    def __init__(self):
        self.root = TrieNode()
    
    def charToIndex(self, ch):
        return ord(ch) - ord('a')

    def addWord(self, word: str) -> None:
        node = self.root
        for w in word:
            index = self.charToIndex(w)
            if index not in node.children: node.children[index] = TrieNode()
            node = node.children[index]
        node.isEnd = True

    def search(self, word: str) -> bool:
        node = self.root
        if self.searchDFS(word, node, 0): return True
        return False

    def searchDFS(self, word, node, index):
        if index >= len(word) and node.isEnd: return True
        elif index >= len(word): return False
        if not node: return False
        
        idx = self.charToIndex(word[index])

        if word[index] != "." and idx not in node.children: return False
        elif word[index] != "." and idx in node.children and self.searchDFS(word, node.children[idx], index + 1): return True

        if word[index] == ".":
            for k, v in node.children.items():
                if self.searchDFS(word, v, index + 1): return True


# Your WordDictionary object will be instantiated and called as such:
# obj = WordDictionary()
# obj.addWord(word)
# param_2 = obj.search(word)