class Solution(object):
    def mySqrt(self, x):
        """
        :type x: int
        :rtype: int
        """
        if x == 0: return 0
        if x == 1 or x == 2: return 1

        l = 1
        r = x
        middle = 0

        while (l <= r):
            middle = l + (r - l) / 2

            if int(x / middle) == middle:
                return middle
            elif x / middle < middle:
                r = middle - 1
            elif x / middle > middle:
                l = middle + 1
        
        return l - 1