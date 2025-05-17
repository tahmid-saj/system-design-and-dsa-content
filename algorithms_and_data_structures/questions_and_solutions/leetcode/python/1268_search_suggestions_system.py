class TrieNode:
    def __init__(self):
        self.children = {}
        self.searchWords = []

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for w in word:
            if w not in node.children: node.children[w] = TrieNode()
            if len(node.children[w].searchWords) < 3: node.children[w].searchWords.append(word)
            node = node.children[w]

    def search(self, word):
        result, node = [], self.root
        for i in range(len(word)):
            if word[i] not in node.children: return result + [[] for _ in range(len(word) - i)]
            result.append(node.children[word[i]].searchWords)
            node = node.children[word[i]]
        
        return result

class Solution:
    def suggestedProducts(self, products: List[str], searchWord: str) -> List[List[str]]:
        trie = Trie()
        products.sort()
        for product in products: trie.insert(product)

        return trie.search(searchWord)