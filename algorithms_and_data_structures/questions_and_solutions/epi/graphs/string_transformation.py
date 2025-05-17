from collections import namedtuple, deque
import string
class Solution:
    def stringTransformation(self, dict, s, t):
        return self.bfs(dict, s, t)
    
    def bfs(self, dict, s, t):
        word = namedtuple("word", ("str", "dist"))
        start = word(s, 0)
        queue = deque([start])
        dict.remove(s)
        while queue:
            w, d = queue.popleft()
            if w == t: return d

            for i in range(len(w)):
                for c in string.ascii_lowercase:
                    cand = w[:i] + c + w[i + 1:]
                    if cand in dict:
                        dict.remove(cand)
                        queue.append((cand, d + 1))
        
        return -1