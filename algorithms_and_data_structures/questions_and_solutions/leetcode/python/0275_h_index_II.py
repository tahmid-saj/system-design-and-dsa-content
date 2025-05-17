class Solution:
    def hIndex(self, citations: List[int]) -> int:
        # return self.linearSearch(citations)
        return self.binarySearch(citations)
    
    def linearSearch(self, citations):
        i = 0
        while i < len(citations) and citations[-(i + 1)] > i: i += 1
        return i
    
    def binarySearch(self, citations):
        l, r, res = 0, len(citations) - 1, 0
        while l <= r:
            middle = l + (r - l) // 2
            if citations[middle] == len(citations) - middle: return len(citations) - middle
            if citations[middle] < len(citations) - middle: l = middle + 1
            else: r = middle - 1
        return len(citations) - l