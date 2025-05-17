class Solution:
    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        # if s == target: self.res.append(comb), return
        # if s > target: return
        # i = index, while i < len(candidates):
        #   comb.append(candidates[i])
        #   self.backtrack(candidates, target, s + candidates[i], i + 1)
        #   comb.pop()
        #   if s + candidates[i] > target: return
        #   if s + candidates[i] == target: while i + 1 < len(candidates) and candidates[i] == candidates[i + 1]: i += 1
        candidates.sort()
        self.res = set()
        self.backtrack(candidates, target, 0, [], 0)
        return self.res
    
    def backtrack(self, candidates, target, s, comb, index):
        if s > target: return
        if s == target:
            self.res.add(tuple(comb))
            return

        i = index
        while i < len(candidates):
            if s + candidates[i] > target: return
            comb.append(candidates[i])
            self.backtrack(candidates, target, s + candidates[i], comb, i + 1)
            comb.pop()
            if s + candidates[i] == target:
                while i + 1 < len(candidates) and candidates[i] == candidates[i + 1]: i += 1
            i += 1