class TrieNode:
    def __init__(self):
        self.children = {}
        self.isEnd = False
        self.word = ""
    
class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word):
        node = self.root
        for w in word:
            if w not in node.children: node.children[w] = TrieNode()
            node = node.children[w]
        node.isEnd = True
        node.word = word
    
    def search(self, board):
        self.res = set()
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] in self.root.children:
                    self.dfs(board, self.root, i, j)
        
        return self.res
    
    def remove(self, node, word, index):
        if index == len(word):
            if node.isEnd:
                node.isEnd = False
                return not any(node.children)
            return False
        
        if word[index] not in node.children: return False

        res = self.remove(node.children[word[index]], word, index + 1)
        if res:
            del node.children[word[index]]
            return not any(node.children)
        
        return False
    
    def dfs(self, board, node, i, j):
        if node.isEnd == True: 
            self.res.add(node.word)
            # self.remove(self.root, node.word, 0)
        if i < 0 or i >= len(board) or j < 0 or j >= len(board[0]): return
        if board[i][j] not in node.children: return

        ch = board[i][j]
        tmp, board[i][j] = board[i][j], "/"

        self.dfs(board, node.children[ch], i + 1, j)
        self.dfs(board, node.children[ch], i - 1, j)
        self.dfs(board, node.children[ch], i, j + 1)
        self.dfs(board, node.children[ch], i, j - 1)

        board[i][j] = tmp

class Solution:
    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
        trie = Trie()
        for word in words: trie.insert(word)

        return trie.search(board)