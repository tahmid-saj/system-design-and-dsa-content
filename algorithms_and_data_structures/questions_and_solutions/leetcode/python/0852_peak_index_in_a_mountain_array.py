class Solution:
    def peakIndexInMountainArray(self, arr: List[int]) -> int:
        l, r = 0, len(arr) - 1

        while l < r:
            middle = l + (r - l) // 2

            if arr[middle] > arr[middle + 1]: r = middle
            else: l = middle + 1
        
        return l