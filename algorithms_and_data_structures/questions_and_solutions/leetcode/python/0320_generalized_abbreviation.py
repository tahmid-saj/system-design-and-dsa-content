class Solution:
    def generateAbbreviations(self, word: str) -> List[str]:
        self.res = []
        self.backtrack(word, 0, [], False)
        return self.res
    
    def backtrack(self, word, index, comb, prevAbb):
        if index == len(word):
            self.res.append("".join(comb))
            return

        comb.append(word[index])
        self.backtrack(word, index + 1, comb, False)
        comb.pop()
        
        for i in range(index, len(word)):
            if not prevAbb:
                comb.append(str(i - index + 1))
                self.backtrack(word, i + 1, comb, True)
                comb.pop()