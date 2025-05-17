class Solution:
    def canThreePartsEqualSum(self, arr: List[int]) -> bool:
        s = sum(arr)
        if s % 3 != 0: return False
        curr, count = s // 3, 0

        for num in arr:
            curr -= num
            if curr == 0: 
                curr = s // 3
                count += 1
        
        return count >= 3