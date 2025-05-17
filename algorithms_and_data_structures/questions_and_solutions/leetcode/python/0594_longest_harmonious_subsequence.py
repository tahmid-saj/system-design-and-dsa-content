class Solution:
    def findLHS(self, nums: List[int]) -> int:
        res = 0
        count_map = {}

        for num in nums:
            if num not in count_map.keys():
                count_map[num] = 1
            else:
                count_map[num] += 1

        # 1:1, 2:3, 3:2, 5:1, 7:1

        for num, count in count_map.items():
            if num + 1 in count_map:
                res = max(count + count_map[num + 1], res)

        return res