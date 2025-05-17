class Solution:
    def decode(self, s):
        res, num = [], 0
        for i in range(len(s)):
            if s[i].isnumeric():
                num *= 10
                num += int(s[i])
            else:
                res.append(num * s[i])
                num = 0

        return "".join(res)

    def encode(self, s):
        if len(s) == 0: return ""
        res = []
        count, curr = 0, ""
        for i in range(len(s)):
            if curr != s[i]:
                if curr != "": res.extend([str(count), curr])
                count = 1
                curr = s[i]
            else: count += 1
        
        res.extend([str(count), curr])
        
        return "".join(res)