class Solution:
    def majorityElement(self, nums: List[int]) -> List[int]:
        freq1, num1, freq2, num2 = 0, None, 0, None

        for num in nums:
            if num == num1: freq1 += 1
            elif num == num2: freq2 += 1
            elif freq1 == 0:
                num1 = num
                freq1 += 1
            elif freq2 == 0:
                num2 = num
                freq2 += 1
            else:
                freq1 -= 1
                freq2 -= 1
        
        res = []
        for num in [num1, num2]:
            if nums.count(num) > len(nums) // 3: res.append(num)
        return res