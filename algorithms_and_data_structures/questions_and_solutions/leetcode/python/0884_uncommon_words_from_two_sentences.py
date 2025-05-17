class Solution:
    def uncommonFromSentences(self, s1: str, s2: str) -> List[str]:
        freq = {}
        for s in s1.split(): freq[s] = freq.get(s, 0) + 1
        for s in s2.split(): freq[s] = freq.get(s, 0) + 1

        res = []
        for k, v in freq.items():
            if v == 1: res.append(k)

        return res