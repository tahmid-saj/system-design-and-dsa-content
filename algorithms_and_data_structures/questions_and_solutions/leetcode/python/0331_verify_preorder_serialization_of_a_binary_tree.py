class Solution:
    def isValidSerialization(self, preorder: str) -> bool:
        return self.slots(preorder)
    
    def slots(self, preorder):
        slots, prev = 1, None

        for c in preorder:
            if c == ",":
                slots -= 1
                if slots < 0: return False
                if prev != "#": slots += 2
            prev = c
        slots = slots + 1 if prev != "#" else slots - 1
        return slots == 0