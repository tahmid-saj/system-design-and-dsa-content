class Solution:
    def hIndex(self, citations: List[int]) -> int:
        # return self.linearSearch(citations)
        return self.countingSort(citations)
    
    def linearSearch(self, citations):
        citations.sort()
        i = 0
        while i < len(citations) and citations[-(i + 1)] > i: i += 1
        return i
    
    def countingSort(self, citations):
        countArray = [0 for _ in range(max(citations) + 1)]
        outputArray = [0 for _ in range(len(citations))]

        for citation in citations: countArray[citation] += 1
        for i in range(1, len(countArray)): countArray[i] += countArray[i - 1]
        for i in range(len(outputArray)):
            outputArray[countArray[citations[i]] - 1] = citations[i]
            countArray[citations[i]] -= 1
        
        i = 0
        while i < len(outputArray) and outputArray[-(i + 1)] > i: i += 1
        return i