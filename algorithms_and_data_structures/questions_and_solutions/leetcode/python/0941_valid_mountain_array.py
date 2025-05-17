class Solution:
    def validMountainArray(self, arr: List[int]) -> bool:
        if len(arr) < 3: return False

        i = 1
        while i < len(arr) and arr[i - 1] < arr[i]:
            if arr[i - 1] == arr[i]: return False
            i += 1
        if i == 1 or i == len(arr): return False
        
        while i < len(arr) and arr[i - 1] > arr[i]:
            if arr[i - 1] == arr[i]: return False
            i += 1
        
        return i == len(arr)