class Solution:
    def generatePalindromes(self, s: str) -> List[str]:
        if len(s) == 1: return [s]
        freq, oddCount, odd = Counter(s), 0, ""
        for k, v in freq.items():
            if v % 2 != 0: 
                oddCount += 1
                odd = k
                freq[k] -= 1
            if oddCount >= 2: return []
        
        if len(freq) == 1: return [s]
        self.res = []
        self.backtrack(s, freq, odd, "")
        return self.res
    
    def backtrack(self, s, freq, odd, comb):
        if (2 * len(comb)) + len(odd) == len(s):
            self.res.append(str(comb + odd + comb[::-1]))
            return
        
        for c in freq:
            if freq[c] % 2 == 0 and freq[c] > 0:
                comb += c
                freq[c] -= 2
                self.backtrack(s, freq, odd, comb)
                comb = str(comb[:-1])
                freq[c] += 2