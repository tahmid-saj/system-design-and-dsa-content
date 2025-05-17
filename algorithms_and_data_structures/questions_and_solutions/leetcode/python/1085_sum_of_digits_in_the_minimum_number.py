class Solution:
    def sumOfDigits(self, nums: List[int]) -> int:
        minimum = min(nums)

        res = 0
        while minimum > 0:
            res += minimum % 10
            minimum //= 10
        if res % 2 == 0: return 1
        return 0