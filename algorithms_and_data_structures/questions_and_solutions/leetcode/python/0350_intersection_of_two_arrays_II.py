class Solution(object):
    def intersect(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: List[int]
        """
        nums1Count = {}
        for num1 in nums1:
            if not num1 in nums1Count: nums1Count[num1] = 1
            else: nums1Count[num1] += 1

        res = []
        for num2 in nums2:
            if num2 in nums1Count:
                if nums1Count[num2] == 1: nums1Count.pop(num2)
                else: nums1Count[num2] -= 1
                res.append(num2)
        
        return res