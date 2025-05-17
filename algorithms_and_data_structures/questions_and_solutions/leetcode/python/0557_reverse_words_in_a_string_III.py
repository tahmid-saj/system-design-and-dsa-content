class Solution:
    def reverseWords(self, s: str) -> str:
        # loop through s using i:
        # l = 0
        # if s[i + 1] == " " or i == len(s):
        #   s = reverse(l, i, s)
        #   l = i + 2
        def reverse(l, r, s):
            sl = list(s)
            while l < r:
                sl[l], sl[r] = sl[r], sl[l]
                l += 1
                r -= 1
            return "".join(sl)

        l = 0
        for i in range(0, len(s)):
            if i == len(s) - 1 or s[i + 1] == " ":
                s = reverse(l, i, s)
                l = i + 2

        return s