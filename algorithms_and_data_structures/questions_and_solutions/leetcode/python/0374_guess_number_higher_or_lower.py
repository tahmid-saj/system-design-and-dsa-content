# The guess API is already defined for you.
# @param num, your guess
# @return -1 if num is higher than the picked number
#          1 if num is lower than the picked number
#          otherwise return 0
# def guess(num):

class Solution(object):
    def guessNumber(self, n):
        """
        :type n: int
        :rtype: int
        """
        if n == 1: return 1

        l, r, middle = 2, n, 0

        while l <= r:
            middle = l + (r - l) // 2
            res = guess(middle)

            if res == 0: return middle
            elif res == -1: r = middle - 1
            elif res == 1: l = middle + 1

        return l - 1