class Solution:
    def findRelativeRanks(self, score: List[int]) -> List[str]:
        # 5 4 3 2 1
        scoreMap = {}
        for i in range(0, len(score)): scoreMap[score[i]] = i
        score.sort()

        # 1 2 3 4 5
        # loop through score using i:
        # if len(score) > 3 and i < len(score) - 3: res[scoreMap[score[i]]] = str(len(score) - i)
        # elif i == len(score) - 3: res[scoreMap[score[i]]] = "Bronze Medal"
        # elif i == len(score) - 2: res[scoreMap[score[i]]] = "Silver Medal"
        # elif i == len(score) - 1: res[scoreMap[score[i]]] = "Gold Medal"
        # return res
        res = [0] * len(score)
        for i in range(0, len(score)):
            if len(score) > 3 and i < len(score) - 3: res[scoreMap[score[i]]] = str(len(score) - i)
            elif i == len(score) - 3: res[scoreMap[score[i]]] = "Bronze Medal"
            elif i == len(score) - 2: res[scoreMap[score[i]]] = "Silver Medal"
            elif i == len(score) - 1: res[scoreMap[score[i]]] = "Gold Medal"

        return res