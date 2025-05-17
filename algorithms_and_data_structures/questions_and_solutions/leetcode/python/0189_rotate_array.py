class Solution:
    def rotate(self, nums: List[int], k: int) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        k = k % len(nums)
        if k == 0: return
        # push to front
        # for i in range(len(nums) - k, len(nums)): nums.insert(0, nums.pop())

        # cyclic replacements
        c, i, prev = 0, 0, None
        while c < len(nums):
            j = i + k
            if j > len(nums) - 1: j = (i + k) % len(nums)

            if prev == None: 
                prev = nums[j]
                nums[j] = nums[i]
            else:
                tmp = nums[j]
                nums[j] = prev
                prev = tmp

            c += 1
            i = j
            if (c % 2 == 0 and len(nums) / k == 2) or (len(nums) % 2 == 0 and i == 0):
                prev = None 
                i += 1