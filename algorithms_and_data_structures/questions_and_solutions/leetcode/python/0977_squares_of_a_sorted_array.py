class Solution:
    def sortedSquares(self, nums: List[int]) -> List[int]:
        n = len(nums)
        squares = [0 for x in range(n)]
        
        l, r, i = 0, n - 1, n - 1
        while l <= r:
            lRes = nums[l] * nums[l]
            rRes = nums[r] * nums[r]

            if lRes < rRes:
                squares[i] = rRes
                r -= 1
            else:
                squares[i] = lRes
                l += 1

            i -= 1

        return squares