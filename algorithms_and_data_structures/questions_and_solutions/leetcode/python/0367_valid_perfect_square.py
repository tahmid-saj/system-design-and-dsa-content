class Solution(object):
    def isPerfectSquare(self, num):
        """
        :type num: int
        :rtype: bool
        """
        l = 0
        r = num
        while l <= r:
            m = (l + r) >> 1
            val = m * m

            if val == num: return True
            elif val > num: r = m - 1
            else: l = m + 1

        return False