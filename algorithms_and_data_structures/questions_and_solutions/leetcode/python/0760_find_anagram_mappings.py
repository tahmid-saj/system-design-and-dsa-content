class Solution:
    def anagramMappings(self, nums1: List[int], nums2: List[int]) -> List[int]:
        index, res = {}, []
        for i in range(len(nums2)): index[nums2[i]] = i

        for i in range(len(nums1)): res.append(index[nums1[i]])
        return res