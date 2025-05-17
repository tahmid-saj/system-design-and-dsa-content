class Solution:
    def minWindow(self, paragraph: str, keywords: str) -> str:
        subarray = namedtuple("subarray", ("start", "end"))
        keywordToIndex = {k: i for i, k in enumerate(keywords)}
        latestOccurence = [-1 for _ in range(len(keywords))]
        shortestSubarrayLength = [math.inf for _ in range(len(keywords))]
        shortestDistance = math.inf
        result = subarray(-1, -1)

        for i, p in enumerate(paragraph):
            if p in keywordToIndex:
                keywordIndex = keywordToIndex[p]
                if keywordIndex == 0: shortestSubarrayLength[keywordIndex] = 1
                elif shortestSubarrayLength[keywordIndex - 1] != math.inf:
                    distanceToPreviousKeyword = (i - latestOccurence[keywordIndex - 1])
                    shortestSubarrayLength[keywordIndex] = (distanceToPreviousKeyword + shortestSubarrayLength[keywordIndex - 1])
                latestOccurence[keywordIndex] = i

                if (keywordIndex == len(keywords) - 1 and shortestSubarrayLength[-1] < shortestDistance):
                    shortestDistance = shortestSubarrayLength[-1]
                    result = subarray(i - shortestDistance + 1, i)
        
        return paragraph[result.start:result.end + 1]