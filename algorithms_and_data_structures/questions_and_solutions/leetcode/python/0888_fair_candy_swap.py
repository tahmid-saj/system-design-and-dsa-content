class Solution:
    def fairCandySwap(self, aliceSizes: List[int], bobSizes: List[int]) -> List[int]:
        sumA, sumB = sum(aliceSizes), sum(bobSizes)
        setB = set(bobSizes)
        for num in aliceSizes:
            if num + (sumB - sumA) / 2 in setB: return [num, num + (sumB - sumA) / 2]