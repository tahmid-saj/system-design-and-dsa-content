class Solution:
    def gcdOfStrings(self, str1: str, str2: str) -> str:
        if str1 + str2 != str2 + str1: return ""
        maxLength = gcd(len(str1), len(str2))
        return str2[:maxLength]