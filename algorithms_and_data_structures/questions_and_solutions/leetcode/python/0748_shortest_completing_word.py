class Solution:
    def shortestCompletingWord(self, licensePlate: str, words: List[str]) -> str:
        freqlp = {}
        for i in range(len(licensePlate)): 
            if licensePlate[i].isalpha(): freqlp[licensePlate[i].lower()] = freqlp.get(licensePlate[i].lower(), 0) + 1

        res = None
        for word in words:
            freqWord = {}
            for w in word:
                if w.isalpha() and w.lower() in freqlp:
                    if freqWord.get(w.lower(), 0) < freqlp[w.lower()]: freqWord[w.lower()] = freqWord.get(w.lower(), 0) + 1
                    if freqWord == freqlp:
                        if not res or len(word) < len(res): res = word
        return res