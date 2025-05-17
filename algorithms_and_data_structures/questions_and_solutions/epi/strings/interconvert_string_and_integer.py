from functools import reduce
import string
class Solution:
    def intToStr(self, num):
        neg = False
        if int < 0:
            num = -num
            neg = True

        res = ""
        while num > 0:
            n = num % 10
            res.append(chr(ord("0") + n))
            num //= 10
        res = res[::-1]

        if neg: return "-" + res
        return res
    
    def strToInt1(self, s):
        if len(s) == 0: return 0
        neg, start = False, 0
        if s[0] == "-":
            neg = True
            start = start + 1

        res = 0
        for i in range(start, len(s)):
            res *= 10
            res += int(s[i])

        if neg: return "-" + res
        return res
    
    def strToInt2(self, s):
        res = reduce(lambda runningSum, c: (runningSum * 10) + string.digits.index(c), s[s[0] in "+-":], 0)
        if s[0] == "-": return -res
        return res