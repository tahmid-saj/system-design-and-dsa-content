class Solution(object):
    def merge(self, nums1, m, nums2, n):
        """
        :type nums1: List[int]
        :type m: int
        :type nums2: List[int]
        :type n: int
        :rtype: None Do not return anything, modify nums1 in-place instead.
        """
        # we can work backwards from m to 0 for nums1, n to 0 for nums2 inserting at m + n towards 0
        # i in range(m, -1, -1), j in range (n, -1, -1), k in range (m + n, -1, -1), while k >= 0:
        # -> if nums1[i] < nums2[j]: nums1[k] = nums2[j], j--, k--
        # -> elif nums1[i] >= nums2[j]: nums1[k] = nums1[i], i--, k--
        # return nums1

        if n == 0: return

        i, j, k = m - 1, n - 1, m + n - 1

        while j >= 0:
            if i >= 0 and nums1[i] > nums2[j]:
                nums1[k] = nums1[i]
                i -= 1
                k -= 1
            else:
                nums1[k] = nums2[j]
                j -= 1
                k -= 1
        