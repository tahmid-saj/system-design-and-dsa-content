class TrieNode:
    def __init__(self):
        self.children = {}
        self.isEnd = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def charToIndex(self, ch):
        return ord(ch) - ord('a')
    
    def insert(self, word):
        node = self.root
        for w in word:
            i = self.charToIndex(w)
            if i not in node.children: node.children[i] = TrieNode()
            node = node.children[i]
        node.isEnd = True
    
    def search(self, word, start, dp):
        node = self.root
        for i in range(start, len(word)):
            index = self.charToIndex(word[i])
            if index not in node.children: break
            node = node.children[index]
            if node.isEnd: dp[start] = min(dp[start], dp[i + 1])

class Solution:
    def minExtraChar(self, s: str, dictionary: List[str]) -> int:
        trie = Trie()
        for word in dictionary: trie.insert(word)

        dp = [0 for _ in range(len(s) + 1)]

        for start in range(len(s) - 1, -1, -1):
            dp[start] = dp[start + 1] + 1
            res = trie.search(s, start, dp)
        
        return dp[0]