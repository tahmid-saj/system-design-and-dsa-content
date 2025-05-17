class Solution:
    def longestPalindrome(self, words: List[str]) -> int:
        # return self.frequencyTracking1(words)
        # return self.frequencyTracking2(words)
        return self.frequencyTracking3(words)

    def frequencyTracking1(self, words):
        seen, middle, res = {}, 0, 0
        for word in words:
            if word not in seen:
                seen[word[1] + word[0]] = seen.get(word[1] + word[0], 0) + 1
                if word[0] == word[1]: middle += 1
            elif word in seen:
                seen[word] -= 1
                if seen[word] == 0: seen.pop(word)
                res += 4
                if word[0] == word[1]: middle -= 1
        
        if middle >= 1: res += 2
        return res

    def frequencyTracking2(self, words):
        freq, middle, res = Counter(words), False, 0

        for k, v in freq.items():
            if k[0] == k[1]:
                if v % 2 == 0: res += v
                else:
                    res += v - 1
                    middle = True
            elif k[0] < k[1]: res += 2 * min(v, freq[k[1] + k[0]])
        
        if middle: res += 1
        return res * 2
    
    def frequencyTracking3(self, words):
        freq, middle, res = [[0 for _ in range(26)] for _ in range(26)], False, 0

        for word in words: freq[ord(word[0]) - ord('a')][ord(word[1]) - ord('a')] += 1

        for i in range(26):
            if freq[i][i] % 2 == 0: res += freq[i][i]
            else:
                res += freq[i][i] - 1
                middle = True
            for j in range(i + 1, 26): res += 2 * min(freq[i][j], freq[j][i])
        
        if middle: res += 1
        return res * 2