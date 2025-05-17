class Solution:
  def solveKnapsack(self, profits, weights, capacity):
    # return self.knapsackRecursive(profits, weights, capacity, 0)

    # self.dp = [[-1 for _ in range(capacity + 1)] for _ in range(len(weights))]
    # return self.knapsackTopdown(profits, weights, capacity, 0)

    # return self.knapsackBottomUp(profits, weights, capacity)
    return self.knapsackBottomUpLinearSpace(profits, weights, capacity)
  
  def knapsackRecursive(self, profits, weights, capacity, index):
    if capacity <= 0 or index >= len(profits): return 0
    
    profit1, profit2 = 0, 0
    if capacity - weights[index] >= 0: profit1 = profits[index] + self.knapsackRecursive(profits, weights, capacity - weights[index], index + 1)
    profit2 = self.knapsackRecursive(profits, weights, capacity, index + 1)

    return max(profit1, profit2) 

  def knapsackTopdown(self, profits, weights, capacity, index):
    if capacity <= 0 or index >= len(profits): return 0
    if self.dp[index][capacity] != -1: return self.dp[index][capacity]

    profit1, profit2 = 0, 0
    if capacity - weights[index] >= 0: profit1 = profits[index] + self.knapsackTopdown(profits, weights, capacity - weights[index], index + 1)
    profit2 = self.knapsackTopdown(profits, weights, capacity, index + 1)

    self.dp[index][capacity] = max(profit1, profit2)
    return self.dp[index][capacity]

  def knapsackBottomUp(self, profits, weights, capacity):
    if len(profits) == 0 or len(weights) == 0: return 0
    dp = [[0 for _ in range(capacity + 1)] for _ in range(len(weights))]

    for c in range(capacity + 1):
      if c >= weights[0]: dp[0][c] = profits[0]
    
    for i in range(1, len(weights)):
      for c in range(1, capacity + 1):
        profit1, profit2 = 0, 0
        if c - weights[i] >= 0: profit1 = profits[i] + dp[i - 1][c - weights[i]]
        profit2 = dp[i - 1][c]
        dp[i][c] = max(profit1, profit2)
    
    return dp[-1][-1]

  def knapsackBottomUpLinearSpace(self, profits, weights, capacity):
    if len(profits) == 0 or len(weights) == 0: return 0
    dp = [0 for _ in range(capacity + 1)]

    for c in range(capacity + 1):
      if c - weights[0] >= 0: dp[c] = profits[0]
    
    for i in range(1, len(weights)):
      for c in range(capacity, -1, -1):
        profit1, profit2 = 0, 0
        if c - weights[i] >= 0: profit1 = profits[i] + dp[c - weights[i]]
        profit2 = dp[c]
        dp[c] = max(profit1, profit2)
    
    return dp[-1]