class Solution:
    def rotateString(self, s: str, goal: str) -> bool:
        return self.bruteForce(s, goal)
        # return self.simpleCheck(s, goal)
    
    def simpleCheck(self, s, goal):
        return len(s) == len(goal) and s in (goal + goal)
    
    def bruteForce(self, s, goal):
        if len(s) != len(goal): return False
        if len(s) == 0: return True

        for shift in range(len(s)):
            if all(s[i] == goal[(shift + i) % len(s)] for i in range(len(s))): return True
        return False