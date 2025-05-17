class Solution:
    def uniqueMorseRepresentations(self, words: List[str]) -> int:
        morse = [".-","-...","-.-.","-..",".","..-.","--.","....","..",".---","-.-",".-..","--","-.","---",".--.","--.-",".-.","...","-","..-","...-",".--","-..-","-.--","--.."]
        letters = list("abcdefghijklmnopqrstuvwxyz")
        morseLetters = dict(zip(letters, morse))
        seen = set()
        for word in words:
            curr = []
            for w in word: curr.append(morseLetters[w])
            seen.add("".join(curr))
        return len(seen)