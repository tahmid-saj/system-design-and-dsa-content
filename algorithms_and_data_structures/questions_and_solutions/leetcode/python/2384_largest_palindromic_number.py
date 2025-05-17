class Solution:
    def largestPalindromic(self, num: str) -> str:
        freq = {}
        for i in range(len(num)): freq[num[i]] = freq.get(num[i], 0) + 1
        res, odd = "", ""
        # loop through 9 to 0 using i:
        #   if i in freq:
        #       if i % 2 == 0: res += i * (freq[i] // 2), freq.pop(i)
        #       elif i % 2 != 0: res += i * ((freq[i] - 1) // 2), freq.pop(i), if odd == "": odd = i
        for i in "9876543210":
            if i in freq:
                if freq[i] % 2 == 0: res += i * (freq[i] // 2)
                elif freq[i] % 2 != 0:
                    if freq[i] > 2: res += i * ((freq[i] - 1) // 2)
                    if odd == "": odd = i
                freq.pop(i)
        
        if res != "" and res[0] == "0" and odd == "": return "0"
        if res != "" and res[0] == "0" and odd != "": return odd
                
        return res + odd + res[::-1]