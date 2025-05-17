class Solution:
    def minimumDeletions(self, nums: List[int]) -> int:
        return self.constantSpace(nums)
        # return self.twoPointers(nums)
    
    def constantSpace(self, nums):
        minIndex = nums.index(min(nums))
        maxIndex = nums.index(max(nums))

        min_start_dist = minIndex + 1
        min_end_dist = len(nums) - minIndex
        max_start_dist = maxIndex + 1
        max_end_dist = len(nums) - maxIndex

        res = min(
            max(min_start_dist, max_start_dist),
            max(min_end_dist, max_end_dist),
            min(min_start_dist + max_end_dist, max_start_dist + min_end_dist)
        )

        return res

    def twoPointers(self, nums):
        if len(nums) == 1: return 1
        minIndex, minNum = -1, math.inf
        for i in range(len(nums)):
            if nums[i] < minNum:
                minNum = nums[i]
                minIndex = i

        maxIndex, maxNum = -1, -math.inf
        for i in range(len(nums)):
            if nums[i] > maxNum:
                maxNum = nums[i]
                maxIndex = i

        res, i, j = 0, 0, len(nums) - 1
        while i < j:
            min_i_dist, min_j_dist, max_i_dist, max_j_dist = abs(minIndex - i), abs(minIndex - j), abs(maxIndex - i), abs(maxIndex - j)
            closest_i, closest_j = min(min_i_dist, max_i_dist), min(min_j_dist, max_j_dist)

            if closest_i < closest_j: 
                if i == maxIndex: maxIndex = math.inf
                elif i == minIndex: minIndex = math.inf
                res += 1
                i += 1
            elif (minIndex == i and maxIndex == j) or (maxIndex == i and minIndex == j):
                if i == maxIndex: maxIndex = math.inf
                elif i == minIndex: minIndex = math.inf
                if j == maxIndex: maxIndex = math.inf
                elif j == minIndex: minIndex = math.inf
                res += 2
                i += 1
                j -= 1
            elif closest_j <= closest_i: 
                if j == maxIndex: maxIndex = math.inf
                elif j == minIndex: minIndex = math.inf
                res += 1
                j -= 1
            if minIndex == math.inf and maxIndex == math.inf: break
        
        return res