class Solution:
    def partition(self, s: str) -> List[List[str]]:
        self.res = []
        self.backtrack(s, 0, [])
        return self.res
    
    def backtrack(self, s, index, comb):
        if index >= len(s):
            if len(comb) > 0: self.res.append(list(comb))
            return

        for i in range(index, len(s)):
            curr = s[index: i + 1]
            if self.isPalindrome(curr):
                comb.append(curr)
                self.backtrack(s, i + 1, comb)
                comb.pop()
    
    def isPalindrome(self, sub):
        l, r = 0, len(sub) - 1
        while l < r:
            if sub[l] != sub[r]: return False
            l += 1
            r -= 1
        return True