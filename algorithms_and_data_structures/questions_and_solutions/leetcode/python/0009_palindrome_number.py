class Solution(object):
    def isPalindrome(self, x):
        """
        :type x: int
        :rtype: bool
        """
        if x < 0: return False

        rev, org = 0, x
        while (x > 0):
            rev *= 10
            rev += x % 10
            x /= 10
        
        return rev == org