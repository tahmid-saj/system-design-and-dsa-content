class Solution:
    def findOcurrences(self, text: str, first: str, second: str) -> List[str]:
        text = text.split()
        i, res = 0, []
        while i < len(text):
            if text[i] == first and i + 2 < len(text) and i + 1 < len(text) and text[i + 1] == second: res.append(text[i + 2])
            i += 1
        return res