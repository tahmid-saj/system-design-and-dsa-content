class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        # if prices are going down, don't buy them
        # if prices are going up, but them and sell them on the next day
        res = 0
        for i in range(0, len(prices) - 1):
            if prices[i] < prices[i + 1]: res += prices[i + 1] - prices[i]
        
        return res