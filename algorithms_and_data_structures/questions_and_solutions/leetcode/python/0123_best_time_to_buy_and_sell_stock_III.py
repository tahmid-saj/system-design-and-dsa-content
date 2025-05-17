class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        # return self.twoPass(prices)
        return self.onePass(prices)

    def twoPass(self, prices):
        if len(prices) <= 1: return 0
        f, b = [0 for _ in range(len(prices))], [0 for _ in range(len(prices))]

        minPrice, maxProfit = prices[0], 0
        for i in range(1, len(prices)):
            minPrice = min(minPrice, prices[i])
            maxProfit = max(maxProfit, prices[i] - minPrice)
            f[i] = maxProfit

        maxPrice, maxProfit = prices[-1], 0
        for i in range(len(prices) - 2, -1, -1):
            maxPrice = max(maxPrice, prices[i])
            maxProfit = max(maxProfit, maxPrice - prices[i] + f[i])
            b[i] = maxProfit
        
        return max(b)
    
    def onePass(self, prices):
        if len(prices) <= 1: return 0

        t1Cost, t2Cost = math.inf, math.inf
        t1Profit, t2Profit = 0, 0
        for i in range(len(prices)):
            t1Cost = min(t1Cost, prices[i])
            t1Profit = max(t1Profit, prices[i] - t1Cost)
            t2Cost = min(t2Cost, prices[i] - t1Profit)
            t2Profit = max(t2Profit, prices[i] - t2Cost)
        
        return t2Profit