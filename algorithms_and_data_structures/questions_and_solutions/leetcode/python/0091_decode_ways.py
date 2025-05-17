class Solution:
    def numDecodings(self, s: str) -> int:
        return self.recursive(s, 0)

        # dp = {}
        # return self.topDown(s, 0, dp)

        # dp = [0 for i in range(len(s))]
        # return self.bottomUp(s, dp)

        # return self.bottomUpConstantSpace(s)

    def recursive(self, s, index):
        if index == len(s): return 1
        if index > len(s): return 0
        if s[index] == "0": return 0

        res1, res2 = 0, 0
        res1 = self.recursive(s, index + 1)
        
        num = s[index: index + 2]
        if 0 < int(num) <= 26: res2 = self.recursive(s, index + 2)

        return res1 + res2

    def topDown(self, s, index, dp):
        if index in dp: return dp[index]

        if index == len(s): return 1
        if index > len(s): return 0
        if s[index] == "0": return 0

        res = 0
        if index + 1 <= len(s): res += self.recursive(s, index + 1)
        if index + 2 <= len(s):
            if int(s[index:index + 2]) > 0 and int(s[index:index + 2]) <= 26: res += self.recursive(s, index + 2)
        
        dp[index] = res

        return dp[index]

    def bottomUp(self, s, dp):
        if s[0] == "0": return 0
        dp[0] = 1

        for i in range(1, len(s)):
            if s[i] != "0": dp[i] = dp[i - 1]
            twoDigit = s[i - 1:i + 1]
            if twoDigit[0] != "0" and int(twoDigit) > 0 and int(twoDigit) <= 26:
                if i == 1: dp[i] += 1
                else: dp[i] += dp[i - 2]

        return dp[len(s) - 1]
    
    def bottomUpConstantSpace(self, s):
        if s[0] == "0": return 0
        if len(s) == 1: return 1
        
        prev, curr = 1, 0
        if s[1] != "0": curr = prev
        twoDigit = s[0:2]
        if int(twoDigit) > 0 and int(twoDigit) <= 26: curr += 1
        
        for i in range(2, len(s)):
            tmp = 0
            if s[i] != "0": tmp = curr
            twoDigit = s[i - 1:i + 1]
            if twoDigit[0] != "0" and int(twoDigit) > 0 and int(twoDigit) <= 26: tmp += prev
            prev = curr
            curr = tmp
        
        return curr