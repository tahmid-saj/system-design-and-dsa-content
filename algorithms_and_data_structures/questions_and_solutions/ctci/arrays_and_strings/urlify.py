class Solution:
    def urlify(self, s, length):
        res = []
        for c in s:
            if c == " ":
                if res and res[-1] == "%20": continue
                res.append("%20")
            else: res.append(c)
        if res and res[-1] == "%20": res.pop()

        return "".join(res)

sol = Solution()
print(sol.urlify("Mr John Smith       ", 13))
