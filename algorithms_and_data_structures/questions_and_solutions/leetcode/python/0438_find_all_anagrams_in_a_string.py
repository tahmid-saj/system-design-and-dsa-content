class Solution:
    def findAnagrams(self, s: str, p: str) -> List[int]:
        # return self.twoHashmaps(s, p)
        # return self.oneHashmap(s, p)
        return self.twoArrays(s, p)

    def twoHashmaps(self, s, p):
        freqS, freqP = {}, {}
        for i in range(len(p)): freqP[p[i]] = freqP.get(p[i], 0) + 1

        windowStart, res = 0, []
        for windowEnd in range(0, len(s)):
            freqS[s[windowEnd]] = freqS.get(s[windowEnd], 0) + 1

            if windowEnd - windowStart == len(p):
                freqS[s[windowStart]] -= 1
                if freqS[s[windowStart]] == 0: freqS.pop(s[windowStart])
                windowStart += 1
            
            if freqS == freqP: res.append(windowStart)
        
        return res

    def oneHashmap(self, s, p):
        freqP = {}
        for i in range(len(p)): freqP[p[i]] = freqP.get(p[i], 0) + 1

        windowStart, res, matched = 0, [], 0
        for windowEnd in range(0, len(s)):
            if s[windowEnd] in freqP:
                freqP[s[windowEnd]] -= 1
                if freqP[s[windowEnd]] == 0: matched += 1
            
            if windowEnd - windowStart == len(p):
                if s[windowStart] in freqP: 
                    if freqP[s[windowStart]] == 0: matched -= 1
                    freqP[s[windowStart]] += 1
                windowStart += 1
            
            if matched == len(freqP): res.append(windowStart)
        
        return res
    
    def twoArrays(self, s, p):
        arrS, arrP = [0 for _ in range(26)], [0 for _ in range(26)]
        for i in range(len(p)): arrP[ord(p[i]) - ord('a')] += 1

        windowStart, res = 0, []
        for windowEnd in range(0, len(s)):
            arrS[ord(s[windowEnd]) - ord('a')] += 1

            if windowEnd - windowStart == len(p):
                arrS[ord(s[windowStart]) - ord('a')] -= 1
                windowStart += 1
            
            if arrS == arrP: res.append(windowStart)
        
        return res