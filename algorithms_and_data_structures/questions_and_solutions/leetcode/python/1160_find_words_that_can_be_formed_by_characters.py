class Solution:
    def countCharacters(self, words: List[str], chars: str) -> int:
        freqChars, res = {}, 0
        for char in chars: freqChars[char] = freqChars.get(char, 0) + 1

        for word in words:
            freq = freqChars.copy()
            for w in word:
                if w in freq:
                    freq[w] -= 1
                    if freq[w] == 0: freq.pop(w)
                elif w not in freq: break
            else: res += len(word)
        
        return res