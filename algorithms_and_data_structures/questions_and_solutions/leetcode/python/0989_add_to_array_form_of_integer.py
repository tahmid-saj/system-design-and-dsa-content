class Solution:
    def addToArrayForm(self, num: List[int], k: int) -> List[int]:
        carry, i = 0, len(num) - 1
        while i >= 0 or k > 0:
            n = k % 10
            k //= 10
            curr = 0 if i < 0 else num[i]
            s = curr + n + carry

            if carry == 0:
                if s >= 10: carry = 1
            elif carry == 1:
                if s < 10: carry = 0
                
            if i < 0: num.insert(0, s % 10)
            else: num[i] = s % 10
            i -= 1
        
        if carry == 1: num.insert(0, 1)
        return num