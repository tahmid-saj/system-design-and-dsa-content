class Solution:
    def toLowerCase(self, s: str) -> str:
        # return self.hashmap(s)
        return self.ord(s)
    
    def hashmap(self, s):
        upper, lower = "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"
        upperToLower = dict(zip(upper, lower))
        res = [upperToLower[c] if c in upper else c for c in s]
        return "".join(res)
    
    def ord(self, s):
        res = []
        for c in s:
            if 65 <= ord(c) <= 90: res.append(chr(ord(c) + 32))
            else: res.append(c)
        return "".join(res)