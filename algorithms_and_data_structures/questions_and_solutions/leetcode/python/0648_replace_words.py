class TrieNode:
    def __init__(self):
        self.children = {}
        self.isEnd = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word):
        node = self.root
        for w in word:
            if w not in node.children: node.children[w] = TrieNode()
            node = node.children[w]
        node.isEnd = True
    
    def search(self, word):
        node, prefix = self.root, ""
        for w in word:
            prefix += w
            if w not in node.children: return word
            node = node.children[w]
            if node.isEnd: break
        
        return prefix

class Solution:
    def replaceWords(self, dictionary: List[str], sentence: str) -> str:
        trie = Trie()
        for word in dictionary: trie.insert(word)

        sentence = sentence.split(" ")
        for i in range(len(sentence)): sentence[i] = trie.search(sentence[i])

        return " ".join(sentence)