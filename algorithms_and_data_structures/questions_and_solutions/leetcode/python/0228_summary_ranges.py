class Solution(object):
    def summaryRanges(self, nums):
        """
        :type nums: List[int]
        :rtype: List[str]
        """
        if len(nums) == 0: return []
        res = [""]
        res[0] = str(nums[0])
        if len(nums) == 1:
            return res
        # start = nums[0]
        # j = 0
        # res = [(str)nums[0]]
        # loop through nums using i (1 to len(nums)):
        # -> if nums[i] - start > 1:
        #       if start == nums[i - 1]: j += 1, res[j] += (str)nums[i], start = nums[i]
        #       elif start != nums[i - 1]: res[j] += "->" + (str)nums[i - 1], j += 1, res[j] = nums[i], start = nums[i]
        # -> elif nums[i] - start == 1 and i == len(nums) - 1: res[j] += "->" + (str)nums[i]
        # return res
        start = nums[0]
        j = 0

        for i in range(1, len(nums)):
            if nums[i] - nums[i - 1] > 1:
                if start == nums[i - 1]:
                    j += 1
                    res.append("")
                    res[j] += str(nums[i])
                    start = nums[i]
                elif start != nums[i - 1]:
                    res[j] += "->" + str(nums[i - 1])
                    j += 1
                    res.append("")
                    res[j] = str(nums[i])
                    start = nums[i]
            elif nums[i] - nums[i - 1] == 1 and i == len(nums) - 1:
                res[j] += "->" + str(nums[i])

        return res