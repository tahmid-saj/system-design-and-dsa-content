class Solution:
    def distributeCandies(self, candyType: List[int]) -> int:
        # if the distinct number of elements are more than n // 2: return n // 2
        # else if lower: return distinct number of elements
        distinct = 1
        # loop through candyType using i (1, len(candyType)):
        # if candyType[i] != candyType[i - 1]: distinct += 1
        # if distinct >= n // 2: return n // 2
        # return distinct
        candyType.sort()
        for i in range(1, len(candyType)):
            if candyType[i] != candyType[i - 1]: distinct += 1
        
        if distinct >= len(candyType) // 2: return len(candyType) // 2
        return distinct