class Solution:
    def findDifference(self, nums1: List[int], nums2: List[int]) -> List[List[int]]:
        set1, set2, res = set(nums1), set(nums2), [[], []]
        for num in set1: 
            if num not in set2: res[0].append(num)
        for num in set2:
            if num not in set1: res[1].append(num)
        
        return res