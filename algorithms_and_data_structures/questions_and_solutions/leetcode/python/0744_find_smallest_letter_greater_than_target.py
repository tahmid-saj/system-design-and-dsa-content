class Solution:
    def nextGreatestLetter(self, letters: List[str], target: str) -> str:
        # return self.letterSearch(letters, target)
        return self.binarySearch(letters, target)
    
    def letterSearch(self, letters, target):
        res = letters[0]
        letters = set(letters)
        for c in "abcdefghijklmnopqrstuvwxyz":
            if c in letters and ord(c) > ord(target): 
                res = c
                break
        return res
    
    def binarySearch(self, letters, target):
        l, r, res = 0, len(letters) - 1, None
        while l <= r:
            middle = l + (r - l) // 2
            ordMiddle, ordTarget = ord(letters[middle]), ord(target)
            if ordMiddle > ordTarget:
                res = letters[middle]
                if middle == 0 or ord(letters[middle - 1]) <= ordTarget: break
                r = middle - 1
            elif ordMiddle <= ordTarget: l = middle + 1
        if res: return res
        return letters[0]