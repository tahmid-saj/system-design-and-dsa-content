class Solution:
    def buddyStrings(self, s: str, goal: str) -> bool:
        if len(s) != len(goal): return False
        swapS, swapGoal = defaultdict(int), defaultdict(str)
        same = {}
        for i in range(len(s)):
            if s[i] != goal[i]:
                if s[i] in swapS or i in swapGoal: return False
                swapS[s[i]] = i
                swapGoal[i] = goal[i]
            if s[i] == goal[i]: 
                same[s[i]] = same.get(s[i], 0) + 1
        for k, v in same.items():
            if v >= 2 and len(swapS) == 0: return True
        if len(swapS) != 2: return False

        for k, v in swapS.items():
            if v not in swapGoal: return False
            g1 = swapGoal[v]
            if g1 not in swapS: return False
            s2 = swapS[g1]
            if s2 not in swapGoal: return False
            g2 = swapGoal[s2]
        
        return True