class Solution:
    def countPrefixes(self, words: List[str], s: str) -> int:
        res, prefixes = 0, set()
        for word in words:
            if word in prefixes:
                res += 1
                continue
            if word == s[:len(word)]: 
                res += 1
                prefixes.add(word)
        
        return res