class Solution:
    def compress(self, s: List[str]) -> int:
        if len(s) == 0: return ""
        count, i = 1, 0
        for j in range(1, len(s)):
            if s[j] != s[j - 1]:
                s[i] = s[j - 1]
                i += 1
                if count > 1:
                    occurence = str(count)
                    s[i:i + len(occurence)] = list(occurence)
                    i += len(occurence)
                count = 1
            else: count += 1
        
        s[i] = s[-1]
        i += 1
        if count > 1:
            occurence = str(count)
            s[i:i + len(occurence)] = list(occurence)
            i += len(occurence)
        
        return i