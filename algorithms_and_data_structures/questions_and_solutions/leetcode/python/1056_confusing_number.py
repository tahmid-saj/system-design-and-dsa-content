class Solution:
    def confusingNumber(self, n: int) -> bool:
        conf = {
            0: 0,
            1: 1,
            6: 9,
            8: 8,
            9: 6
        }
        confNum, res = n, 0
        while confNum > 0:
            c = confNum % 10
            if c not in conf: return False
            res *= 10
            res += conf[c]
            confNum //= 10
        return res != n