class Solution:
    def intervalIntersection(self, firstList: List[List[int]], secondList: List[List[int]]) -> List[List[int]]:
        i, j, res = 0, 0, []

        while i < len(firstList) and j < len(secondList):
            # see if a and b overlap
            a_overlaps_b = (firstList[i][1] >= secondList[j][0] and firstList[i][1] <= secondList[j][1]) or (secondList[j][0] >= firstList[i][0] and secondList[j][1] <= firstList[i][1])
            b_overlaps_a = (secondList[j][1] >= firstList[i][0] and secondList[j][1] <= firstList[i][1]) or (firstList[i][0] >= secondList[j][0] and firstList[i][1] <= secondList[j][1])

            # add the overlap
            if a_overlaps_b or b_overlaps_a:
                start = max(firstList[i][0], secondList[j][0])
                end = min(firstList[i][1], secondList[j][1])
                res.append([start, end])

            # increment i or j
            if firstList[i][1] <= secondList[j][1]: i += 1
            else: j += 1
        
        return res