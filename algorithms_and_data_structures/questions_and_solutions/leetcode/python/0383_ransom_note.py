class Solution:
    def canConstruct(self, ransomNote: str, magazine: str) -> bool:
        from collections import Counter

        freq = Counter(magazine)

        for i in range(len(ransomNote)):
            if ransomNote[i] in freq:
                if freq[ransomNote[i]] == 1: del freq[ransomNote[i]]
                else: freq[ransomNote[i]] -= 1
            else: return False
        
        return True