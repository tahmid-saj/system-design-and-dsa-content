class Solution:
    def reverseStr(self, s: str, k: int) -> str:
        # l, r, i = 0, 0, 0
        # if len(s) < k: l = 0, r = len(s) - 1, return reverse(l, r)
        # loop through s using i < len(s):
        # if i + 1 % k == 0:
        # l = i - k + 1
        # r = i
        # s = reverse(l, r)
        # i += 2K
        def reverse(l, r, s):
            sl = list(s)
            while l < r:
                sl[l], sl[r] = sl[r], sl[l]
                l += 1
                r -= 1
            
            return "".join(sl)

        if len(s) < k:
            l, r = 0, len(s) - 1
            return reverse(l, r, s)

        i = k - 1
        while i < len(s):
            if (i + 1) % k == 0:
                l = i - k + 1
                s = reverse(l, i, s)
                i += 2 * k

        return s