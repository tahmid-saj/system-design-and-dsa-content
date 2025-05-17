class TrieNode:
    def __init__(self):
        self.isWord = False
        self.children = {}

class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        # self.words = set(wordDict)
        # @lru_cache(None)
        # def topDown(index):
        #     if index == len(s): return True
        #     for w in self.words:
        #         if s[index:index + len(w)] == w and topDown(index + len(w)): return True
        #     return False
        # return topDown(0)
    
        # return self.trieBFS(s, wordDict)
        # return self.bottomUp(s, wordDict)
        return self.lastLengthOfDecomposition(s, wordDict)

    def bottomUp(self, s, wordDict):
        dp = [False for _ in range(len(s))]

        for i in range(len(s)):
            for w in wordDict:
                if i - (len(w) - 1) < 0: continue
                if i - (len(w) - 1) == 0 or dp[i - len(w)] == True:
                    if s[i - (len(w) - 1):i + 1] == w: dp[i] = True
        
        return dp[-1]

    def trieBFS(self, s, wordDict):
        words = set(wordDict)
        queue = deque([0])
        seen = set()

        while queue:
            start = queue.popleft()
            if start == len(s): return True

            for end in range(start + 1, len(s) + 1):
                if end in seen: continue

                if s[start:end] in words:
                    queue.append(end)
                    seen.add(end)
        
        return False
    
    def lastLengthOfDecomposition(self, s, wordDict):
        wordDict = set(wordDict)
        lastLength = [-1 for _ in range(len(s))]

        for i in range(len(s)):
            if s[:i + 1] in wordDict:
                lastLength[i] = i + 1
                continue
            
            for j in range(i):
                if lastLength[j] != -1 and s[j + 1:i + 1] in wordDict:
                    lastLength[i] = i - j
                    break
        
        # res = []
        # if lastLength[-1] != -1:
        #     i = len(s) - 1
        #     while i >= 0:
        #         res.append(s[i + 1 - lastLength[i]:i + 1])
        #         i -= lastLength[i]
        #     res = res[::-1]
        # return res
        if lastLength[-1] != -1: return True
        return False