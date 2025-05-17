class Solution:
    def judgeCircle(self, moves: str) -> bool:
        # U = vertical += 1, D = vertical -= 1
        # R = horizontal += 1, L = -= 1
        # loop through moves using i:
        # if moves[i] == "U": vertical += 1
        # elif moves[i] == "D": vertical -= 1
        # elif moves[i] == "R": horizontal += 1
        # elif moves[i] == "L": horizontal -= 1
        vertical, horizontal = 0, 0

        for i in range(0, len(moves)):
            if moves[i] == "U": vertical += 1
            elif moves[i] == "D": vertical -= 1
            elif moves[i] == "R": horizontal += 1
            elif moves[i] == "L": horizontal -= 1

        return vertical == 0 and horizontal == 0