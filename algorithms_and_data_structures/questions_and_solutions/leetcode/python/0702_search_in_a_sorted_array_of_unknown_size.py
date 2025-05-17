# """
# This is ArrayReader's API interface.
# You should not implement it, or speculate about its implementation
# """
#class ArrayReader:
#    def get(self, index: int) -> int:

class Solution:
    def search(self, reader: 'ArrayReader', target: int) -> int:
        l, r = 0, 1

        while reader.get(r) < target:
            lNew = r + 1
            r += (r - l + 1) * 2
            l = lNew

        while l <= r:
            middle = l + (r - l) // 2
            val = reader.get(middle)

            if val < target: l = middle + 1
            elif val > target: r = middle - 1
            else: return middle
        
        return -1