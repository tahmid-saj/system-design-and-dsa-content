class Solution:
    def removeKdigits(self, num: str, k: int) -> str:
        stack = []
        
        for digit in num:
            while k > 0 and stack and stack[-1] > digit:
                stack.pop()
                k -= 1
                
            stack.append(digit)
            
        # Truncate the remaining K digits
        stack = stack[:-k] if k > 0 else stack 
        
        # Remove any leading zeros
        return "".join(stack).lstrip("0") or "0"