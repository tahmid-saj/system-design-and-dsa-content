class Solution(object):
    def isHappy(self, n):
        """
        :type n: int
        :rtype: bool
        """
        def helper(num):
            res = 0
            while num > 0:
                res += pow(num % 10, 2)
                num /= 10
            return res

        if n == 1: return True

        slow = n
        fast = helper(n)

        while n != 1 and slow != fast:
            slow = helper(slow)
            fast = helper(helper(fast))
            
        return fast == 1