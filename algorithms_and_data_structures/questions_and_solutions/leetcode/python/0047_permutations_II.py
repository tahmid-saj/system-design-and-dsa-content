class Solution:
    def permuteUnique(self, nums: List[int]) -> List[List[int]]:
        self.res = []
        counter = Counter(nums)
        self.backtrack(nums, counter, [])
        return self.res
    
    def backtrack(self, nums, counter, comb):
        if len(comb) == len(nums):
            self.res.append(list(comb))
            return
        
        for num in counter:
            if counter[num] > 0:
                comb.append(num)
                counter[num] -= 1
                self.backtrack(nums, counter, comb)
                comb.pop()
                counter[num] += 1