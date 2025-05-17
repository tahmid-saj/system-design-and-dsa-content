class Solution:
    def toGoatLatin(self, sentence: str) -> str:
        res, i = [], 1
        for word in sentence.split():
            if word[0] in "aeiouAEIOU": res.append(word + "ma" + "a" * i)
            else: res.append(word[1:] + word[0] + "ma" + "a" * i)
            i += 1
        return " ".join(res)