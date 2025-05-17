class Solution:
    def fixedPoint(self, arr: List[int]) -> int:
        l, r, res = 0, len(arr) - 1, -1
        
        while l < r:
            middle = l + (r - l) // 2
            if arr[middle] == middle: res = middle
            if arr[middle] < middle: l = middle + 1
            else: r = middle
        
        return res