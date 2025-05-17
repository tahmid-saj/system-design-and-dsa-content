class Solution:
    def wordPatternMatch(self, pattern: str, s: str) -> bool:
        return self.backtrackSol1(pattern, s, {})
        # return self.backtrackSol2(pattern, s)
    
    def backtrackSol1(self, pattern, curr, mappings):
        if not pattern: return not curr

        # if pattern[0] in mappings
        if pattern[0] in mappings:
            if curr[:len(mappings[pattern[0]])] != mappings[pattern[0]]: return False
            return self.backtrackSol1(pattern[1:], curr[len(mappings[pattern[0]]):], mappings)
        
        # if pattern[0] is not in mappings
        for i in range(len(curr)):
            if curr[: i + 1] in mappings.values(): continue

            mappings[pattern[0]] = curr[: i + 1]
            if self.backtrackSol1(pattern[1:], curr[i + 1:], mappings): return True
            del mappings[pattern[0]]
        
        return False

    def backtrackSol2(self, pattern, s):
        self.patternString = {}
        res = self.backtrack(pattern, s, 0, 0)

        for k, v in self.patternString.items():
            self.patternString[k] = ""
            if v in self.patternString.values(): return False

        return res
    
    def backtrack(self, pattern, s, j, index):
        if j == len(pattern) and index == len(s): return True
        elif j >= len(pattern) or index >= len(s): return False
        
        for i in range(index, len(s)):
            curr = s[index: i + 1]
            if pattern[j] in self.patternString and len(curr) == len(self.patternString[pattern[j]]) and self.patternString[pattern[j]] != curr: return False

            if pattern[j] not in self.patternString: self.patternString[pattern[j]] = curr
            elif pattern[j] in self.patternString and len(curr) < len(self.patternString[pattern[j]]): continue
            if pattern[j] in self.patternString and self.patternString[pattern[j]] == curr and self.backtrack(pattern, s, j + 1, i + 1): return True
            if pattern[j] in self.patternString: self.patternString.pop(pattern[j])
        return False