class Solution:
    def checkIfPangram(self, sentence: str) -> bool:
        sentence = sentence.lower()
        letters = set()
        for i, x in enumerate(sentence):
            if ord(x) >= 97 and ord(x) <= 122: letters.add(x)
        return len(letters) == 26