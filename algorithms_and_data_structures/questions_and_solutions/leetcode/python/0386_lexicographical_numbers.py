class TrieNode:
    def __init__(self):
        self.children = {}
        self.num = None

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, num):
        node = self.root
        for w in num:
            if w not in node.children: node.children[w] = TrieNode()
            node = node.children[w]
        node.isEnd = True
        node.num = int(num)
    
    def search(self):
        self.res = []
        self.searchDfs(self.root)
        return self.res
    
    def searchDfs(self, node):
        if node.num:
            self.res.append(node.num)
        if not node: return

        for w, n in node.children.items(): self.searchDfs(n)

class Solution:
    def lexicalOrder(self, n: int) -> List[int]:
        trie = Trie()
        for i in range(1, n + 1): trie.insert(str(i))

        return trie.search()
