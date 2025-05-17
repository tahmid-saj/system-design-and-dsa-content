class Solution:
    def numRescueBoats(self, people: List[int], limit: int) -> int:
        i, j, res = 0, len(people) - 1, 0
        people.sort()

        while i < j:
            if people[i] + people[j] <= limit: i += 1
            j -= 1
            res += 1
        
            if i == j: res += 1
        
        return res