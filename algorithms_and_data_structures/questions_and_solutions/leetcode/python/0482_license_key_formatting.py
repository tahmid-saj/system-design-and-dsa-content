class Solution:
    def licenseKeyFormatting(self, s: str, k: int) -> str:
        res = ""
        # j = 0
        # start from the back, using i loop through s:
        # if s[i] != "-":
        #   j += 1
        #   res += s[i]
        #   if j % k == 0 and i != 0: res += "-"
        if len(s) == 1 and s[0] != "-": return s.upper()
        elif len(s) == 1 and s[0] == "-": return ""

        j = 0
        for i in range(len(s) - 1, -1, -1):
            if s[i] != "-":
                j += 1
                res += s[i]
                if j % k == 0 and i != 0: res += "-"

        if res != "" and res[-1] == "-": res = res[:-1]
        
        return res.upper()[::-1]