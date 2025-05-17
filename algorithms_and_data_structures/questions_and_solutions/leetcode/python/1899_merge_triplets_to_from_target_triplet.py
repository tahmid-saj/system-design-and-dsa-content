class Solution:
    def mergeTriplets(self, triplets: List[List[int]], target: List[int]) -> bool:
        res = set()
        for triplet in triplets:
            if triplet[0] > target[0] or triplet[1] > target[1] or triplet[2] > target[2]: continue
            for i, v in enumerate(triplet):
                if v == target[i]: res.add(i)
        
        if len(res) == 3: return True
        return False