class Solution:
    def jump(self, nums: List[int]) -> int:
        curr_farthest, curr_farthest_end, res = 0, 0, 0

        for i in range(len(nums) - 1):
            curr_farthest = max(curr_farthest, i + nums[i])

            if i == curr_farthest_end:
                res += 1
                curr_farthest_end = curr_farthest
        
        return res