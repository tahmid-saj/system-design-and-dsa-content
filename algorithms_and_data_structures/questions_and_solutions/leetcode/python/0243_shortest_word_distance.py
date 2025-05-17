class Solution:
    def shortestDistance(self, wordsDict: List[str], word1: str, word2: str) -> int:
        shortestDistance = len(wordsDict) # Initialize the shortest distance with the length of the wordsDict list
        position1, position2 = -1, -1 # Initialize the positions of word1 and word2 with -1

        for i, word in enumerate(wordsDict):
            if word == word1: # If the current word is word1, update the position1
                position1 = i
            elif word == word2: # If the current word is word2, update the position2
                position2 = i
            # If both the positions are updated, update the shortest distance
            if position1 != -1 and position2 != -1:
                shortestDistance = min(shortestDistance, abs(position1 - position2))

        return shortestDistance