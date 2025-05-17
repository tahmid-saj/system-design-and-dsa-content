class Solution:
    def relativeSortArray(self, arr1: List[int], arr2: List[int]) -> List[int]:
        presentElements = {}
        lengthOfArr1 = len(arr1)

        for i in range(len(arr2)):
            presentElements[arr2[i]] = i

        def relativeSort(x):
            if x in presentElements:
                return presentElements[x]
            return x + lengthOfArr1

        arr1.sort(key = relativeSort)
        return arr1