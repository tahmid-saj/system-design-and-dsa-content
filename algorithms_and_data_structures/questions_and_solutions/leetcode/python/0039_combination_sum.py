class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        # if s == target: self.res.append(comb), return
        # if s > target: return
        # loop through candidates using i: (index, len(candidates)):
        #   comb.append(candidates[i])
        #   self.backtrack(candidates, target, s + candidates[i], index)
        #   comb.pop()
        self.res = []
        self.backtrack(candidates, target, 0, 0, [])
        return self.res
    
    def backtrack(self, candidates, target, s, index, comb):
        if s == target:
            self.res.append(list(comb))
            return
        if s > target: return

        for i in range(index, len(candidates)):
            comb.append(candidates[i])
            self.backtrack(candidates, target, s + candidates[i], i, comb)
            comb.pop()