class Solution:
    def twoCitySchedCost(self, costs: List[List[int]]) -> int:
        return self.greedy1(costs)
        # return self.greedy2(costs)

    def greedy1(self, costs):
        costs.sort(key=lambda x: x[0] - x[1])

        cost, i, j = 0, 0, len(costs) - 1
        while i < j:
            cost += costs[i][0] + costs[j][1]
            i += 1
            j -= 1
            
        return cost
    
    def greedy2(self, costs):
        costs.sort(key=lambda x: x[0] - x[1])

        i, j, res = 0, len(costs) - 1, 0
        while i < j:
            if costs[i][0] + costs[j][1] < costs[i][1] + costs[j][0]: res += costs[i][0] + costs[j][1]
            else: res += costs[i][1] + costs[j][0]
            i += 1
            j -= 1
        
        return res