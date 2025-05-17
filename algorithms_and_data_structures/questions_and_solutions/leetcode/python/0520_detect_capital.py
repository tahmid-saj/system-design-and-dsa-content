class Solution:
    def detectCapitalUse(self, word: str) -> bool:
        if word.upper() == word: return True
        if word.lower() == word: return True
        if word[0].upper() + word[1:].lower() == word: return True
        return False