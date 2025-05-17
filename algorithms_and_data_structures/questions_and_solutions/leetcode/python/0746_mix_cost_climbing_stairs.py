class Solution:
    def minCostClimbingStairs(self, cost: List[int]) -> int:
        # self.minCost = math.inf
        # self.knapsack(cost, 0, 0)
        # return self.minCost

        dp = {}
        return self.topDown(cost, len(cost), dp)

        # dp = [0 for i in range(len(cost) + 1)]
        # return self.bottomUp(cost, dp)

        return self.bottomUpConstantSpace(cost)
    
    def knapsack(self, cost, curr, index):
        if index == len(cost): 
            self.minCost = min(self.minCost, curr)
            return True
        if index > len(cost):return False

        if index + 1 <= len(cost):
            self.knapsack(cost, curr + cost[index], index + 1)
            if index == 0: self.knapsack(cost, curr, index + 1)
        if index + 2 <= len(cost): self.knapsack(cost, curr + cost[index], index + 2)

        return False
    
    def topDown(self, cost, index, dp):
        if index <= 1: return 0
        if index in dp: return dp[index]

        oneStep = cost[index - 1] + self.topDown(cost, index - 1, dp)
        twoStep = cost[index - 2] + self.topDown(cost, index - 2, dp)
        dp[index] = min(oneStep, twoStep)

        return dp[index]
    
    def bottomUp(self, cost, dp):
        # dp[-1] = 0
        # dp[-2] = cost[-1]

        # for i in range(len(cost) - 2, -1, -1):
        #     dp[i] = cost[i] + min(dp[i + 1], dp[i + 2])
        
        # return min(dp[0], dp[1])

        # alternate bottomUp
        dp[0] = 0
        dp[1] = 0

        for i in range(2, len(cost) + 1):
            dp[i] = min(dp[i - 1] + cost[i - 1], dp[i - 2] + cost[i - 2])
        
        return dp[-1]
    
    def bottomUpConstantSpace(self, cost):
        # prev, curr = 0, cost[-1]

        # for i in range(len(cost) - 2, -1, -1):
        #     tmp = cost[i] + min(prev, curr)
        #     prev = curr
        #     curr = tmp
        
        # return min(curr, prev)

        # alternate bottomUpConstantSpace
        prev, curr = 0, 0
        for i in range(2, len(cost) + 1):
            tmp = min(curr + cost[i - 1], prev + cost[i - 2])
            prev = curr
            curr = tmp
        
        return curr