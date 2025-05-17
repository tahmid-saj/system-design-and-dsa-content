# The isBadVersion API is already defined for you.
# @param version, an integer
# @return a bool
# def isBadVersion(version):

class Solution(object):
    def firstBadVersion(self, n):
        """
        :type n: int
        :rtype: int
        """
        if n == 1: return 1

        # 1 2 3 4 5
        # F F F T T
        l, r, middle = 1, n, 0

        while l <= r:
            middle = l + (r - l) // 2
            res = isBadVersion(middle)

            if res == True:
                r = middle - 1
            elif res == False:
                l = middle + 1

        return l

        