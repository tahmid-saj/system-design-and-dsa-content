class Solution:
    def numJewelsInStones(self, jewels: str, stones: str) -> int:
        Jset = set(jewels)
        return sum(s in Jset for s in stones)