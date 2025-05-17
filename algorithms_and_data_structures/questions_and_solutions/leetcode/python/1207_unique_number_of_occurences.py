class Solution:
    def uniqueOccurrences(self, arr: List[int]) -> bool:
        freq, occurence = {}, set()
        for i in range(len(arr)): freq[arr[i]] = freq.get(arr[i], 0) + 1
        for k, v in freq.items():
            if v in occurence: return False
            occurence.add(v)
        
        return True