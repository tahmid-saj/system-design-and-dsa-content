class Solution:
    def totalFruit(self, fruits: List[int]) -> int:
        maxLength, windowStart = 0, 0
        baskets = {}

        for windowEnd in range(0, len(fruits)):
            baskets[fruits[windowEnd]] = baskets.get(fruits[windowEnd], 0) + 1
            if len(baskets) <= 2: maxLength = max(maxLength, windowEnd - windowStart + 1)

            while len(baskets) > 2:
                if baskets[fruits[windowStart]] == 1: baskets.pop(fruits[windowStart])
                else: baskets[fruits[windowStart]] -= 1
                windowStart += 1

        return maxLength