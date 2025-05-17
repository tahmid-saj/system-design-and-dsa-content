from collections import defaultdict
class ValidWordAbbr:
    def __init__(self, dictionary: List[str]):
        self.abb = defaultdict(set)
        for word in dictionary: 
            abb = self.abbreviate(word)
            self.abb[abb].add(word)

    def isUnique(self, word: str) -> bool:
        abb = self.abbreviate(word)
        if abb not in self.abb: return True
        if abb in self.abb and word in self.abb[abb] and len(self.abb[abb]) == 1: return True
        return False

    def abbreviate(self, word):
        if len(word) <= 2: return word
        return word[0] + str(len(word[1:-1])) + word[-1]


# Your ValidWordAbbr object will be instantiated and called as such:
# obj = ValidWordAbbr(dictionary)
# param_1 = obj.isUnique(word)