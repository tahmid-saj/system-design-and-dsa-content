class Solution:
    def checkIfExist(self, arr: List[int]) -> bool:
        seen = set()
        for i in range(len(arr)):
            if (arr[i] * 2) in seen or (arr[i] / 2) in seen: return True
            seen.add(arr[i])
        return False