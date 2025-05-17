class Solution:
    def areSentencesSimilar(self, sentence1: List[str], sentence2: List[str], similarPairs: List[List[str]]) -> bool:
        if len(sentence1) != len(sentence2): return False
        similar = set()
        for pair in similarPairs: similar.add((pair[0], pair[1]))

        for i in range(len(sentence1)):
            if sentence1[i] == sentence2[i]: continue
            if (sentence1[i], sentence2[i]) not in similar and (sentence2[i], sentence1[i]) not in similar: return False
        return True