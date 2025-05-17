class Solution:
    def exclusiveTime(self, n: int, logs: List[str]) -> List[int]:
        res, stk = [0 for _ in range(n)], []

        for i in range(len(logs)):
            currLog = logs[i].split(":")
            Id, state, time = int(currLog[0]), currLog[1], int(currLog[2])

            if state == "start": stk.append((Id, state, time))
            else:
                topId, topState, topTime = stk.pop()
                res[topId] += time - int(topTime) + 1
                if stk: res[stk[-1][0]] -= time - int(topTime) + 1
        
        return res