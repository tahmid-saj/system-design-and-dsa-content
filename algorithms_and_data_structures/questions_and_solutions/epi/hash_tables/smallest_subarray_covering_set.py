from collections import namedtuple, Counter
class Solution:
    def smallestSubarrayCoveringSet(self, paragraph, keywords):
        dist = namedtuple("dist", ("start", "end"))
        keywordsCounter = Counter(keywords)
        start, res, keywordsToCover = 0, dist(-1, -1), len(keywords)

        for end in range(0, len(paragraph)):
            if paragraph[end] in keywords:
                keywordsCounter[paragraph[end]] -= 1
                if keywordsCounter[paragraph[end]] >= 0: keywordsToCover -= 1
            
            while keywordsToCover == 0:
                if res == dist(-1, -1) or res.end - res.start > end - start: res = dist(start, end)
                if paragraph[start] in keywords:
                    keywordsCounter[paragraph[start]] += 1
                    if keywordsCounter[paragraph[start]] >= 0: keywordsToCover += 1
                start += 1
        
        return res
