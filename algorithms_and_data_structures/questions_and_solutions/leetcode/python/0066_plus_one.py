class Solution(object):
    def plusOne(self, digits):
        """
        :type digits: List[int]
        :rtype: List[int]
        """
        # if digits[-1] + 1 < 10: digits[-1] += 1, return digits
        # else:
        # carry = 1, digits[-1] = (digits[-1] + 1) % 10
        # loop through digits from -2 position to 0 using i:
        # -> if digits[i] + carry < 10: digits[i] += carry, carry = 0, break
        # -> elif digits[i] + carry > 10: digits[i] = (digits[i] + carry) % 10
        # if carry == 1: digits.insert(1)
        # return digits

        if digits[-1] + 1 < 10:
            digits[-1] += 1
            return digits

        carry = 1
        digits[-1] = (digits[-1] + 1) % 10

        for i in range(len(digits) - 2, -1, -1):
            if digits[i] + carry < 10:
                digits[i] = (digits[i] + carry) % 10
                carry = 0
                break
            elif digits[i] + carry >= 10:
                digits[i] = (digits[i] + carry) % 10
            
        if carry == 1:
            digits.insert(0, 1)
        return digits