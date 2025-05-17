class TrieNode:
    def __init__(self):
        self.children = {}
        self.isEnd = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
        self.maxLength = 0
    
    def charToIndex(self, ch):
        return ord(ch) - ord('a')
    
    def insert(self, word):
        length = 0
        node = self.root

        for w in word:
            i = self.charToIndex(w)
            if i not in node.children: node.children[i] = TrieNode()
            node = node.children[i]
            length += 1
        node.isEnd = True
        self.maxLength = max(self.maxLength, length)
    
    def search(self, word):
        node = self.root
        for w in word:
            i = self.charToIndex(w)
            if i not in node.children: return False
            node = node.children[i]
        if node.isEnd: return True
        return False

class Solution:
    def indexPairs(self, text: str, words: List[str]) -> List[List[int]]:
        trie = Trie()
        for word in words: trie.insert(word) 

        res = []
        maxLength = trie.maxLength
        for length in range(1, maxLength + 1):
            for i in range(0, len(text) - length + 1):
                j = i + length
                if trie.search(text[i:j]): res.append([i, j - 1])
        
        return sorted(res)