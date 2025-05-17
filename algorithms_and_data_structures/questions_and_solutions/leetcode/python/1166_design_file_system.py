class TrieNode:
    def __init__(self, val=None):
        self.children = {}
        self.val = val
    
class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, path, val):
        pathList = path.split("/")
        node = self.root
        for i in range(len(pathList)):
            if pathList[i] == "": continue

            if pathList[i] not in node.children:
                if i == len(pathList) - 1: 
                    node.children[pathList[i]] = TrieNode(val)
                    return True
                else: return False
            node = node.children[pathList[i]]

        return False

    def search(self, path):
        pathList = path.split("/")
        node = self.root
        for i in range(len(pathList)):
            if pathList[i] == "": continue

            if pathList[i] not in node.children: return -1
            node = node.children[pathList[i]]

        return node.val

class FileSystem:

    def __init__(self):
        self.trie = Trie()

    def createPath(self, path: str, value: int) -> bool:
        return self.trie.insert(path, value)

    def get(self, path: str) -> int:
        return self.trie.search(path)


# Your FileSystem object will be instantiated and called as such:
# obj = FileSystem()
# param_1 = obj.createPath(path,value)
# param_2 = obj.get(path)