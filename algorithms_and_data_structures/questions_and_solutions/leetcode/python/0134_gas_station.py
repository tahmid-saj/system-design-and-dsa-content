class Solution:
    def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:
        totalGas = sum(gas)
        totalCost = sum(cost)
        if totalGas < totalCost: return -1

        tank, res = 0, 0
        for i in range(len(gas)):
            tank += gas[i] - cost[i]
            if tank < 0:
                tank = 0
                res = i + 1
        
        return res