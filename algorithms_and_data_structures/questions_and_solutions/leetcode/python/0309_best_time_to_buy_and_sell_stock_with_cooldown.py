class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        # return self.dpStateMachine(prices)
        return self.dpOn2(prices)

    def dpStateMachine(self, prices):
        sold, held, reset = -math.inf, -math.inf, 0

        for i in range(len(prices)):
            prevSold = sold
            sold = held + prices[i]
            held = max(held, reset - prices[i])
            reset = max(reset, prevSold)
        
        return max(sold, reset)

    def dpOn2(self, prices):
        L = len(prices)
        # padding the array with additional zero to simply the logic
        MP = [0] * (L + 2)

        for i in range(L-1, -1, -1):
            C1 = 0
            # Case 1). buy and sell the stock
            for sell in range(i + 1, L):
                profit = (prices[sell] - prices[i]) + MP[sell + 2]
                C1 = max(profit, C1)

            # Case 2). do no transaction with the stock p[i]
            C2 = MP[i + 1]

            # sum up two cases
            MP[i] = max(C1, C2)

        return MP[0]