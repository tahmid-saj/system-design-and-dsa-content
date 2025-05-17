import bintrees, math
class Solution:
    def findClosestEntriesIn3SortedArrays(self, sorted_arrays):
        iters = bintrees.RBTree()
        for i, sorted_array in enumerate(sorted_arrays):
            it = iter(sorted_array)
            firstMin = next(sorted_array, None)
            if firstMin: iters.insert((firstMin, i), it)
        
        res = math.inf
        while True:
            minVal, minIndex = iters.min_key()
            maxVal, _ = iters.max_key()
            res = min(res, maxVal - minVal)
            it = iters.pop_min()[1]
            nextMin = next(it, None)
            if not nextMin: return res
            iters.insert((nextMin, minIndex), it)
        
        return res