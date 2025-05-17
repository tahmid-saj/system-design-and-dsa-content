# """
# This is MountainArray's API interface.
# You should not implement it, or speculate about its implementation
# """
#class MountainArray:
#    def get(self, index: int) -> int:
#    def length(self) -> int:

class Solution:
    def findInMountainArray(self, target: int, mountain_arr: 'MountainArray') -> int:
        keyIndex = 1e8

        l, r = 0, mountain_arr.length() - 1
        while l < r:
            middle = l + (r - l) // 2
            val = mountain_arr.get(middle)
            if val == target: keyIndex = min(keyIndex, middle)
            if val > mountain_arr.get(middle + 1): r = middle
            else: l = middle + 1
        peak = l
        if mountain_arr.get(peak) == target: keyIndex = min(keyIndex, peak)

        # first half
        l, r = 0, peak
        while l <= r:
            middle = l + (r - l) // 2
            val = mountain_arr.get(middle)
            if val == target: keyIndex = min(keyIndex, middle)
            if val < target: l = middle + 1
            else: r = middle - 1

        # second half
        l, r = peak, mountain_arr.length() - 1
        while l <= r:
            middle = l + (r - l) // 2
            val = mountain_arr.get(middle)
            if val == target: keyIndex = min(keyIndex, middle)
            if val < target: r = middle - 1
            else: l = middle + 1

        if keyIndex == 1e8: return -1
        return keyIndex