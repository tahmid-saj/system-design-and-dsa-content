class TrieNode:
    def __init__(self):
        self.children = {}
        self.isEnd = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def charToIndex(self, ch):
        return ord(ch) - ord('a')

    def insert(self, word: str) -> None:
        node = self.root
        for w in word:
            index = self.charToIndex(w)
            if index not in node.children: node.children[index] = TrieNode()
            node = node.children[index]
        node.isEnd = True

    def search(self, word: str) -> bool:
        node = self.root
        for w in word:
            index = self.charToIndex(w)
            if index not in node.children: return False
            node = node.children[index]
        return node.isEnd

    def startsWith(self, prefix: str) -> bool:
        node = self.root
        for w in prefix:
            index = self.charToIndex(w)
            if index not in node.children: return False
            node = node.children[index]
        return True

# Your Trie object will be instantiated and called as such:
# obj = Trie()
# obj.insert(word)
# param_2 = obj.search(word)
# param_3 = obj.startsWith(prefix)