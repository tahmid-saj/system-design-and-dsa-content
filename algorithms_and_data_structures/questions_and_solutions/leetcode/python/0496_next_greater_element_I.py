class Solution:
    def nextGreaterElement(self, nums1: List[int], nums2: List[int]) -> List[int]:
        stk, nge = [], {num1: -1 for num1 in nums1}

        for i in range(len(nums2)):
            while stk and stk[-1] < nums2[i]:
                num1 = stk.pop()
                if num1 in nge: nge[num1] = nums2[i]
            stk.append(nums2[i])
        
        return list(nge.values())