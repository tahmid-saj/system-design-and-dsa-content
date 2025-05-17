class TrieNode(self):
  def __init__(self):
    self.children = [None] * 26
    self.endOfWord = False

class Trie(self):
  def __init__(self):
    self.root = TrieNode()
  
  def charToIndex(self, ch):
    return ord(ch) - ord('a')

  def insert(self, word):
    node = self.root
    for w in word:
      index = self.charToIndex(w)
      if not node.children[index]: node.children[index] = TrieNode()
      node = node.children[index]
    node.endOfWord = True
  
  def search(self, word):
    node = self.root
    for w in word:
      index = self.charToIndex(w)
      if not node.children[index]: return False
      node = node.children[index]
    return node.endOfWord
  
  def delete(self, word):
    self.deleteRecursive(self.root, word, 0)
  
  def deleteRecursive(self, currNode, word, index):
    # returning False in this recursive call indicates there are no nodes to further delete 
    # returning True in this recursive call indicates there are nodes to delete (Null nodes)
    if index == len(word):
      if currNode.endOfWord:
        currNode.endOfWord = False
        return not any(currNode.children)
      return False
    
    node = currNode.children[self.charToIndex(word[index])]
    if not node: return False
    
    shouldDelete = self.deleteRecursive(node, word, index + 1)
    if shouldDelete:
      currNode.children[self.charToIndex(word[index])] = None
      return not any(currNode.children)

    return False