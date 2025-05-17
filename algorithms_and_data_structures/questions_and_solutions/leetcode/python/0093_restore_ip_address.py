class Solution:
    def restoreIpAddresses(self, s: str) -> List[str]:
        # if index == len(s): self.res.append(comb[:-1]), return
        # loop through (index, len(s)) using i:
        #   comb += s[i] + ".", self.backtrack(s, comb, i + 1), comb = comb[:-2]
        #   if s[i] != "0":
        #       comb += s[i:i + 2] + ".", self.backtrack(s, comb, i + 2), comb = comb[:-3]
        #       if int(s[i:i + 3]) <= 255:
        #           comb += s[i:i + 3] + ".", self.backtrack(s, comb, i + 3), comb = comb[:-4]

        self.res = []
        self.backtrack(s, 0, [])
        return self.res
    
    def backtrack(self, s, index, comb, digits):
        if index == len(s) and len(comb) == 4:
            self.res.append("".join(comb)[:-1])
            return
        if index >= len(s): return
        if len(comb) >= 4: return

        # single digit
        comb.append(s[index] + ".")
        self.backtrack(s, index + 1, comb)
        comb.pop()

        # double digits
        num = s[index: index + 2]
        if num[0] != "0":
            comb.append(num + ".")
            self.backtrack(s, index + 2, comb)
            comb.pop()
        
        # triple digits
        num = s[index: index + 3]
        if num[0] != "0" and 0 <= int(num) <= 255:
            comb.append(num + ".")
            self.backtrack(s, index + 3, comb)
            comb.pop()

    def iterative(self, s):
        res = []
        queue = deque([([], 0)]) # holds (comb, index)

        while queue:
            comb, index = queue.popleft()

            if index == len(s) and len(comb) == 4:
                res.append("".join(comb)[:-1])
                continue
            if index >= len(s): continue
            if len(comb) >= 4: continue

            # single digit
            queue.append((comb + [s[index] + "."], index + 1))

            # double digits
            num = s[index: index + 2]
            if num[0] != "0": queue.append((comb + [num + "."], index + 2))

            # triple digits
            num = s[index: index + 3]
            if num[0] != "0" and 0 <= int(num) <= 255: queue.append((comb + [num + "."], index + 3))
        
        return res