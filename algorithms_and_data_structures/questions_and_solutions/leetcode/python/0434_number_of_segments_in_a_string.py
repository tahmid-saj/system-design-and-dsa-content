class Solution:
    def countSegments(self, s: str) -> int:
        if len(s) == 0: return 0

        counting, res = False, 0

        for i in range(0, len(s)):
            if counting == False and s[i] != " ":
                counting = True
            elif counting == True and (s[i] == " " or i == len(s) - 1):
                counting = False
                res += 1

        if counting == True: res += 1

        return res