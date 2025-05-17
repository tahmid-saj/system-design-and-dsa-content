class Solution(object):
    def maxProfit(self, prices):
        """
        :type prices: List[int]
        :rtype: int
        """
        profit, minPrices = 0, 1e8
        # loop through prices using i:
        # -> if minPrices > prices[i]: minPrices = prices[i]
        # -> profit = max(profit, prices[i] - minPrices)
        # return profit
        for i in range(len(prices)):
            if minPrices > prices[i]: minPrices = prices[i]
            profit = max(profit, prices[i] - minPrices)
        return profit