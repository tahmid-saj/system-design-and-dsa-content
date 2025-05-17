class Solution(object):
    def intersection(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: List[int]
        """
        set1 = { num1 for num1 in nums1 }

        res = set()
        for num2 in nums2:
            if num2 in set1: 
                res.add(num2)
        
        return list(res)