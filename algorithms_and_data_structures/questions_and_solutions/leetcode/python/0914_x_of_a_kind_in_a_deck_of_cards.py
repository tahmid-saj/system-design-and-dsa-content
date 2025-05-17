class Solution:
    def hasGroupsSizeX(self, deck: List[int]) -> bool:
        return self.bruteForce(deck)
        # return self.gcdOfFreq(deck)
    
    def bruteForce(self, deck):
        freq = {}
        for num in deck: freq[num] = freq.get(num, 0) + 1
        for x in range(2, len(deck) + 1):
            if len(deck) % x == 0:
                if all(v % x == 0 for v in freq.values()): return True
        return False

    def gcdOfFreq(self, deck):
        freq = {}
        for num in deck: freq[num] = freq.get(num, 0) + 1
        return functools.reduce(math.gcd, freq.values()) >= 2