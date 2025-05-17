class Solution:
    def minWindow(self, paragraph: str, keywords: str) -> str:
        subarray = namedtuple("subarray", ("start", "end"))
        start, res = 0, subarray(-1, -1)
        keywordsCounter, keywordsToCover = Counter(keywords), len(keywords)
        words = set(keywords)

        for end in range(len(paragraph)):
            if paragraph[end] in words:
                keywordsCounter[paragraph[end]] -= 1
                if keywordsCounter[paragraph[end]] >= 0: keywordsToCover -= 1
            
            while keywordsToCover == 0:
                if (res.start == -1 and res.end == -1) or res.end - res.start > end - start: res = subarray(start, end)

                if paragraph[start] in words:
                    keywordsCounter[paragraph[start]] += 1
                    if keywordsCounter[paragraph[start]] > 0: keywordsToCover += 1
                start += 1
        
        return paragraph[res.start:res.end + 1]